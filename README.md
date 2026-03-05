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
- `docs/publishing/namespace-decision.md` — namespace stabilization decision and freeze rule
- `docs/publishing/w3id-request-payload.md` — ready-to-submit W3ID registration payload

## Publishing status (important)

Namespace stabilization is in progress and must complete before broad downstream cutover.

- `w3id.org/salmon` is currently controlled by another project.
- `w3id.org/salmon-domain-ontology` registration is being prepared.
- Until W3ID registration + in-repo IRI rewrite are complete, dependent-app migrations should remain limited/surgical.
