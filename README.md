# salmon-domain-ontology

Shared salmon interoperability ontology for cross-organization data integration.

## Project status

This repository is under active development as we build out the **Salmon Domain Ontology** as a reusable, cross-organization semantic layer for salmon data.

## Contributions welcome

We welcome contributions from domain experts, data stewards, and ontology practitioners.

If you want to contribute:
- Open an issue describing the use case, gap, or term request.
- Reference relevant domain standards, vocabularies, or source schemas where possible.
- Submit a pull request for proposed ontology/module updates.
- Follow `CONVENTIONS.md` for namespace and modeling rules.

## Current structure

- `ontology/salmon-domain-ontology.ttl` — modular primary build (imports modules 01–07 + conservative alignment)
- `ontology/salmon-domain-ontology-research.ttl` — optional research build (adds exploratory alignment module)
- `ontology/salmon-domain-ontology-rda-case-study.ttl` — optional case-study bridge build (adds profile bridge mappings from RDA juvenile-condition graph, including Hakai + Neville decomposition terms)
- `ontology/modules/` — category modules + alignment modules + profile bridge modules
- `CONVENTIONS.md` — modeling and namespace conventions (`salmon:` canonical)
- `docs/migrations/README.md` — migration map, boundary rules, adoption checklist, cutover runbook, smoke-run templates, and release-readiness notes

## Phase notes (2026-02-27)

This repository now includes a seven-category module scaffold and migrated reusable upper-level alignment work from the DFO Salmon Ontology alignment branch.

Migration stance:
- Reusable terms are being minted in `salmon:`.
- DFO source ontology terms are **not removed** during this phase.
- A migration map is tracked in `docs/migrations/gcdfo-to-salmon-wave1.csv`.
