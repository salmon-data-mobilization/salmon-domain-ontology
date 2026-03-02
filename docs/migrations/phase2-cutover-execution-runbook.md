# Phase 2 cutover execution runbook (DFO + SPSR)

This runbook defines the minimum execution contract to declare phase-2 migration cutover publish-ready.

## 1) Scope

- Applies to downstream consumers using shared `salmon:` terms and profile bridge handling.
- Covers pre-cutover checks, cutover execution timing, owner assignments, and rollback triggers.
- Works with:
  - `phase2-adoption-checklist.md`
  - `phase2-downstream-smoke-run-templates.md`
  - `phase2-tier3-mapping-triage.md`

## 2) Owner matrix

| Role | Default owner | Responsibility |
| --- | --- | --- |
| Cutover coordinator | Ontology maintainer (`@Br-Johnson`) | Go/no-go facilitation, checklist completion, final cutover note |
| DFO smoke-run owner | DFO consumer lead (TBD by team) | Execute DFO smoke-run template and attach evidence |
| SPSR smoke-run owner | SPSR consumer lead (TBD by team) | Execute SPSR smoke-run template and attach evidence |
| Rollback decision owner | Cutover coordinator + consumer owners | Trigger rollback when blocker criteria are met |

> If named downstream owners are unavailable, cutover is deferred.

## 3) Timing plan (Pacific time)

- Preferred window: Tuesday-Thursday, 09:00-12:00.
- Expected duration: 60-90 minutes.
- Freeze period: no ontology/module edits after T-24h except blocker fixes.

### T-5 business days

- Confirm PR #2 scope is stable and blocker checklist is current.
- Confirm smoke-run owners and meeting time.
- Confirm Tier-3 triage register has explicit dispositions.

### T-1 business day

- Dry-run smoke templates with representative datasets (or controlled fixture data).
- Confirm evidence links are prepared for issue #3.
- Confirm rollback contacts are reachable.

### T-0 cutover day

1. Go/no-go checkpoint (15 minutes)
   - Owner: cutover coordinator
   - Inputs: smoke evidence, triage register, rollback readiness
2. Publish/update canonical artifacts and references
   - Owner: ontology maintainer
3. Execute DFO + SPSR smoke runs against cutover target
   - Owners: DFO/SPSR smoke-run owners
4. Record results in issue #3 and PR #2
   - Owner: cutover coordinator

### T+1 business day

- Verify no post-cutover integration regressions are reported.
- Close/retire blocker checklist items that are complete.

## 4) Cutover checklist (execution-time)

- [ ] Go/no-go call held; both consumer owners present or delegated.
- [ ] DFO smoke-run executed with evidence link.
- [ ] SPSR smoke-run executed with evidence link.
- [ ] Tier-3 mapping triage dispositions reviewed and accepted for production posture.
- [ ] Publish-ready decision logged in issue #3 with timestamp and approver.

## 5) Rollback triggers

Rollback is mandatory if any of the following occurs:

1. DFO or SPSR smoke run fails on critical query/output paths.
2. Tier-3 mapping behavior would require unsafe auto-canonicalization.
3. Broken namespace/prefix resolution in downstream integration scripts.
4. Missing evidence for one or both required consumer smoke runs.

## 6) Rollback procedure

1. Announce rollback in issue #3 and PR #2 immediately.
2. Revert consumer pointers/config to last known-good release artifact.
3. Mark failed cutover as `deferred` and capture root cause.
4. Open follow-up blocker item with owner + due date before rescheduling.

Rollback completion criteria:

- Previous known-good outputs restored for both consumers.
- New blocker entry and next cutover attempt date recorded.

## 7) Evidence format (required)

Every cutover action must include:

- Owner
- Timestamp (Pacific)
- Build target/commit reference
- Evidence link (log, query output, or checklist result)
- Status (`pass`, `fail`, `deferred`)
