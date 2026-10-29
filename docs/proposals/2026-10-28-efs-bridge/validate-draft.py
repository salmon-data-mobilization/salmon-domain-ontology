"""Check this isolated proposal; do not rebuild or change the ontology."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
from urllib.parse import unquote, urlparse

from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import DCTERMS, OWL, RDF, RDFS, SKOS

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SMN = Namespace("https://w3id.org/smn/")
IOP = Namespace("https://w3id.org/iadopt/ont/")
SOSA = Namespace("http://www.w3.org/ns/sosa/")
SMNV = Namespace("https://w3id.org/smn/views/salmon-data-metamodel#")
BRIDGE = Namespace("https://example.org/proposal/psc-efs-bridge/")
EX = Namespace("https://example.org/proposal/psc-efs-fixture/")
QUDT = Namespace("http://qudt.org/schema/qudt/")
PSC = URIRef("https://w3id.org/psc/vocab/concept/PSC-CV-000035")
SEX_VERSION = URIRef("http://vocab.nerc.ac.uk/collection/S10/current/S102/2/")
EXPECTED = "Effective Female Spawners (EFS): An estimate of female spawner abundance in the brood year (as opposed to the more traditional total of male and female spawners), which is further adjusted downward by the proportion of eggs that were not spawned, as determined by sampling on the spawning grounds."
MODEL_FILES = ("shared-terms.ttl", "psc-cv-000035-bridge.ttl", "example-observations.ttl")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def check_model(graph: Graph) -> None:
    require(set(graph.objects(PSC, SKOS.definition)) == {Literal(EXPECTED, lang="en")},
            "Original PSC definition changed")
    require((PSC, RDF.type, IOP.Variable) in graph, "Missing variable-instance typing")
    for term in graph.subjects(RDF.type, OWL.Class):
        require((term, RDF.type, SKOS.Concept) not in graph,
                "An IRI is both an OWL class and a SKOS concept")
    require((PSC, RDF.type, OWL.Class) not in graph, "PSC variable became an OWL class")
    require(set(graph.objects(PSC, IOP.hasProperty)) == {BRIDGE.abundanceCharacteristic},
            "Expected exactly one property-description instance")
    require((BRIDGE.abundanceCharacteristic, RDF.type, SMN.Abundance) in graph
            and (BRIDGE.abundanceCharacteristic, RDF.type, IOP.Property) in graph,
            "Abundance class and variable property-description instance were confused")
    require(set(graph.objects(PSC, IOP.hasObjectOfInterest)) == {BRIDGE.productionStockDescription},
            "Expected exactly one entity-description instance")
    require((BRIDGE.productionStockDescription, RDF.type, SMN.Stock) in graph,
            "Missing stock entity role")
    require(set(graph.objects(PSC, IOP.hasConstraint)) == {
        BRIDGE.femaleScope, SMN.SpawnerStageContext, SMN.BroodYearBasis},
        "Female, stage and year-basis scope must stay explicit")
    require((BRIDGE.femaleScope, IOP.constrains, BRIDGE.productionStockDescription) in graph,
            "Female constraint has no contextual entity target")
    require((BRIDGE.femaleScope, DCTERMS.source, SEX_VERSION) in graph,
            "Female scope must cite the pinned existing sex concept")
    require(not set(graph.objects(SEX_VERSION, IOP.constrains)),
            "Reusable NERC concept acquired a variable-specific target")
    for predicate in (SKOS.exactMatch, SKOS.closeMatch, SKOS.broadMatch,
                      SKOS.narrowMatch, SKOS.relatedMatch, OWL.equivalentClass,
                      OWL.equivalentProperty, OWL.sameAs):
        require(not list(graph.triples((None, predicate, None))),
                "Proposal must not assert an unreviewed equivalence or cross-kind match")
    require((SMN.UnspawnedEggAdjustment, RDF.type, SKOS.Concept) in graph
            and (SMN.UnspawnedEggAdjustment, RDF.type, SOSA.Procedure) in graph,
            "Adjustment must be a method concept and procedure")
    require((SMN.UnspawnedEggAdjustment, SKOS.inScheme, SMN.MethodScheme) in graph,
            "Adjustment is not in the shared method scheme")
    require((SMN.UnspawnedEggAdjustment, SKOS.broader, SMN.EnumerationMethod) not in graph,
            "Calculation was incorrectly classified as field enumeration")
    require((SMN.SpawnerAbundance, RDFS.subClassOf, SMN.ObservedRateOrAbundance) in graph,
            "Spawner abundance must be a result category")
    require((SMN.SpawnerAbundance, RDFS.subClassOf, SMN.Abundance) not in graph,
            "Result class was confused with the measured characteristic")
    require((EX.efsObservation, SOSA.usedProcedure, SMN.UnspawnedEggAdjustment) in graph,
            "Procedure must be linked from the observation")
    require((EX.efsObservation, SMNV.hasVariable, PSC) in graph,
            "Result lost the precise PSC variable identity")
    require((EX.femaleObservation, SMNV.hasVariable, EX.rawFemaleVariable) in graph,
            "Raw female abundance lost its separate variable identity")
    require(all((result, RDF.type, SMN.SpawnerAbundance) in graph
                for result in (EX.efsResult, EX.femaleResult)), "Missing spawner result typing")
    female = graph.value(EX.femaleResult, QUDT.numericValue).toPython()
    success = graph.value(EX.spawningSuccessResult, QUDT.numericValue).toPython()
    efs = graph.value(EX.efsResult, QUDT.numericValue).toPython()
    require(efs == female * success and efs != female,
            "Synthetic EFS must preserve partial spawning rather than copy the raw count")


def check_core_isolation() -> int:
    pending = [ROOT / "ontology/salmon-domain-ontology.ttl"]
    seen = set()
    while pending:
        path = pending.pop().resolve()
        require(HERE not in path.parents, "Proposal entered the normative import closure")
        if path in seen:
            continue
        seen.add(path)
        graph = Graph().parse(path)
        for imported in graph.objects(None, OWL.imports):
            parsed = urlparse(str(imported))
            if parsed.scheme == "file":
                pending.append(Path(unquote(parsed.path)))
            elif str(imported).startswith("https://w3id.org/smn/modules/"):
                pending.append(ROOT / "ontology/modules" / (parsed.path.rsplit("/", 1)[-1] + ".ttl"))
    return len(seen)


def main() -> None:
    graph = Graph()
    for name in MODEL_FILES:
        graph.parse(HERE / name)
    receipt = HERE / "evidence/nerc-s10-s102-v2.ttl"
    require(hashlib.sha256(receipt.read_bytes()).hexdigest()
            == "b0e884a4593d9791df61f8f1c7dacbe650c90a30637f9e3dbfc1fac6087d35ff",
            "NERC version-2 source receipt changed")
    source = Graph().parse(receipt)
    require((SEX_VERSION, RDF.type, SKOS.Concept) in source, "NERC source is not a SKOS concept")
    # CI need not clone the separately governed PSC repository. The expected
    # literal is always enforced above; compare authoring data as well when
    # the sibling checkout is available, and report which check was possible.
    psc_authoring = ROOT.parent / "psc-salmon-vocabularies/data/concepts.csv"
    if psc_authoring.is_file():
        with psc_authoring.open(newline="") as stream:
            current = next(row for row in csv.DictReader(stream) if row["concept_id"] == "PSC-CV-000035")
        require(current["definition_en"] == EXPECTED, "Local PSC authoring literal differs")
    check_model(graph)
    controls = []
    for name in ("definition_drift", "class_concept_punning", "raw_count_substitution"):
        mutated = Graph()
        mutated += graph
        if name == "definition_drift":
            mutated.set((PSC, SKOS.definition, Literal("Changed wording", lang="en")))
        elif name == "class_concept_punning":
            mutated.add((PSC, RDF.type, OWL.Class))
        else:
            mutated.set((EX.efsResult, QUDT.numericValue, Literal(100)))
        try:
            check_model(mutated)
        except ValueError:
            controls.append(name)
        else:
            raise ValueError(f"Negative control was not rejected: {name}")
    print(json.dumps({"ok": True, "model_triples": len(graph),
                      "source_triples": len(source), "core_local_files_checked": check_core_isolation(),
                      "psc_authoring_compared": psc_authoring.is_file(),
                      "negative_controls_rejected": controls,
                      "scope": "Structural and synthetic checks; no biological approval or exhaustive OWL reasoning"},
                     indent=2))


if __name__ == "__main__":
    main()
