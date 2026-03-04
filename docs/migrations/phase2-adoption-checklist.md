# Phase 2 adoption checklist

Use this checklist when adopting the modular `salmon-domain-ontology` migration artifacts.

## A) Ontology maintainers (repo-level)

- [ ] Confirm canonical namespace usage is `http://w3id.org/salmon/` (`salmon:`)
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

- [ ] Update prefix bindings and graph queries to use `salmon:` canonical shared terms
- [ ] Validate joins still resolve when profile terms are mapped via bridge modules (Tier 2/3 mappings)
- [ ] Confirm dashboards/reports treat Tier 3 mappings as advisory unless promoted
- [ ] Confirm no hard dependency on removed-in-shared policy-specific SKOS families
- [ ] Run one end-to-end SPSR extraction/report smoke test on case-study build

## D) Pre-release validation evidence

- [ ] Turtle parse check passes for all `.ttl` files in `ontology/`
- [ ] Cutover execution runbook is finalized (`phase2-cutover-execution-runbook.md`)
- [ ] Tier-3 mapping triage register is recorded (`phase2-tier3-mapping-triage.md`)
- [ ] DFO smoke-run evidence is recorded using `phase2-downstream-smoke-run-templates.md`
- [ ] SPSR smoke-run evidence is recorded using `phase2-downstream-smoke-run-templates.md`
- [ ] Migration docs are present and linked from repo README
- [ ] Open blockers are tracked in issue #3 before declaring cutover-ready

## E) Cutover readiness gate

Cutover is ready only when A-D are complete and release-readiness notes show no unresolved blocking items for DFO/SPSR consumers.
