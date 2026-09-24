# Salmon Domain Ontology Modules

This directory contains the modular build-out for the salmon-domain ontology.

If you are new to ontologies, read this first:
- `../../docs/guides/modules-and-bridges-for-biologists.md`

That guide explains (in plain language) how modules, local program ontologies, and bridge profiles work together when mapping real datasets.

## Shared-core modules (01–07)

These files are the shared Salmon-layer baseline by default:

1. `01-entity-systematics.ttl` — core entities, strata classes, and biological unit composition relations.
2. `02-observation-measurement.ttl` — SOSA-aligned observations, measurements, shared abundance, typed year coordinates, survey events, and escapement measurement semantics.
3. `03-assessment-benchmarks.ttl` — stock-assessment abstractions, reference points, benchmark classes, and exploitation-rate terms.
4. `04-management-governance.ttl` — conservative shared event taxonomy (policy schemes remain profile-scoped).
5. `05-provenance-quality.ttl` — shared provenance/quality artifact classes (program confidence vocabularies profile-scoped).
6. `06-data-interoperability.ttl` — I-ADOPT/SOSA/Darwin Core interoperability bridge axioms plus conservative Data Cube and OWL-Time year-coordinate bridges.
7. `07-controlled-vocabularies.ttl` — curated shared SKOS schemes/concepts for year basis, salmon age, context, life phase, origin, methods, statistical modifiers, juvenile freshwater residence duration, juvenile rearing habitat, life-history type, and cycle line.

## Profile/case-study modules (08, 09)

These are not part of the permanent shared baseline by default. They are the **RDA juvenile-condition working case study** used to test the practical mapping process:

- `08-rda-case-study-profile-bridges.ttl` — Hakai profile-layer bridge terms.
  - Focus today: **method semantics and measurement-context terms**.
  - Implemented as an assembled module from split case-study fragments in `../case-studies/rda-juvenile-condition/`:
    - `08-rda-hakai-method-scheme.ttl` (scheme/context)
    - `08-rda-hakai-measurement-methods.ttl` (measurement term mappings)
  - Built via `make compose-case-study-modules`.

- `09-rda-neville-decomposition-profile-bridges.ttl` — Neville decomposition profile-layer bridge terms.
  - Focus today: **entity semantics, observation/measurement concepts, and constraint/statistical modifier terms**.
  - Implemented as an assembled module from split case-study fragments in `../case-studies/rda-juvenile-condition/`:
    - `09-rda-neville-entities.ttl` (entities/strata)
    - `09-rda-neville-observations.ttl` (variables + measurements)
    - `09-rda-neville-constraints.ttl` (constraints/statistical modifiers)
  - Built via `make compose-case-study-modules`.

Importantly, both modules stay in profile-space and map to `smn:` with conservative SKOS predicates unless there is explicit promotion criteria.

## Alignment modules (phase 2 migration)

- `alignment-main.ttl` — conservative merge-safe upper-level alignment bridges.
- `alignment-research.ttl` — exploratory alignment candidates with stronger axioms.

## Optional metamodel views

These do **not** live in `modules/` because they are not part of the normative shared-core import spine:

- `../views/salmon-data-metamodel.ttl` — optional non-normative composition root
- `../views/*.ttl` — focused entity/property/variable/method/event/result/provenance slices for architecture review and biologist-friendly orientation

## Import behavior

- `../salmon-domain-ontology.ttl` imports modules 01–07 + `alignment-main.ttl`.
- `../salmon-domain-ontology-research.ttl` imports the conservative build and then adds `alignment-research.ttl`.
- `../salmon-domain-ontology-rda-case-study.ttl` imports the conservative build and then adds `08-rda-case-study-profile-bridges.ttl` and `09-rda-neville-decomposition-profile-bridges.ttl`.
- `../views/salmon-data-metamodel.ttl` is intentionally **not** imported by any of the above entrypoints.

## Suggested editing posture for future refactors

- If your goal is a simpler onboarding draft, keep the build surface to `smn`, `02`, `07` initially and layer in other shared modules by need.
- If review pressure spikes, merge additional semantics from modules 08/09 into shared core only after cross-dataset reuse is demonstrated.
- Prefer adding explicit term definitions (`iao:0000115` for OWL terms, `skos:definition` for SKOS terms) plus `rdfs:isDefinedBy`; attach provenance when authoritative wording exists. Use `rdfs:comment` only for editorial mapping rationale or scope notes, not as the primary definition field.
- Track unresolved definition/provenance gaps in `../../docs/annotation-gap-ledger.md` rather than inventing new wording during migration cleanup.

## Guardrails

- Use `smn:` for domain terms intended for reuse across organizations.
- Preserve source-provenance notes when migrating terms from DFO Salmon Ontology.
- Keep the optional metamodel view layer in `ontology/views/` rather than the shared-core module chain.
- DFO-specific core terms should not be removed casually, but shared non-normative metamodel views now live here rather than in the DFO repo.
