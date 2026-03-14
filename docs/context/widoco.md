# WIDOCO in this repo

This file is the repo-specific guide for generating the Salmon Domain Ontology publication surface.

## Purpose

WIDOCO generates the HTML documentation site for the shared ontology.

This repo uses WIDOCO as part of a broader publication contract that also includes downloadable serializations and immutable release snapshots.

## Canonical source

- Main ontology input for WIDOCO: `ontology/salmon-domain-ontology.ttl`

## Canonical outputs

Latest publication surface under `docs/`:
- `docs/index.html` — latest HTML documentation
- `docs/smn.ttl` — latest Turtle serialization
- `docs/smn.owl` — latest RDF/XML serialization
- `docs/smn.jsonld` — latest JSON-LD serialization

Immutable version snapshots:
- `docs/releases/<version>/index.html`
- `docs/releases/<version>/smn.ttl`
- `docs/releases/<version>/smn.owl`
- `docs/releases/<version>/smn.jsonld`

## Commands

- Download WIDOCO: `make install-widoco`
- Download ROBOT: `make install-robot`
- Generate HTML only: `make docs-widoco`
- Generate serializations only: `make docs-serializations`
- Run full publication refresh: `make docs-refresh`
- Write immutable snapshot: `make release-snapshot VERSION=X.Y.Z`

## Current limitations

- Java is required for both WIDOCO and ROBOT.
- W3ID still points at the conservative Turtle-first fallback even though generated latest assets now exist under `docs/` and `docs/releases/0.0.0/`; only switch routing after stable public targets are published and verified.
- Ontology header metadata is still thin, so WIDOCO output quality will improve once version / attribution / namespace metadata are expanded.

## Guardrails

- Treat `docs/index.html` as generated output after WIDOCO is adopted.
- Keep project-specific HTML tweaks in `scripts/postprocess_widoco_html.py` rather than hand-editing generated HTML.
- Prefer updating ontology metadata in `ontology/salmon-domain-ontology.ttl` rather than patching generated docs by hand.
