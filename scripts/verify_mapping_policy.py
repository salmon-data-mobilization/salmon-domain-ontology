#!/usr/bin/env python3
"""Enforce CONVENTIONS section 5b mapping placement and coherence rules.

Six checks, all CI-fatal:

1. Foreign-subject statements outside alignment modules: a subject smn does
   not own may carry only documentation annotations (comment/seeAlso/
   isDefinedBy) and bare declaration stubs. Everything else — Tier-1 axioms
   AND instance-level property assertions — is confined to the alignment
   modules; the annotated NCBITaxon MIREOT mirror in module 02 is the one
   explicit exception.
2. One strongest mapping per subject-object pair, checked two ways: within
   every single module/view file (covers 08/09, alignment-research, views —
   the promotion-staging exception is cross-module by definition and can
   never apply within one file), and across the default build spine (which
   excludes alignment-research, the documented staging exception).
3. Reasoner-clean typing invariant: no IRI in the flattened build may be
   typed both owl:Class and skos:Concept (the dual-representation rule).
4. No lexical labels on foreign-namespace subjects, anywhere in smn's
   sources — alignment modules included. Upstream owns its own labels
   (CONVENTIONS 5b rule 3, "import upstream alignments; do not restate
   them"); smn may declare a foreign term and annotate it with prose, but
   restating its name is how a mirror drifts out of agreement with the
   thing it mirrors.
5. Label unambiguity across each build closure: at most one rdfs:label and
   one skos:prefLabel per subject per language tag, and no rdfs:label that
   disagrees with its subject's skos:prefLabel by case or whitespace alone.
6. No SKOS semantic relation in the published default closure may have an
   owl:Class at either end. All twelve predicates below entail skos:Concept
   typing through skos:semanticRelation (SKOS Reference S19-S22, S39-S42).
   The research and case-study overlays are separate editorial surfaces.

Checks 4 and 5 were added 2026-08-16. A label-consuming renderer given two
equally-valid English labels for one subject picks one arbitrarily, so its
output changes between runs with no semantic change behind it — that is what
OWL2VOWL did to dfo-salmon-ontology's docs pipeline, which had to pin to
skos:prefLabel to work around it (its ADR-007). Check 4 stops smn creating
that ambiguity in someone else's terms; check 5 stops it appearing in smn's
own merged artifacts from any direction.

Retirement condition for checks 4 and 5: retire them when label uniqueness is
enforced for the whole ecosystem by a shared upstream gate — a SHACL shape or
ROBOT report run identically by smn, gcdfo, and the PSC vocabularies — so that
this repo-local restatement is redundant rather than load-bearing. Until then
they stay: this repo publishes terms other repos re-serialize, and it is the
only place the invariant is checked at the source.

Retirement condition for check 6's default-only scope: expand it once the
research and case-study rows have been reviewed and repaired. Retire the local
check itself only when a shared ecosystem gate enforces the same invariant on
all published ontology builds and verifies their import closure.
"""

import re
import tempfile
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path

from rdflib import Graph, RDF, RDFS, OWL, URIRef
from rdflib.namespace import SKOS

ROOT = Path(__file__).resolve().parents[1]
SMN = "https://w3id.org/smn"
CATALOG = ROOT / "ontology" / "catalog-v001.xml"
CATALOG_NS = "{urn:oasis:names:tc:entity:xmlns:xml:catalog}"
# The two published build entrypoints. Both are checked: alignment-research
# is not in the default build, so a defect confined to it is invisible in the
# flat artifact — which is exactly where the 2026-08-16 SOSA label duplicates
# had been hiding since the 46a4a51 bootstrap.
DEFAULT_BUILD_ROOT = Path("ontology") / "salmon-domain-ontology.ttl"
BUILD_ROOTS = [
    DEFAULT_BUILD_ROOT,
    Path("ontology") / "salmon-domain-ontology-research.ttl",
]
LEXICAL_LABEL_PREDICATES = (RDFS.label, SKOS.prefLabel, SKOS.altLabel)
ALIGNMENT_MODULES = {
    "alignment-main.ttl",
    "alignment-upper.ttl",
    "alignment-research.ttl",
}
SPINE = [
    "01-entity-systematics.ttl",
    "02-observation-measurement.ttl",
    "03-assessment-benchmarks.ttl",
    "04-management-governance.ttl",
    "05-provenance-quality.ttl",
    "06-data-interoperability.ttl",
    "07-controlled-vocabularies.ttl",
    "alignment-main.ttl",
    "alignment-upper.ttl",
]
TIER1 = {
    RDFS.subClassOf,
    RDFS.subPropertyOf,
    OWL.equivalentClass,
    OWL.equivalentProperty,
    OWL.sameAs,
}
TIER2 = {SKOS.exactMatch}
TIER3 = {SKOS.closeMatch, SKOS.broadMatch, SKOS.narrowMatch, SKOS.relatedMatch}
# The transitive sub-property closure of skos:semanticRelation, including the
# root property itself. This set is about SKOS typing, not mapping strength:
# skos:broader on an owl:Class is the same kind of pun as skos:closeMatch.
SKOS_SEMANTIC_RELATIONS = frozenset({
    SKOS.semanticRelation,
    SKOS.broaderTransitive,
    SKOS.narrowerTransitive,
    SKOS.broader,
    SKOS.narrower,
    SKOS.related,
    SKOS.mappingRelation,
    SKOS.closeMatch,
    SKOS.exactMatch,
    SKOS.broadMatch,
    SKOS.narrowMatch,
    SKOS.relatedMatch,
})


# Predicates a foreign-namespace subject may carry outside alignment
# modules: declaration stubs and prose annotations only.
# Everything else — Tier-1 axioms AND instance-level property assertions
# (the old `sosa:FeatureOfInterest sosa:hasSample sosa:Sample` class of
# mistake) — must live in an alignment module (CONVENTIONS 5b rule 2).
FOREIGN_ALLOWED_PREDICATES = {
    RDFS.comment,
    RDFS.seeAlso,
    RDFS.isDefinedBy,
}
FOREIGN_ALLOWED_TYPE_OBJECTS = {
    OWL.Class,
    OWL.ObjectProperty,
    OWL.DatatypeProperty,
    OWL.AnnotationProperty,
    OWL.NamedIndividual,
    OWL.Ontology,
}


def check_foreign_subjects() -> list:
    failures = []
    paths = sorted((ROOT / "ontology" / "modules").glob("*.ttl")) + sorted(
        (ROOT / "ontology" / "views").glob("*.ttl")
    )
    for path in paths:
        if path.name in ALIGNMENT_MODULES:
            continue
        graph = Graph()
        graph.parse(path, format="turtle")
        for subject, predicate, obj in graph:
            if not isinstance(subject, URIRef) or str(subject).startswith(SMN):
                continue
            if predicate in FOREIGN_ALLOWED_PREDICATES:
                continue
            if predicate in LEXICAL_LABEL_PREDICATES:
                continue  # delegated to check_foreign_subject_labels(), which
                # covers alignment modules too — reporting here as well would
                # print two failures for one defect.
            if predicate == RDF.type and obj in FOREIGN_ALLOWED_TYPE_OBJECTS:
                continue  # bare declaration stub
            if path.name == "02-observation-measurement.ttl" and "NCBITaxon" in str(subject):
                continue  # annotated MIREOT mirror of the upstream taxon hierarchy
            failures.append(
                f"{path.relative_to(ROOT)}: foreign-subject statement "
                f"{subject.n3(graph.namespace_manager)} "
                f"{predicate.n3(graph.namespace_manager)} "
                f"{obj.n3(graph.namespace_manager)}"
            )
    return failures


def _pair_tiers(graph: Graph) -> dict:
    tiers_by_pair = defaultdict(set)
    for subject, predicate, obj in graph:
        if not (isinstance(subject, URIRef) and isinstance(obj, URIRef)):
            continue
        if predicate in TIER1:
            tiers_by_pair[(subject, obj)].add("1")
        elif predicate in TIER2:
            tiers_by_pair[(subject, obj)].add("2")
        elif predicate in TIER3:
            tiers_by_pair[(subject, obj)].add("3")
    return tiers_by_pair


def check_tier_mixing() -> list:
    failures = []
    # (a) No pair mixes tiers WITHIN any single module or view file — this
    # covers 08/09, alignment-research, and the views, where the
    # promotion-staging exception (a cross-module pattern by definition)
    # can never apply.
    all_paths = sorted((ROOT / "ontology" / "modules").glob("*.ttl")) + sorted(
        (ROOT / "ontology" / "views").glob("*.ttl")
    )
    for path in all_paths:
        graph = Graph()
        graph.parse(path, format="turtle")
        for (subject, obj), tiers in sorted(_pair_tiers(graph).items()):
            if len(tiers) > 1:
                failures.append(
                    f"{path.relative_to(ROOT)}: tier-mixed pair within one "
                    f"module (tiers {'/'.join(sorted(tiers))}): {subject} -> {obj}"
                )
    # (b) No pair mixes tiers across the default build spine (which excludes
    # alignment-research — the documented promotion-staging exception).
    graph = Graph()
    for name in SPINE:
        graph.parse(ROOT / "ontology" / "modules" / name, format="turtle")
    for (subject, obj), tiers in sorted(_pair_tiers(graph).items()):
        if len(tiers) > 1:
            failures.append(
                f"tier-mixed pair across the default spine "
                f"(tiers {'/'.join(sorted(tiers))}): {subject} -> {obj}"
            )
    return failures


def check_dual_typing() -> list:
    graph = Graph()
    graph.parse(ROOT / "salmon-domain-ontology.ttl", format="turtle")
    classes = set(graph.subjects(RDF.type, OWL.Class))
    concepts = set(graph.subjects(RDF.type, SKOS.Concept))
    return [
        f"IRI typed both owl:Class and skos:Concept: {iri}"
        for iri in sorted(str(x) for x in classes & concepts if isinstance(x, URIRef))
    ]


def _class_semantic_relation_failures(graph: Graph, source: str) -> list[str]:
    """Find asserted SKOS relations that imply an OWL class is a concept."""
    classes = set(graph.subjects(RDF.type, OWL.Class))
    return [
        f"{source}: SKOS semantic relation on owl:Class: "
        f"{subject} {predicate} {obj}"
        for subject, predicate, obj in sorted(graph, key=lambda triple: tuple(map(str, triple)))
        if predicate in SKOS_SEMANTIC_RELATIONS
        and (subject in classes or obj in classes)
    ]


def check_class_semantic_relations() -> list[str]:
    # Only the default root is the published shared ontology. The research
    # and case-study overlays carry additional unresolved mappings and are
    # outside this B-147 guard until their separate alignment review.
    root = DEFAULT_BUILD_ROOT
    try:
        graph = _import_closure(ROOT / root, require_resolved_imports=True)
    except (FileNotFoundError, ValueError) as error:
        return [f"{root}: {error}"]
    return _class_semantic_relation_failures(graph, str(root))


def self_test_class_semantic_relations() -> None:
    """Each of the twelve SKOS predicates must fail at both class positions."""
    if len(SKOS_SEMANTIC_RELATIONS) != 12:
        raise AssertionError("SKOS pun detector does not cover twelve relations")
    class_iri = URIRef("https://example.org/Class")
    concept_iri = URIRef("https://example.org/Concept")
    for predicate in SKOS_SEMANTIC_RELATIONS:
        graph = Graph()
        graph.add((class_iri, RDF.type, OWL.Class))
        graph.add((concept_iri, RDF.type, SKOS.Concept))
        graph.add((class_iri, predicate, concept_iri))
        graph.add((concept_iri, predicate, class_iri))
        failures = _class_semantic_relation_failures(graph, "self-test")
        if len(failures) != 2:
            raise AssertionError(f"SKOS pun detector missed {predicate}")
        graph.remove((class_iri, predicate, concept_iri))
        graph.remove((concept_iri, predicate, class_iri))
        graph.add((concept_iri, predicate, concept_iri))
        if _class_semantic_relation_failures(graph, "self-test"):
            raise AssertionError(f"SKOS pun detector rejected concept relation {predicate}")
    # A missing import can hide the class declaration that makes a relation
    # unsafe, so a clean result requires proving that the catalog reached it.
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory) / "missing-import.ttl"
        root.write_text(
            "<https://example.org/root> a <http://www.w3.org/2002/07/owl#Ontology> ; "
            "<http://www.w3.org/2002/07/owl#imports> <https://example.org/missing> .",
            encoding="utf-8",
        )
        try:
            _import_closure(root, require_resolved_imports=True)
        except ValueError:
            pass
        else:
            raise AssertionError("SKOS pun detector ignored an unresolved import")


def check_foreign_subject_labels() -> list:
    """No smn source may name a term it does not own (CONVENTIONS 5b rule 3).

    Unlike check_foreign_subjects() this covers the alignment modules, because
    they are precisely where foreign subjects are allowed to appear — and so
    the only place a foreign label can hide. Declaring the term and annotating
    it with prose stays legal; only the lexical predicates are refused.
    """
    failures = []
    paths = sorted((ROOT / "ontology" / "modules").glob("*.ttl")) + sorted(
        (ROOT / "ontology" / "views").glob("*.ttl")
    )
    for path in paths:
        graph = Graph()
        graph.parse(path, format="turtle")
        for predicate in LEXICAL_LABEL_PREDICATES:
            for subject, _, obj in sorted(graph.triples((None, predicate, None)), key=str):
                if not isinstance(subject, URIRef) or str(subject).startswith(SMN):
                    continue
                failures.append(
                    f"{path.relative_to(ROOT)}: label on a foreign-namespace subject "
                    f"(upstream owns its own labels; declare the term, do not rename it): "
                    f"{subject.n3(graph.namespace_manager)} "
                    f"{predicate.n3(graph.namespace_manager)} {str(obj)!r}"
                    f"@{getattr(obj, 'language', None)}"
                )
    return failures


def _catalog_index() -> dict:
    """Map ontology IRI -> local file, from the catalog ROBOT itself resolves.

    Reusing the catalog rather than re-deriving the mapping keeps this check
    honest about what the reasoner gate actually merges, vendored upstream
    imports included.
    """
    index = {}
    for entry in ET.parse(CATALOG).getroot().iter(f"{CATALOG_NS}uri"):
        index[entry.get("name")] = (CATALOG.parent / entry.get("uri")).resolve()
    return index


def _import_closure(root_path: Path, *, require_resolved_imports: bool = False) -> Graph:
    index = _catalog_index()
    graph = Graph()
    seen = set()

    def visit(path: Path) -> None:
        path = path.resolve()
        if path in seen:
            return
        if not path.exists():
            if require_resolved_imports:
                raise FileNotFoundError(f"ontology import file does not exist: {path}")
            return
        seen.add(path)
        local = Graph()
        local.parse(path, format="turtle")
        for triple in local:
            graph.add(triple)
        for imported in sorted(local.objects(None, OWL.imports), key=str):
            target = index.get(str(imported))
            if target is None:
                if require_resolved_imports:
                    raise ValueError(f"unresolved owl:imports {imported} in {path}")
                continue
            visit(target)

    visit(root_path)
    return graph


def _collapse(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip().casefold()


def check_label_unambiguity() -> list:
    """One name per subject per language, in every build closure.

    Two equally-valid labels for one subject leave a renderer to choose, and
    nothing makes it choose the same way twice.
    """
    failures = []
    for root in BUILD_ROOTS:
        graph = _import_closure(ROOT / root)
        for predicate in (RDFS.label, SKOS.prefLabel):
            by_subject_language = defaultdict(set)
            for subject, _, obj in graph.triples((None, predicate, None)):
                by_subject_language[(subject, getattr(obj, "language", None))].add(str(obj))
            for (subject, language), values in sorted(
                by_subject_language.items(), key=lambda item: str(item[0][0])
            ):
                if len(values) > 1:
                    rendered = ", ".join(repr(v) for v in sorted(values))
                    failures.append(
                        f"{root}: {subject} has {len(values)} "
                        f"{predicate.n3(graph.namespace_manager)} values "
                        f"in @{language}: {rendered}"
                    )
        for subject in sorted(
            set(graph.subjects(RDFS.label, None)) & set(graph.subjects(SKOS.prefLabel, None)),
            key=str,
        ):
            labels = {str(o) for o in graph.objects(subject, RDFS.label)}
            preferred = {str(o) for o in graph.objects(subject, SKOS.prefLabel)}
            for label in sorted(labels):
                for pref in sorted(preferred):
                    if label != pref and _collapse(label) == _collapse(pref):
                        failures.append(
                            f"{root}: {subject} rdfs:label {label!r} differs from "
                            f"skos:prefLabel {pref!r} by case or whitespace only"
                        )
    return failures


def main() -> None:
    self_test_class_semantic_relations()
    failures = (
        check_foreign_subjects()
        + check_tier_mixing()
        + check_dual_typing()
        + check_foreign_subject_labels()
        + check_label_unambiguity()
        + check_class_semantic_relations()
    )
    if failures:
        for failure in failures:
            print(failure)
        raise SystemExit(1)
    print("Mapping policy verified: no foreign-subject axioms outside alignment "
          "modules, no tier-mixed pairs in the default spine, no dual-typed IRIs, "
          "no labels on foreign-namespace subjects, one label per subject per "
          "language in every build closure, no SKOS semantic relation on an "
          "OWL class in the default closure.")


if __name__ == "__main__":
    main()
