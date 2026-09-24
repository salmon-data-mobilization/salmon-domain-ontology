#!/usr/bin/env python3
"""Verify the shared year, age, abundance, and example modeling contract."""

from __future__ import annotations

import csv
from pathlib import Path

from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import OWL, RDF, RDFS, SKOS, XSD

from verify_term_definitions import has_definition


SMN = Namespace("https://w3id.org/smn/")
GCDFO = Namespace("https://w3id.org/gcdfo/salmon#")
ODO = Namespace("http://purl.dataone.org/odo/")
QK = Namespace("http://qudt.org/vocab/quantitykind/")
QB = Namespace("http://purl.org/linked-data/cube#")
SOSA = Namespace("http://www.w3.org/ns/sosa/")
TIME = Namespace("http://www.w3.org/2006/time#")
DWC = Namespace("http://rs.tdwg.org/dwc/terms/")
EX = Namespace("https://w3id.org/smn/example/fraser-stock-recruit#")


def require(graph: Graph, triple: tuple, message: str) -> None:
    """Fail with a focused message when a required triple is absent."""
    if triple not in graph:
        raise AssertionError(message)


def require_term_annotations(graph: Graph, term: URIRef, *, skos_term: bool) -> None:
    """Check the repository's minimum human-facing annotation contract.

    Which property holds a definition is decided in verify_term_definitions.py,
    which applies the same rule to every local term, so it is not restated here.
    """
    label_property = SKOS.prefLabel if skos_term else RDFS.label
    if not list(graph.objects(term, label_property)):
        raise AssertionError(f"{term} has no preferred label")
    if not has_definition(graph, term, skos_term=skos_term):
        raise AssertionError(f"{term} has no definition")
    require(
        graph,
        (term, RDFS.isDefinedBy, URIRef("https://w3id.org/smn")),
        f"{term} has no canonical rdfs:isDefinedBy annotation",
    )


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    graph = Graph()

    for path in (
        root / "ontology/modules/02-observation-measurement.ttl",
        root / "ontology/modules/03-assessment-benchmarks.ttl",
        root / "ontology/modules/06-data-interoperability.ttl",
        root / "ontology/modules/07-controlled-vocabularies.ttl",
        root / "ontology/modules/alignment-main.ttl",
        root / "ontology/examples/fraser-stock-recruit-year-age.ttl",
    ):
        graph.parse(path, format="turtle")

    # Shared abundance is an atomic SOSA-aligned characteristic, not a compound
    # variable or a synonym for the unit COUNT.
    require(graph, (SMN.Abundance, RDF.type, OWL.Class), "smn:Abundance must be an OWL class")
    require(
        graph,
        (SMN.Abundance, RDFS.subClassOf, SMN.Characteristic),
        "smn:Abundance must specialize smn:Characteristic",
    )
    require_term_annotations(graph, SMN.Abundance, skos_term=False)
    require(
        graph,
        (SMN.Abundance, SKOS.closeMatch, QK.Population),
        "smn:Abundance must retain the conservative QUDT Population mapping",
    )
    require(
        graph,
        (SMN.Abundance, RDFS.seeAlso, DWC.individualCount),
        "smn:Abundance must cross-reference Darwin Core individualCount without a SKOS concept mapping",
    )
    for mapping_predicate in (
        SKOS.exactMatch,
        SKOS.closeMatch,
        SKOS.broadMatch,
        SKOS.narrowMatch,
        SKOS.relatedMatch,
    ):
        if (SMN.Abundance, mapping_predicate, DWC.individualCount) in graph:
            raise AssertionError("smn:Abundance must not concept-map to the Darwin Core individualCount property")

    # Basis concepts, coordinate properties, and literal values deliberately use
    # different RDF resources and types.
    year_bases = {
        SMN.BroodYearBasis: SMN.broodYear,
        SMN.ReturnYearBasis: SMN.returnYear,
        SMN.CatchYearBasis: SMN.catchYear,
    }
    require(
        graph,
        (SMN.YearBasisScheme, RDF.type, SKOS.ConceptScheme),
        "smn:YearBasisScheme must be a SKOS concept scheme",
    )
    require_term_annotations(graph, SMN.YearBasisScheme, skos_term=True)
    require(graph, (SMN.YearBasis, RDF.type, SKOS.Concept), "smn:YearBasis must be a SKOS concept")
    require(graph, (SMN.YearBasis, SKOS.inScheme, SMN.YearBasisScheme), "smn:YearBasis is outside its scheme")
    require_term_annotations(graph, SMN.YearBasis, skos_term=True)
    for basis, dimension in year_bases.items():
        require(graph, (basis, RDF.type, SKOS.Concept), f"{basis} must be a SKOS concept")
        require(graph, (basis, SKOS.inScheme, SMN.YearBasisScheme), f"{basis} is outside its scheme")
        require(graph, (basis, SKOS.broader, SMN.YearBasis), f"{basis} is not under smn:YearBasis")
        require_term_annotations(graph, basis, skos_term=True)
        if (basis, RDF.type, OWL.Class) in graph:
            raise AssertionError(f"{basis} must remain a SKOS concept rather than also becoming an OWL class")
        require(graph, (dimension, RDF.type, OWL.DatatypeProperty), f"{dimension} must be a datatype property")
        require(graph, (dimension, RDF.type, QB.DimensionProperty), f"{dimension} must be a Data Cube dimension")
        require(graph, (dimension, RDFS.range, XSD.gYear), f"{dimension} must carry xsd:gYear values")
        require_term_annotations(graph, dimension, skos_term=False)
        require(graph, (dimension, QB.concept, basis), f"{dimension} must identify its year-reference basis")
        require(
            graph,
            (dimension, RDFS.seeAlso, TIME.inXSDgYear),
            f"{dimension} must document the conservative OWL-Time bridge",
        )

    require(
        graph,
        (SMN.BroodYearBasis, SKOS.closeMatch, GCDFO.BroodYear),
        "brood-year basis must map conservatively to the DFO concept",
    )
    require(
        graph,
        (SMN.ReturnYearBasis, SKOS.closeMatch, GCDFO.ReturnYear),
        "return-year basis must map conservatively to the DFO concept",
    )
    require(
        graph,
        (SMN.BroodYearBasis, SKOS.closeMatch, ODO.SALMON_00000520),
        "brood-year basis must map conservatively to NCEAS/DataONE SALMON",
    )

    # The four independent age axes remain independent SKOS schemes.
    age_schemes = {
        SMN.AgeNotationScheme: (SMN.AgeNotation, SMN.GilbertRichAgeNotation, SMN.EuropeanAgeNotation),
        SMN.AgeBasisScheme: (SMN.AgeBasis, SMN.AgeAtReturnBasis, SMN.AgeAtMaturityBasis, SMN.AgeAtSamplingBasis),
        SMN.AgeDimensionScheme: (SMN.AgeDimension, SMN.TotalAgeDimension, SMN.FreshwaterAgeDimension, SMN.OceanAgeDimension),
        SMN.AgeClassValueScheme: tuple([SMN.AgeClassValue] + [SMN[f"AgeClassValue{i}"] for i in range(1, 8)]),
    }
    for scheme, concepts in age_schemes.items():
        require(graph, (scheme, RDF.type, SKOS.ConceptScheme), f"{scheme} must be a SKOS concept scheme")
        require_term_annotations(graph, scheme, skos_term=True)
        for concept in concepts:
            require(graph, (concept, RDF.type, SKOS.Concept), f"{concept} must be a SKOS concept")
            require(graph, (concept, SKOS.inScheme, scheme), f"{concept} is outside {scheme}")
            require_term_annotations(graph, concept, skos_term=True)

    for age in range(1, 8):
        concept = SMN[f"AgeClassValue{age}"]
        require(
            graph,
            (concept, SKOS.notation, Literal(age, datatype=XSD.integer)),
            f"{concept} must expose integer notation {age}",
        )
        labels = [str(label).lower() for label in graph.objects(concept, SKOS.prefLabel)]
        if any("year class" in label for label in labels):
            raise AssertionError(f"{concept} uses the ambiguous cohort phrase 'year class'")

    # The worked example demonstrates mixed grain, explicit Gilbert-Rich
    # decomposition, and separate result-producing procedures for abundance
    # estimation and age determination.
    require(graph, (EX.spawnerEstimateDSD, QB.component, EX.spawnerBroodYearComponent), "spawner DSD lacks brood year")
    if (EX.spawnerEstimateDSD, QB.component, EX.spawnerReturnYearComponent) in graph:
        raise AssertionError("stock-by-brood-year spawner estimates must not inherit a return-year dimension")
    for component in (
        EX.recruitBroodYearComponent,
        EX.recruitReturnYearComponent,
        EX.recruitTotalAgeComponent,
        EX.recruitFreshwaterAgeComponent,
    ):
        require(graph, (EX.recruitEstimateDSD, QB.component, component), "recruit DSD is missing a varying dimension")
    require(
        graph,
        (EX.fraserRecruitEstimates, EX.ageNotation, SMN.GilbertRichAgeNotation),
        "example must declare Gilbert-Rich notation",
    )
    require(
        graph,
        (EX.fraserRecruitEstimates, EX.ageBasis, SMN.AgeAtReturnBasis),
        "example must declare age-at-return basis",
    )
    for recruit_observation in (
        EX.recruits2000_2004_age42,
        EX.recruits2000_2005_age52,
    ):
        if (recruit_observation, SOSA.usedProcedure, EX.scaleAgeDeterminationProcedure) in graph:
            raise AssertionError(
                "an age-determination procedure must not be the result-producing procedure "
                "of a recruit-abundance observation"
            )
        require(
            graph,
            (recruit_observation, SOSA.usedProcedure, EX.recruitAbundanceEstimationProcedure),
            "each recruit-abundance observation must identify its abundance-estimation procedure",
        )

    age_determinations = {
        EX.ageDetermination2000_2004_age42: (
            EX.ageResult2000_2004_age42,
            SMN.AgeClassValue4,
            SMN.AgeClassValue2,
        ),
        EX.ageDetermination2000_2005_age52: (
            EX.ageResult2000_2005_age52,
            SMN.AgeClassValue5,
            SMN.AgeClassValue2,
        ),
    }
    for age_observation, (age_result, total_age, freshwater_age) in age_determinations.items():
        require(
            graph,
            (age_observation, RDF.type, SOSA.Observation),
            "age determination must be an observation",
        )
        require(
            graph,
            (age_observation, SOSA.observedProperty, EX.salmonAgeProperty),
            "age determination must observe salmon age rather than abundance",
        )
        if (age_observation, SOSA.observedProperty, EX.salmonAbundanceProperty) in graph:
            raise AssertionError("the separate age observation must not also observe abundance")
        require(
            graph,
            (age_observation, SOSA.usedProcedure, EX.scaleAgeDeterminationProcedure),
            "the scale procedure must be attached to the separate age observation",
        )
        require(
            graph,
            (age_observation, SOSA.hasResult, age_result),
            "age determination must expose an age result",
        )
        require(graph, (age_result, RDF.type, SOSA.Result), "age result must be a SOSA result")
        require(graph, (age_result, EX.totalAge, total_age), "age result must expose the determined total age")
        require(
            graph,
            (age_result, EX.freshwaterAge, freshwater_age),
            "age result must expose the determined freshwater age",
        )

    migration_path = root / "docs/migrations/gcdfo-to-salmon-year-age.csv"
    with migration_path.open(newline="", encoding="utf-8") as handle:
        migrations = {(row["old_iri"], row["new_iri"]): row for row in csv.DictReader(handle)}
    for old, new in (
        (str(GCDFO.YearBasis), str(SMN.YearBasis)),
        (str(GCDFO.BroodYear), str(SMN.BroodYearBasis)),
        (str(GCDFO.ReturnYear), str(SMN.ReturnYearBasis)),
        (str(GCDFO.CatchYear), str(SMN.CatchYearBasis)),
        (str(GCDFO.GilbertRichAgeNotation), str(SMN.GilbertRichAgeNotation)),
        (str(GCDFO.AgeAtReturnBasis), str(SMN.AgeAtReturnBasis)),
        (str(GCDFO.TotalAgeDimension), str(SMN.TotalAgeDimension)),
        (str(GCDFO.Age1YearClass), str(SMN.AgeClassValue1)),
        (str(GCDFO.Age7YearClass), str(SMN.AgeClassValue7)),
    ):
        if (old, new) not in migrations:
            raise AssertionError(f"migration map is missing {old} -> {new}")

    print("Year/age/abundance semantic contract verified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
