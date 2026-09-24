#!/usr/bin/env python3
"""Fail the build when a local smn term has no definition.

A local term is an smn: IRI that a file in ontology/modules/ types as an OWL
class, object, datatype or annotation property, or as a SKOS concept or concept
scheme. Its definition must be in the property CONVENTIONS section 10 names for
its kind: skos:definition for a SKOS term, obo:IAO_0000115 for anything else.
definition_property() below is the only place that rule is written in code.
require_term_annotations() in verify_year_age_semantic_contract.py calls
has_definition() from here rather than keeping its own copy.

The one exception is a row in ontology/definition-exemptions.csv. Every row
names the queue item that will retire it, meaning the item that will write the
definition or delete the term; the ids are items in the metasalmon hub queue
(queue/items/ in salmon-data-mobilization/metasalmon). A row retires with its
term, so this check also fails on a stale row: one whose term now has a
definition, or is no longer a local term. The change that defines or deletes a
term must therefore delete its row as well, so no row outlives its gap.

The check reads presence only. It judges no definition, so it decides nothing
about what a term means.

Before it reads the ontology, it runs against a built-in fixture. A planted
undefined term, a SKOS term defined only in the OWL property, and two stale
rows must be reported, and nothing may be reported once both terms have the
right definition and the stale rows are gone. The positive control is there
because a check that cannot fail looks exactly like one that passes.

Retires when: a gate shared with smn's sibling vocabularies enforces this
per-kind rule over smn's local terms, which would make this copy redundant.
The exemptions file goes sooner, when its last row does.
"""

from __future__ import annotations

import csv
import re
from collections import Counter
from pathlib import Path

from rdflib import Graph, Literal, URIRef
from rdflib.namespace import OWL, RDF, SKOS

ROOT = Path(__file__).resolve().parents[1]
MODULES = ROOT / "ontology" / "modules"
EXEMPTIONS = ROOT / "ontology" / "definition-exemptions.csv"

SMN = "https://w3id.org/smn/"
IAO_DEFINITION = URIRef("http://purl.obolibrary.org/obo/IAO_0000115")
SKOS_KINDS = frozenset({SKOS.Concept, SKOS.ConceptScheme})
LOCAL_KINDS = SKOS_KINDS | {
    OWL.Class,
    OWL.ObjectProperty,
    OWL.DatatypeProperty,
    OWL.AnnotationProperty,
}
# The shape of a hub queue id: a letter prefix, a hyphen and a number (B-232).
QUEUE_ID = re.compile(r"[A-Z]+-[0-9]+")

PROPERTY_CURIES = {IAO_DEFINITION: "obo:IAO_0000115", SKOS.definition: "skos:definition"}


def definition_property(*, skos_term: bool) -> URIRef:
    """Where a term's definition belongs: skos:definition for SKOS, IAO_0000115 otherwise."""
    return SKOS.definition if skos_term else IAO_DEFINITION


def has_definition(graph: Graph, term: URIRef, *, skos_term: bool) -> bool:
    """Whether the term carries the definition property for its kind. Presence only."""
    return (term, definition_property(skos_term=skos_term), None) in graph


def curie(term: URIRef) -> str:
    return "smn:" + str(term)[len(SMN):] if str(term).startswith(SMN) else f"<{term}>"


def local_terms(graph: Graph) -> dict[URIRef, bool]:
    """Every local term in the graph, mapped to whether it is a SKOS term."""
    terms: dict[URIRef, bool] = {}
    for kind in LOCAL_KINDS:
        for term in graph.subjects(RDF.type, kind):
            if isinstance(term, URIRef) and str(term).startswith(SMN):
                terms[term] = terms.get(term, False) or kind in SKOS_KINDS
    return terms


def read_exemptions(path: Path) -> tuple[dict[URIRef, tuple[int, str]], list[str]]:
    """The file's rows as {term: (line, queue id)}, and a problem for each malformed row."""
    rows: dict[URIRef, tuple[int, str]] = {}
    problems: list[str] = []
    if not path.exists():
        return rows, problems
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != ["term", "retired_by"]:
            return rows, [f"the header must be exactly 'term,retired_by', not {reader.fieldnames!r}"]
        for row in reader:
            line = reader.line_num
            if None in row or row["retired_by"] is None:
                problems.append(f"line {line}: a row has exactly two fields, term and retired_by")
                continue
            text, queue_id = row["term"].strip(), row["retired_by"].strip()
            if not text.startswith("smn:") or text == "smn:":
                problems.append(f"line {line}: {text!r} is not an smn: term")
                continue
            if not QUEUE_ID.fullmatch(queue_id):
                problems.append(
                    f"line {line}: {text} names {queue_id!r} to retire it, which is not a queue id"
                )
            term = URIRef(SMN + text[len("smn:"):])
            if term in rows:
                problems.append(f"line {line}: {text} already has a row, at line {rows[term][0]}")
                continue
            rows[term] = (line, queue_id)
    return rows, problems


def find_problems(
    graph: Graph, rows: dict[URIRef, tuple[int, str]]
) -> tuple[dict[URIRef, bool], list[URIRef], list[tuple[URIRef, str]]]:
    """Return the local terms, the undefined ones with no row, and each stale row with its reason."""
    terms = local_terms(graph)
    missing = [
        term
        for term in sorted(terms, key=str)
        if term not in rows and not has_definition(graph, term, skos_term=terms[term])
    ]
    stale: list[tuple[URIRef, str]] = []
    for term in sorted(rows, key=str):
        if term not in terms:
            stale.append((term, "is not a local term in ontology/modules/"))
        elif has_definition(graph, term, skos_term=terms[term]):
            where = PROPERTY_CURIES[definition_property(skos_term=terms[term])]
            stale.append((term, f"has a definition now, in {where}"))
    return terms, missing, stale


FIXTURE = """
@prefix smn: <https://w3id.org/smn/> .
@prefix obo: <http://purl.obolibrary.org/obo/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .

smn:Defined a owl:Class ; obo:IAO_0000115 "A defined class." .
smn:Planted a owl:Class .
smn:WrongProperty a skos:Concept ; obo:IAO_0000115 "Defined in the OWL property." .
smn:Exempted a owl:ObjectProperty .
smn:ExemptedButDefined a skos:ConceptScheme ; skos:definition "A defined scheme." .
"""


def self_test() -> list[str]:
    """Run the check on FIXTURE and return what it got wrong, which is nothing when it works."""
    graph = Graph().parse(data=FIXTURE, format="turtle")
    smn = {name: URIRef(SMN + name) for name in (
        "Planted", "WrongProperty", "Exempted", "ExemptedButDefined", "Gone"
    )}
    rows = {smn[name]: (line, "B-1") for line, name in enumerate(
        ("Exempted", "ExemptedButDefined", "Gone"), start=2
    )}
    errors = []
    _, missing, stale = find_problems(graph, rows)
    if set(missing) != {smn["Planted"], smn["WrongProperty"]}:
        errors.append(f"reported {sorted(map(curie, missing))} as undefined, "
                      "expected smn:Planted and smn:WrongProperty")
    if {term for term, _ in stale} != {smn["ExemptedButDefined"], smn["Gone"]}:
        errors.append(f"reported {sorted(curie(t) for t, _ in stale)} as stale, "
                      "expected smn:ExemptedButDefined and smn:Gone")
    graph.add((smn["Planted"], IAO_DEFINITION, Literal("Now defined.")))
    graph.add((smn["WrongProperty"], SKOS.definition, Literal("Now defined.")))
    del rows[smn["ExemptedButDefined"]], rows[smn["Gone"]]
    _, missing, stale = find_problems(graph, rows)
    if missing or stale:
        errors.append("still reported problems after the fixture's terms were defined "
                      "and its stale rows deleted")
    return errors


def main() -> int:
    errors = self_test()
    if errors:
        print("The term definition check failed its own fixture, so its verdict "
              "on the ontology cannot be trusted:")
        for error in errors:
            print(f"  {error}")
        return 1

    graph = Graph()
    typed_in: dict[URIRef, list[str]] = {}
    for path in sorted(MODULES.glob("*.ttl")):
        module = Graph().parse(path, format="turtle")
        for term in local_terms(module):
            typed_in.setdefault(term, []).append(path.name)
        graph += module

    exemptions = EXEMPTIONS.relative_to(ROOT).as_posix()
    rows, malformed = read_exemptions(EXEMPTIONS)
    terms, missing, stale = find_problems(graph, rows)

    if not terms:
        print(f"Found no local terms in {MODULES.relative_to(ROOT).as_posix()}/. "
              "The check is not reading what it thinks it is, so it cannot pass.")
        return 1

    if missing or stale or malformed:
        print("Term definition check failed.")
        if missing:
            print(f"\nLocal terms with no definition and no row in {exemptions}: {len(missing)}")
            print("Write the definition. If it cannot be written yet, add a row naming "
                  "the queue item that will write it.")
            for term in missing:
                where = PROPERTY_CURIES[definition_property(skos_term=terms[term])]
                print(f"  {curie(term)} ({', '.join(typed_in[term])}) needs {where}")
        if stale:
            print(f"\nStale rows in {exemptions}: {len(stale)}")
            print("A row retires with its term, so delete it.")
            for term, reason in stale:
                line, queue_id = rows[term]
                print(f"  line {line}: {curie(term)} (retired by {queue_id}) {reason}")
        if malformed:
            print(f"\nMalformed rows in {exemptions}: {len(malformed)}")
            for problem in malformed:
                print(f"  {problem}")
        return 1

    by_item = Counter(queue_id for _, queue_id in rows.values())
    counts = ", ".join(f"{queue_id}: {n}" for queue_id, n in sorted(by_item.items()))
    print(f"Term definitions verified: {len(terms)} local terms in ontology/modules/, "
          f"{len(terms) - len(rows)} defined, {len(rows)} exempted by {exemptions}"
          + (f" ({counts})." if counts else "."))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
