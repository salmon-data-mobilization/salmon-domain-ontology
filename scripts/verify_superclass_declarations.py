#!/usr/bin/env python3
"""Fail when a superclass IRI asserted in modules is neither declared nor vendored.

The defect (hub queue B-143). A module may assert `smn:X rdfs:subClassOf ns:Y`
where nothing anywhere in this repository says what `ns:Y` is. Nothing in the
build noticed: `sosa:Property` sat under `smn:Characteristic` from 2026-08-10
to 2026-09-14, with the whole characteristic hierarchy hanging off an IRI that
SOSA does not publish, through every CI run in between.

**The reasoner is not this check and must never be offered as one.** ELK reads
an un-axiomatised IRI as a class about which nothing is known. Nothing is
entailed, nothing contradicts, the closure stays consistent, no class is
unsatisfiable, and `make verify-reasoner` passes. That is precisely how the
`sosa:Property` case survived a month of green builds. A reasoner answers "do
these axioms contradict each other"; this script answers "does this name refer
to anything", and no amount of reasoning turns the second question into the
first.

## What "declared" means here

An IRI is **declared** when some file in `ontology/modules/` or
`ontology/imports/` carries a class-declaration axiom for it: `rdf:type
owl:Class`, `rdf:type rdfs:Class`, or `rdf:type owl:DeprecatedClass`. Nothing
else counts, and one exclusion is the entire point: an IRI that appears only
as the *object* of an `rdfs:subClassOf` is not declared by that appearance.
That is the defect, not evidence against it.

Declarations are read from the union of `ontology/modules/` and
`ontology/imports/` because that is the set B-143 names — "declared in those
modules [or] present in a vendored import". A declaration stub in a module is
as good as a vendored file here; CONVENTIONS 5b rule 2 permits a bare stub
(`ex:Term a owl:Class .`) anywhere, so refusing to count one would contradict
the conventions this repository already enforces.

## What is checked

Every object of an `rdfs:subClassOf` triple in `ontology/modules/*.ttl`. The
three object kinds are handled explicitly rather than by falling through a
`URIRef` test:

- `URIRef` — a named superclass. Resolved against the declared set. This is
  the check.
- `BNode` — an anonymous class expression: `owl:Restriction`,
  `owl:intersectionOf` and the `rdf:List` nodes under it. It names no IRI, so
  there is nothing to resolve. Skipped, and **counted in the summary line** so
  that the skip is visible in every run rather than silent.
- `Literal` — malformed RDFS. Reported as its own failure class, because a
  literal is not a `URIRef` and would otherwise leave by the same door as a
  blank node.

## What is deliberately not checked, and why

- **Fillers inside anonymous class expressions.** `owl:someValuesFrom
  geosparql:Feature` in `02-observation-measurement.ttl` is an undeclared IRI
  in a restriction, not an asserted superclass. Widening to restriction
  fillers is a real check and a separate one; B-143 is scoped to superclasses.
- **`rdfs:domain`, `rdfs:range`, `rdfs:subPropertyOf`.** Same reason. The
  first run of this script found six undeclared IRIs in domain/range position,
  including the second half of the `sosa:Property` defect
  (`smn:characteristicFor rdfs:domain sosa:Property`). They are recorded in
  the B-143 hand-back rather than fixed or gated here.
- **Whether a declaration reaches the build that uses it.** This asks only
  whether the IRI is axiomatised anywhere in what smn ships or vendors. A
  per-closure variant — module 09's declaration does not reach module 02's
  build — is strictly stronger and is a different question from B-143's.

## Staged mode, and what ends it

`--staged` runs the same scan but treats the IRIs in `KNOWN_UNDECLARED` as
already-reported rather than as new failures. It exists because the gate would
otherwise arrive red over the modules as they stand, and a check that arrives
red teaches its first reader to weaken it.

Staged mode is not a mute button. It is fatal on three things:

1. The two-direction fixture below, in both modes. The fixture is what proves
   the gate works, so it is enforced from the day the gate lands, before the
   gate itself is. A staged check whose demonstration is also staged rots
   before it ever guards.
2. Any undeclared superclass IRI **not** in `KNOWN_UNDECLARED`. New breakage
   fails immediately; that is the protection the staged state still buys.
3. Any entry in `KNOWN_UNDECLARED` that is **no longer** undeclared. The
   baseline is required to shrink. This is what stops the staged state
   becoming permanent: when B-107 replaces `sosa:Property`, this script goes
   red until its entry is deleted, and the failure message says so and names
   the switch-on condition.

*Switch-on condition (dated 2026-09-15):* when `KNOWN_UNDECLARED` is empty,
delete it, `REASONS`, `--staged` and `main()`'s staged branch, and change the
`test` target in the Makefile from `verify-superclass-declarations-staged` to
`verify-superclass-declarations`. Individual entries are retired by the
conditions in `REASONS`, which every staged run prints. The last one to go will
be `sosa:Property` — hub item B-107, itself held behind smn pull request #27.

*Retirement of the whole script:* retires when an upstream gate run identically
by smn, gcdfo and the PSC vocabularies checks referential integrity of asserted
axioms across all three, so that this repo-local check is redundant rather than
load-bearing. Until then it stays: this repository publishes terms other
repositories re-serialize, and it is the only place the invariant is checked at
the source.
"""

from __future__ import annotations

import argparse
import re
from collections import defaultdict
from pathlib import Path

from rdflib import BNode, Graph, Literal, OWL, RDF, RDFS, URIRef

ROOT = Path(__file__).resolve().parents[1]
MODULE_DIR = ROOT / "ontology" / "modules"
IMPORT_DIR = ROOT / "ontology" / "imports"

# The class-declaration axioms this check accepts. owl:Class is the OWL 2 form;
# rdfs:Class is the RDFS form the vendored SOSA snapshot uses alongside it
# (`sosa:ObservableProperty a rdfs:Class, owl:Class`); owl:DeprecatedClass is
# the form a retired-but-still-referenced term carries.
DECLARATION_TYPES = {OWL.Class, RDFS.Class, OWL.DeprecatedClass}

# Built-in classes of the OWL and RDFS vocabularies. These are defined by the
# specifications rather than by anything this repository ships, so no file here
# declares them and none should. Exercised by the fixture below so the list is
# not untested.
# *Retires when:* the declared set is seeded from vendored copies of the OWL and
# RDFS vocabularies, at which point these resolve like any other IRI and this
# enumeration is deleted rather than maintained.
BUILTIN_CLASSES = {
    OWL.Thing,
    OWL.Nothing,
    RDFS.Resource,
    RDFS.Literal,
    RDFS.Datatype,
}

# The two shapes the first run found, each with the condition that retires it.
# Neither is an exemption: both are reported on every staged run.
REASONS = {
    "not-vendored": (
        "the namespace is not vendored under ontology/imports/ at all, and no "
        "module declares a stub for it. CONVENTIONS 5b rule 2 permits a bare "
        "declaration stub (`ex:Term a owl:Class .`) anywhere, so either a stub "
        "or a vendored import resolves this; which one is a modelling decision "
        "and is not B-143's to make, because B-143 is structural and carries "
        "no term ruling. RETIRES WHEN that decision is taken and the "
        "declaration lands."
    ),
    "B-107": (
        "hub item B-107, the defect B-143 was cut from. This is the one entry "
        "whose namespace IS vendored (ontology/imports/sosa.ttl): the IRI is "
        "simply absent from it, because SOSA publishes "
        "sosa:ObservableProperty, which the vendored file does declare. A "
        "wrong term, not a missing import, so vendoring would not fix it. "
        "RETIRES WHEN B-107 lands the replacement; B-107 is itself held behind "
        "smn pull request #27, which edits the same module and regenerates the "
        "docs artifacts."
    ),
}

# Baseline: every undeclared superclass IRI in ontology/modules/ as measured on
# 2026-09-15 at d45f8f7, mapped to its reason in REASONS. Staged mode reports
# these without failing; it fails on anything not listed, and on any listed
# entry that has since been declared.
KNOWN_UNDECLARED = {
    "http://purl.obolibrary.org/obo/BFO_0000015": "not-vendored",
    "http://purl.obolibrary.org/obo/IAO_0000030": "not-vendored",
    "http://purl.obolibrary.org/obo/IAO_0000109": "not-vendored",
    "http://purl.obolibrary.org/obo/NCBITaxon_8015": "not-vendored",
    "http://purl.obolibrary.org/obo/NCBITaxon_8018": "not-vendored",
    "http://rs.tdwg.org/dwc/terms/Event": "not-vendored",
    "http://rs.tdwg.org/dwc/terms/Organism": "not-vendored",
    "http://www.opengis.net/ont/geosparql#Feature": "not-vendored",
    "http://www.w3.org/ns/sosa/Property": "B-107",
}


def collect_declared(paths: list[Path]) -> set[URIRef]:
    """IRIs carrying a class-declaration axiom in any of `paths`."""
    declared = set()
    for path in paths:
        graph = Graph()
        graph.parse(path, format="turtle")
        for declaration_type in sorted(DECLARATION_TYPES, key=str):
            for subject in graph.subjects(RDF.type, declaration_type):
                if isinstance(subject, URIRef):
                    declared.add(subject)
    return declared


def _locate(path: Path, obj: URIRef) -> str:
    """Best-effort source lines for `rdfs:subClassOf <obj>` in one file.

    rdflib carries no line information, so this re-reads the file and matches
    on the tokens Turtle could have written the object as: the full IRI in
    angle brackets, or a prefixed name built from a binding the file itself
    declares. Only text to the right of `subClassOf` is searched, so the same
    IRI in subject position on another axiom is not picked up. Reported per
    file rather than per subject, because attributing a line to one of several
    subjects sharing a superclass would be false precision; it degrades to no
    line reference rather than guessing.
    """
    text = path.read_text(encoding="utf-8")
    tokens = [f"<{obj}>"]
    for prefix, namespace in re.findall(
        r"^@prefix\s+([A-Za-z][\w.-]*)?:\s+<([^>]*)>\s*\.", text, flags=re.MULTILINE
    ):
        if namespace and str(obj).startswith(namespace):
            tokens.append(f"{prefix}:{str(obj)[len(namespace):]}")
    hits = []
    for number, line in enumerate(text.splitlines(), start=1):
        _, marker, tail = line.partition("subClassOf")
        if marker and any(token in tail for token in tokens):
            hits.append(str(number))
    return f":{','.join(hits)}" if hits else ""


def scan(module_paths: list[Path], declared: set[URIRef]) -> tuple[dict, list, int]:
    """Undeclared named superclasses, literal superclasses, and the bnode count.

    Returns (undeclared, malformed, anonymous_count) where `undeclared` maps an
    IRI to the sorted list of rendered places asserting it, one per file.
    """
    by_iri = defaultdict(lambda: defaultdict(set))
    malformed = []
    anonymous = 0
    for path in module_paths:
        graph = Graph()
        graph.parse(path, format="turtle")
        where = path.relative_to(ROOT).as_posix()
        for subject, _, obj in graph.triples((None, RDFS.subClassOf, None)):
            if isinstance(obj, BNode):
                # Anonymous class expression: restriction, intersection/union,
                # or an rdf:List node under one. Names no IRI; nothing to
                # resolve. Counted, not silently dropped.
                anonymous += 1
                continue
            if isinstance(obj, Literal):
                malformed.append(
                    f"{where}: literal in superclass position — "
                    f"{subject} rdfs:subClassOf {obj!r}"
                )
                continue
            if not isinstance(obj, URIRef):
                malformed.append(
                    f"{where}: unhandled superclass node kind "
                    f"{type(obj).__name__} — {subject} rdfs:subClassOf {obj}"
                )
                continue
            if obj in BUILTIN_CLASSES or obj in declared:
                continue
            by_iri[str(obj)][path].add(str(subject))

    undeclared = {}
    for iri, by_path in by_iri.items():
        undeclared[iri] = [
            f"{path.relative_to(ROOT).as_posix()}{_locate(path, URIRef(iri))}"
            f" — asserted on {', '.join(sorted(subjects))}"
            for path, subjects in sorted(by_path.items(), key=lambda kv: str(kv[0]))
        ]
    return undeclared, malformed, anonymous


# --- Two-direction fixture ---------------------------------------------------
#
# The demonstration B-143 asks for, run on every invocation in both modes: a
# module asserting a superclass in a foreign namespace that nothing declares
# turns the gate red, and removing that one assertion turns it green. The two
# fixtures differ by exactly the FOREIGN_ASSERTION line and nothing else, so a
# green second direction cannot be an artefact of some other edit.

_FIXTURE_PREAMBLE = """
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix ex: <http://example.org/fixture/> .
@prefix foreign: <http://example.org/nothing-declares-this/> .

ex:Declared a owl:Class .
ex:AlsoDeclared a owl:Class ; rdfs:subClassOf ex:Declared .

# A built-in superclass must not be reported (exercises BUILTIN_CLASSES).
ex:UnderThing a owl:Class ; rdfs:subClassOf owl:Thing .

# Anonymous class expressions must not be reported: a restriction, and an
# intersection whose rdf:List nodes are blank too.
ex:Restricted a owl:Class ; rdfs:subClassOf
  [ a owl:Restriction ; owl:onProperty ex:p ; owl:someValuesFrom ex:Declared ] .
ex:Intersected a owl:Class ; rdfs:subClassOf
  [ a owl:Class ; owl:intersectionOf ( ex:Declared ex:AlsoDeclared ) ] .

# The definitional trap: appearing only as the OBJECT of rdfs:subClassOf is not
# a declaration. ex:ObjectOnly is never typed, so asserting it as a superclass
# must be reported.
ex:Orphan a owl:Class ; rdfs:subClassOf ex:ObjectOnly .
"""

FOREIGN_ASSERTION = "ex:Broken a owl:Class ; rdfs:subClassOf foreign:Undeclared .\n"

FIXTURE_RED = _FIXTURE_PREAMBLE + FOREIGN_ASSERTION
FIXTURE_GREEN = _FIXTURE_PREAMBLE

FIXTURE_FOREIGN_IRI = "http://example.org/nothing-declares-this/Undeclared"
FIXTURE_OBJECT_ONLY_IRI = "http://example.org/fixture/ObjectOnly"


def _scan_fixture(turtle: str) -> tuple[set, list, int]:
    """Run the same scan logic over an in-memory fixture module."""
    graph = Graph()
    graph.parse(data=turtle, format="turtle")
    declared = {s for s in graph.subjects(RDF.type, OWL.Class) if isinstance(s, URIRef)}
    undeclared = set()
    malformed = []
    anonymous = 0
    for subject, _, obj in graph.triples((None, RDFS.subClassOf, None)):
        if isinstance(obj, BNode):
            anonymous += 1
            continue
        if isinstance(obj, Literal):
            malformed.append(str(obj))
            continue
        if obj in BUILTIN_CLASSES or obj in declared:
            continue
        undeclared.add(str(obj))
    return undeclared, malformed, anonymous


def self_test() -> list[str]:
    """Both directions, plus the node kinds. Fatal in every mode."""
    failures = []

    red, red_malformed, red_anonymous = _scan_fixture(FIXTURE_RED)
    green, _, green_anonymous = _scan_fixture(FIXTURE_GREEN)

    # Direction 1: the foreign undeclared superclass turns the gate red.
    if FIXTURE_FOREIGN_IRI not in red:
        failures.append(
            "fixture direction 1: the foreign undeclared superclass "
            f"{FIXTURE_FOREIGN_IRI} was NOT reported — the gate does not catch "
            "the defect it exists for"
        )
    # Direction 2: removing that one line turns the gate green for it.
    if FIXTURE_FOREIGN_IRI in green:
        failures.append(
            "fixture direction 2: removing the assertion did not clear "
            f"{FIXTURE_FOREIGN_IRI} — the gate reports an IRI the module no "
            "longer asserts"
        )
    # The two fixtures differ by exactly that one line.
    if FIXTURE_RED != FIXTURE_GREEN + FOREIGN_ASSERTION:
        failures.append(
            "fixture directions differ by more than the foreign assertion, so "
            "a green direction 2 would not be attributable to removing it"
        )
    # Object-only appearance is not a declaration, in both directions.
    for name, result in (("red", red), ("green", green)):
        if FIXTURE_OBJECT_ONLY_IRI not in result:
            failures.append(
                f"fixture ({name}): an IRI appearing only as the object of "
                "rdfs:subClassOf was treated as declared — that is the "
                "definition this check turns on"
            )
    # Anonymous expressions and built-ins are skipped, not reported.
    if red_anonymous != 2 or green_anonymous != 2:
        failures.append(
            "fixture: expected 2 anonymous superclass expressions (a "
            f"restriction and an intersection), saw red={red_anonymous} "
            f"green={green_anonymous}"
        )
    if any("owl#Thing" in iri for iri in red | green):
        failures.append("fixture: owl:Thing was reported; BUILTIN_CLASSES is not applied")
    if red_malformed:
        failures.append(f"fixture: unexpected malformed superclasses {red_malformed}")
    # Exactly two undeclared IRIs in red, one in green: no accidental extras.
    if red != {FIXTURE_FOREIGN_IRI, FIXTURE_OBJECT_ONLY_IRI}:
        failures.append(f"fixture (red): unexpected result set {sorted(red)}")
    if green != {FIXTURE_OBJECT_ONLY_IRI}:
        failures.append(f"fixture (green): unexpected result set {sorted(green)}")

    # The baseline is only legible if every entry resolves to a reason that
    # states what retires it, and only honest if no reason outlives its last
    # entry. Both directions, so neither half rots unnoticed.
    for iri, key in sorted(KNOWN_UNDECLARED.items()):
        if key not in REASONS:
            failures.append(
                f"baseline entry {iri} cites reason {key!r}, which is not in "
                "REASONS, so nothing records what would retire it"
            )
    for key in sorted(set(REASONS) - set(KNOWN_UNDECLARED.values())):
        failures.append(
            f"REASONS entry {key!r} is cited by no baseline entry; delete it "
            "rather than leaving a retirement condition for nothing"
        )

    return failures


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--staged",
        action="store_true",
        help=(
            "report the IRIs in KNOWN_UNDECLARED without failing on them. "
            "Still fatal on the fixture, on any IRI not in that baseline, and "
            "on any baseline entry that has since been declared."
        ),
    )
    args = parser.parse_args()

    fixture_failures = self_test()
    if fixture_failures:
        print("The two-direction fixture failed. The gate is not working:")
        for failure in fixture_failures:
            print(f"  {failure}")
        raise SystemExit(1)

    module_paths = sorted(MODULE_DIR.glob("*.ttl"))
    import_paths = sorted(IMPORT_DIR.glob("*.ttl"))
    declared = collect_declared(module_paths + import_paths)
    undeclared, malformed, anonymous = scan(module_paths, declared)

    failures = list(malformed)
    baselined = {}
    for iri in sorted(undeclared):
        rendered = "\n".join(f"      {p}" for p in undeclared[iri])
        if args.staged and iri in KNOWN_UNDECLARED:
            baselined[iri] = rendered
            continue
        failures.append(
            f"undeclared superclass IRI {iri}\n{rendered}\n"
            "      nothing in ontology/modules/ or ontology/imports/ declares "
            "it as a class"
        )

    if args.staged:
        stale = sorted(set(KNOWN_UNDECLARED) - set(undeclared))
        for iri in stale:
            failures.append(
                f"stale baseline entry {iri}: it is declared now, so delete its "
                "KNOWN_UNDECLARED entry in this file. When the baseline is "
                "empty, delete it with --staged and switch the Makefile's test "
                "target from verify-superclass-declarations-staged to "
                "verify-superclass-declarations."
            )

    if failures:
        for failure in failures:
            print(failure)
        raise SystemExit(1)

    print(
        f"Superclass declarations verified over {len(module_paths)} modules "
        f"against {len(declared)} declarations "
        f"({len(import_paths)} vendored imports; {anonymous} anonymous "
        "superclass expressions skipped by design)."
    )
    if baselined:
        print(
            f"\nSTAGED (hub item B-143): {len(baselined)} known undeclared "
            "superclass IRIs are reported but not failing. This is a recorded "
            "backlog, not an accepted state:"
        )
        for iri in sorted(baselined):
            print(f"  [{KNOWN_UNDECLARED[iri]}] {iri}")
            print(f"{baselined[iri]}")
        print("\n  Reasons, each carrying what retires it:")
        for key in sorted({KNOWN_UNDECLARED[iri] for iri in baselined}):
            print(f"    [{key}] {REASONS[key]}")
        print(
            "\n  New undeclared superclasses still fail, in this mode too. "
            "When the list above is empty the gate switches on; the exact "
            "condition is in this script's docstring."
        )


if __name__ == "__main__":
    main()
