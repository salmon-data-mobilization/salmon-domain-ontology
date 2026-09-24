# salmon-domain-ontology

Shared salmon interoperability ontology for cross-organization data integration.

**Integration context:** See the Salmon Data Integration System overview page (https://br-johnson.github.io/salmon-data-integration-system/) and walkthrough video (https://youtu.be/B0Zqac49zng?si=VmOjbfMDMd2xW9fH).

## Project status

This repository is under active development as we build out the **Salmon Domain Ontology** as a reusable, cross-organization semantic layer for salmon data.

## Contributions welcome

We welcome contributions from domain experts, data stewards, and ontology practitioners.

If you want to contribute:
- Open an issue describing the use case, gap, or term request.
- Use issue templates under `.github/ISSUE_TEMPLATE/` for new terms, missing parents, definition updates, and obsoletions.
- Reference relevant domain standards, vocabularies, or source schemas where possible.
- Submit a pull request for proposed ontology/module updates.
- Follow `CONVENTIONS.md` for namespace and modeling rules.

## Current structure

- `ontology/salmon-domain-ontology.ttl` - modular primary build (imports modules 01-07 + conservative alignment)
- `salmon-domain-ontology.ttl` - flattened, import-free master TTL artifact for one-file consumers (generated)
- `ontology/salmon-domain-ontology-research.ttl` - optional research build (adds exploratory alignment module)
- `ontology/salmon-domain-ontology-rda-case-study.ttl` - optional case-study bridge build (adds profile bridge mappings from the RDA juvenile-condition graph, including Hakai + Neville decomposition terms)
- `ontology/modules/` - category modules + alignment modules + profile bridge modules
- `ontology/views/` - optional, non-normative metamodel views for maintainers and salmon biologists
- `CONVENTIONS.md` - modeling and namespace conventions (`smn:` canonical)
- `docs/context/widoco.md` - WIDOCO publication workflow and output contract
- `docs/migrations/README.md` - migration map, boundary rules, adoption checklist, cutover runbook, smoke-run templates, and release-readiness notes
- `docs/publishing/namespace-decision.md` - namespace stabilization decision and freeze rule
- `docs/publishing/w3id-request-payload.md` - merged `smn` W3ID registration record + follow-up publication checklist
- `docs/guides/modules-and-bridges-for-biologists.md` - beginner-friendly guide to modules, local profiles, and bridge mapping

## Where non-core terms live

For teams using MetaSalmon Data GPT / R package with local or program-specific terms:

1. **File-first (recommended first step):** keep local terms in a project-local profile file (their own namespace), map conservatively to shared `smn:`.
2. **Collaborative profile artifact (optional):** if multiple teams need shared access to the same local contract, use `https://w3id.org/smn/profile/<program>/` as a temporary bridge namespace.
3. **Shared-core promotion (rare):** promote to `smn:` only when term reuse is broad and semantics are stable.

If a team wants an independent WIDOCO site for profile terms, run WIDOCO against their own profile ontology source and host that site under their own namespace/hosting. SMN's own publication workflow remains centered on the shared ontology plus curated pilot profiles, so this is the simplest way to serve a separate profile docs site without expanding the core namespace.

## Docs / publication workflow

The repo now has a first-pass publication pipeline matching the DFO pattern in a lighter form.

Core commands:
- `make install-widoco`
- `make install-robot`
- `make compose-case-study-modules`
- `make compose-flat-ttl`
- `make verify-ontology-parse`
- `make verify-year-age-semantic-contract`
- `make verify-term-definitions`
- `make verify-flat-ttl`
- `make verify-doc-term-anchors`
- `make verify-doc-version-metadata`
- `make test`
- `make ci`
- `make verify-generated-artifacts`
- `make docs-refresh`
- `make release-snapshot VERSION=X.Y.Z`
- `make release VERSION=X.Y.Z`

Generated publication targets:
- `docs/index.html`
- `docs/smn.ttl`
- `docs/smn.owl`
- `docs/smn.jsonld`
- `docs/releases/<version>/`

Note: Java 17+ is required for WIDOCO and ROBOT. The repo now carries generated latest assets under `docs/` plus immutable release snapshots under `docs/releases/<version>/`. `make release VERSION=X.Y.Z` is the canonical release path: it updates ontology version metadata, refreshes the WIDOCO publication surface, runs validation, and writes the immutable snapshot. Root, SemVer, and canonical term-path W3ID routing use those published targets; term paths such as `https://w3id.org/smn/Escapement` dereference to WIDOCO anchors by default and remain content-negotiable for Turtle, RDF/XML, and JSON-LD.

## New to ontologies?

Start with `docs/guides/modules-and-bridges-for-biologists.md`.
It explains the module + bridge approach in plain language for dataset teams.

If you want the optional mental-model view of how entity/property/variable/constraint/method/result pieces fit together, then read `ontology/views/README.md` next.
