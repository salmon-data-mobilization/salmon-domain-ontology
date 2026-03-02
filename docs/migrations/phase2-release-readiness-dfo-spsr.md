# Phase 2 release-readiness notes (DFO + SPSR downstream consumers)

These notes track the minimum evidence required before publish-ready migration/cutover.

## Readiness dimensions

### 1) Shared/profile boundary stability

- Boundary rules documented and aligned with `CONVENTIONS.md`.
- Deferred profile terms remain out of shared core.
- Bridge modules are used for profile concept interoperability without semantic collapse.

### 2) Migration artifact completeness

- Machine map exists: `gcdfo-to-salmon-wave1.csv`.
- Human-readable inventory exists: `wave1-term-inventory.md`.
- Case-study bridge coverage exists: `rda-graph-concept-coverage.md`.
- Phase 2 operations docs exist:
  - `phase2-boundary-rules.md`
  - `phase2-adoption-checklist.md`
  - `phase2-cutover-execution-runbook.md`
  - `phase2-downstream-smoke-run-templates.md`
  - `phase2-tier3-mapping-triage.md`

### 3) DFO downstream readiness

Required evidence:

- DFO pipelines can consume shared `salmon:` terms for migrated rows.
- Deferred DFO terms remain profile-resolved without loss.
- No production dependency on auto-canonicalizing Tier-3 mappings.

### 4) SPSR downstream readiness

Required evidence:

- SPSR query/report layer resolves shared terms and bridge mappings.
- Reports depending on profile vocabularies retain expected references.
- At least one end-to-end smoke run passes against selected build target.

## Blocker register (issue #3)

| Blocker | Owner | Evidence | Status |
| --- | --- | --- | --- |
| DFO consumer smoke-run evidence recorded | DFO smoke-run owner (TBD by team) | Use template in `phase2-downstream-smoke-run-templates.md` and post result to issue #3 | Open |
| SPSR consumer smoke-run evidence recorded | SPSR smoke-run owner (TBD by team) | Use template in `phase2-downstream-smoke-run-templates.md` and post result to issue #3 | Open |
| Cutover execution runbook finalized (timing, owner, rollback) | Ontology maintainer (`@Br-Johnson`) | `phase2-cutover-execution-runbook.md` | Cleared |
| Tier-3 mapping queue explicitly triaged for production policy | Ontology maintainer (`@Br-Johnson`) | `phase2-tier3-mapping-triage.md` | Cleared |

## Publish-ready decision gate

Publish-ready cutover requires:

1. Both consumer smoke-run blockers closed with evidence links in issue #3.
2. No unresolved critical regressions from smoke runs.
3. Cutover coordinator records final go/no-go decision in issue #3.
