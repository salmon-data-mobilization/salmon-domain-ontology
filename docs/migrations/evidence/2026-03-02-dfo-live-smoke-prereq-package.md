# DFO live smoke prerequisite evidence package — 2026-03-02

## Purpose

Provide the strongest non-fabricated evidence possible from local assets before the final live DFO smoke run.

This package does **not** claim live parity completion.

## Evidence sources

- Preflight command log:
  - `docs/migrations/evidence/2026-03-02-dfo-live-smoke-preflight.log`
- Fixture smoke summary (generated from local assets only):
  - `docs/migrations/evidence/2026-03-02-phase2-smoke-fixture-results.md`
  - `docs/migrations/evidence/2026-03-02-phase2-smoke-fixture-results.json`
- DFO deferred smoke note:
  - `docs/migrations/evidence/2026-03-02-dfo-smoke-run.md`

## Pre-cleared vs blocked status

### Pre-cleared (with evidence)

- ✅ **Migrated-term readiness**
  - 3/3 sampled migrated terms resolve in shared modules (`ReportingOrManagementStratum`, `Stock`, `Deme`).
  - Evidence: fixture results (`dfo.checks["Migrated-term check"]`).

- ✅ **Deferred-profile boundary safety**
  - `ConservationUnit` and `StockManagementUnit` are not promoted into shared `salmon:` core.
  - Evidence: fixture results (`dfo.checks["Deferred-profile check"]`).

- ✅ **Bridge handling survivability (proxy)**
  - Deferred-profile terms remain consumable in local templates.
  - Evidence: fixture results (`dfo.checks["Bridge handling check"]`).

- ✅ **Migration-map scale known**
  - Current wave counts: `migrated=23`, `deferred_profile=38`.
  - Evidence: preflight log migration count step.

### Still blocked (live-runtime required)

- ⏳ **Prefix migration check in real DFO consumer runtime**
  - Local scan found no `w3id.org/salmon/` references in local `dfo-salmon-ontology` repo clone.
  - This does not prove operational runtime config; live runtime evidence is still required.

- ⏳ **Output parity check against last known-good DFO baseline**
  - No local DFO consumer output baseline artifact is available in this workspace.
  - Requires one live DFO smoke run with baseline comparison artifacts.

## Final gate definition

DFO blocker can be closed only when a live run posts all of:

1. Config evidence showing `http://w3id.org/salmon/` binding in the live consumer runtime.
2. Live smoke execution log (`exit 0`, no critical errors).
3. Output parity artifact comparing live output to last known-good baseline (`pass`).

## Exact final execution runbook

Use:

- `docs/migrations/phase2-dfo-live-smoke-runbook.md`

That runbook defines required inputs, commands, expected outputs, and issue-comment evidence format for the final unblock run.
