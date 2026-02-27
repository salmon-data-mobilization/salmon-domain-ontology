# salmon-domain-ontology

Shared salmon interoperability ontology for cross-organization data integration.

## Current structure

- `ontology/salmon-domain-ontology.ttl` — modular primary build (imports modules 01–07 + conservative alignment)
- `ontology/salmon-domain-ontology-research.ttl` — optional research build (adds exploratory alignment module)
- `ontology/modules/` — category modules + alignment modules
- `CONVENTIONS.md` — modeling and namespace conventions (`salmon:` canonical)

## Phase notes (2026-02-27)

This repository now includes a seven-category module scaffold and migrated reusable upper-level alignment work from the DFO Salmon Ontology alignment branch.

Migration stance:
- Reusable terms are being minted in `salmon:`.
- DFO source ontology terms are **not removed** during this phase.
- A migration map is tracked in `docs/migrations/gcdfo-to-salmon-wave1.csv`.
