# Entrypoints (What Is Actually Used?)

Purpose: keep one short, reliable map of what starts the ontology builds, what is wired in, and where to edit things.

## Run (human-facing)

- Start command(s): none; this repo ships ontology artifacts and docs, not a running app/service.
- Local URL(s): none.
- Required environment variables (names only, no secrets): none for normal doc/ontology work.

## Build

- Build command(s): no compile step; committed Turtle files are the canonical build artifacts.
- Main deliverables:
  - `ontology/salmon-domain-ontology.ttl` — primary modular build
  - `ontology/salmon-domain-ontology-research.ttl` — research overlay build
  - `ontology/salmon-domain-ontology-rda-case-study.ttl` — case-study/profile-bridge build
  - `salmon-domain-ontology.ttl` — root compatibility wrapper that imports `https://w3id.org/smn`

## Test

- Test command(s):
  - Parse all ontology Turtle files:
    ```bash
    python3 - <<'PY'
    from pathlib import Path
    from rdflib import Graph
    for path in sorted(Path('ontology').rglob('*.ttl')):
        Graph().parse(path, format='turtle')
        print(f'OK {path}')
    PY
    ```
  - Regenerate fixture smoke evidence when the migration/evidence helper changes:
    ```bash
    python3 docs/migrations/evidence/run_phase2_smoke_fixture_checks.py
    ```
- Fastest smoke test: parse the `ontology/**/*.ttl` files with rdflib.

## App Entry Points / Wiring

- Main entry file(s):
  - `ontology/salmon-domain-ontology.ttl`
  - `ontology/salmon-domain-ontology-research.ttl`
  - `ontology/salmon-domain-ontology-rda-case-study.ttl`
  - `salmon-domain-ontology.ttl`
- Routes / handlers / commands:
  - No app routes.
  - Publication-routing source of truth lives in:
    - `docs/publishing/namespace-decision.md`
    - `docs/publishing/w3id-request-payload.md`
    - `docs/publishing/w3id-smn-draft/.htaccess`
- Background jobs (if any): none.

## UI Styling

- Canonical styling system (repo-majority): not applicable.
- Style entry files / patterns: not applicable.
- Design tokens / CSS variables live in: not applicable.
- Inline styles policy: not applicable.

## Canonical Implementations (Per Feature)

- Shared ontology core → `ontology/salmon-domain-ontology.ttl` importing modules `01`-`07` plus `ontology/modules/alignment-main.ttl`
- Research alignment overlay → `ontology/salmon-domain-ontology-research.ttl` + `ontology/modules/alignment-research.ttl`
- Case-study/profile bridges → `ontology/salmon-domain-ontology-rda-case-study.ttl` + modules `08` and `09`
- Root compatibility import path → `salmon-domain-ontology.ttl`
- Modeling rules and boundary decisions → `CONVENTIONS.md` + `docs/migrations/phase2-boundary-rules.md`
- Migration/cutover status and evidence → `docs/migrations/README.md` + `docs/migrations/phase2-*.md` + `docs/migrations/evidence/`
- Namespace/publication posture → `docs/publishing/namespace-decision.md` + `docs/publishing/w3id-request-payload.md`

## What to read before editing

- Changing ontology terms/modules/build imports:
  - `CONVENTIONS.md`
  - `ontology/modules/README.md`
  - the relevant module(s) under `ontology/modules/`
- Changing migration/cutover docs:
  - `docs/migrations/README.md`
  - `docs/migrations/phase2-adoption-checklist.md`
  - `docs/migrations/phase2-cutover-execution-runbook.md`
  - `docs/migrations/phase2-tier3-mapping-triage.md`
- Changing namespace/publication docs:
  - `docs/publishing/namespace-decision.md`
  - `docs/publishing/w3id-request-payload.md`
  - `docs/publishing/evidence/2026-03-13-w3id-live-redirect-check.md`
