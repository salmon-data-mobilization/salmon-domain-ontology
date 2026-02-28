# Salmon Domain Ontology Modules

This directory contains the modular build-out for the salmon-domain ontology.

## Category modules (phase 1 scaffold)

1. `01-entity-systematics.ttl` — core entities, strata classes, and biological unit composition relations.
2. `02-observation-measurement.ttl` — SOSA-aligned observations, measurements, survey events, and escapement measurement semantics.
3. `03-assessment-benchmarks.ttl` — stock-assessment abstractions, reference points, benchmark classes, and exploitation-rate terms.
4. `04-management-governance.ttl` — conservative shared event taxonomy (policy schemes remain profile-scoped).
5. `05-provenance-quality.ttl` — shared provenance/quality artifact classes (program confidence vocabularies profile-scoped).
6. `06-data-interoperability.ttl` — I-ADOPT/SOSA/Darwin Core interoperability bridge axioms.
7. `07-controlled-vocabularies.ttl` — small curated shared SKOS schemes/concepts for context, life phase, and origin only.
8. `08-rda-case-study-profile-bridges.ttl` — Hakai profile-layer bridge terms from RDA juvenile-condition case-study mappings.
9. `09-rda-neville-decomposition-profile-bridges.ttl` — Neville decomposition profile-layer bridge terms (not promoted into shared core by default).

## Alignment modules (phase 2 migration)

- `alignment-main.ttl` — conservative merge-safe upper-level alignment bridges.
- `alignment-research.ttl` — exploratory alignment candidates with stronger axioms.

## Import behavior

- `../salmon-domain-ontology.ttl` imports modules 01–07 + `alignment-main.ttl`.
- `../salmon-domain-ontology-research.ttl` imports the conservative build and then adds `alignment-research.ttl`.
- `../salmon-domain-ontology-rda-case-study.ttl` imports the conservative build and then adds `08-rda-case-study-profile-bridges.ttl`.

## Guardrails

- Use `salmon:` for domain terms intended for reuse across organizations.
- Preserve source-provenance notes when migrating terms from DFO Salmon Ontology.
- Do **not** remove terms from DFO source ontology as part of this phase.
