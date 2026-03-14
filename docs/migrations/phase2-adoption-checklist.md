# Phase 2 adoption checklist

Status: **retained as the post-closeout reference checklist; phase 2 is closed and `0.0.0` is tagged**

Use sections A-C when adopting or validating the modular `salmon-domain-ontology`
artifacts in downstream work. Section D records the repo-level closeout evidence
that cleared the original phase-2 gate.

## A) Ontology maintainers (repo-level)

- [ ] Confirm canonical namespace usage matches `docs/publishing/namespace-decision.md` (`https://w3id.org/smn/` as `smn:`; W3ID path live)
- [ ] Confirm shared build imports modules `01`-`07` + `alignment-main`
- [ ] Confirm case-study build imports modules `08` and `09` only as profile bridges
- [ ] Verify migration map (`gcdfo-to-salmon-wave1.csv`) is up to date for migrated/deferred terms
- [ ] Verify boundary contract aligns with `phase2-boundary-rules.md`

## B) DFO consumer adoption

- [ ] Keep DFO profile vocabulary terms in profile namespace (no forced promotion into shared)
- [ ] Apply old->new replacements only for `status=migrated` rows from the migration map
- [ ] Preserve deferred-profile terms (`status=deferred_profile`) in DFO profile pipelines
- [ ] Confirm no dependency on deprecated `gcdfo:` shared namespace assumptions in integration scripts
- [ ] Validate at least one representative DFO ingest using the shared + profile bridge pattern

## C) SPSR consumer adoption

- [ ] Update prefix bindings and graph queries to use `smn:` canonical shared terms
- [ ] Validate joins still resolve when profile terms are mapped via bridge modules (Tier 2/3 mappings)
- [ ] Confirm dashboards/reports treat Tier 3 mappings as advisory unless promoted
- [ ] Confirm no hard dependency on removed-in-shared policy-specific SKOS families
- [ ] Run one end-to-end SPSR extraction/report smoke test on case-study build

## D) Phase-2 closeout evidence (historical gate)

- [x] Turtle parse check passed for all `.ttl` files in `ontology/`
- [x] Cutover execution runbook finalized (`phase2-cutover-execution-runbook.md`)
- [x] Tier-3 mapping triage register recorded (`phase2-tier3-mapping-triage.md`)
- [x] DFO provider-verification note recorded in place of the fictional separate DFO live-smoke gate (`phase2-dfo-live-smoke-runbook.md`)
- [x] SPSR smoke-run evidence recorded using `phase2-downstream-smoke-run-templates.md`
- [x] Migration docs present and linked from repo README
- [x] Original issue #3 blocker package cleared before the `0.0.0` stabilization tag

## E) Current use of this checklist

Phase 2 already closed. Use A-C as an adopter checklist for future downstream
work; do not treat D as an open blocker register unless a new migration/cutover
cycle is explicitly opened.
