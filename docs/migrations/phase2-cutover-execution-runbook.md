# Phase 2 cutover execution runbook (DFO provider + SPSR consumer)

Status: **historical closeout reference; phase 2 is closed and `0.0.0` is tagged**

This runbook captured the minimum execution contract used to close the phase-2
migration/cutover package. Keep it as the historical record of what cleared the
work and as the template to copy if a similar coordinated cutover is needed
later.

## 1) Scope

- Applied to the phase-2 downstream reality:
  - **DFO** acted as the ontology/provider layer
  - **SPSR** was the operative downstream consumer execution lane
- Covered pre-cutover checks, cutover execution timing, owner assignments, and
  rollback triggers.
- Worked with:
  - `phase2-adoption-checklist.md`
  - `phase2-downstream-smoke-run-templates.md`
  - `phase2-dfo-live-smoke-runbook.md`
  - `phase2-tier3-mapping-triage.md`

## 2) Owner matrix

| Role | Default owner | Responsibility |
| --- | --- | --- |
| Cutover coordinator | Ontology maintainer (`@Br-Johnson`) | Go/no-go facilitation, checklist completion, final cutover note |
| DFO provider verification owner | Ontology maintainer (`@Br-Johnson`) | Record that no separate DFO consumer runtime existed for this phase and attach provider-side evidence |
| SPSR smoke-run owner | SPSR consumer lead (team-assigned at execution time) | Execute SPSR smoke-run template and attach evidence |
| Rollback decision owner | Cutover coordinator + SPSR smoke-run owner | Trigger rollback when blocker criteria are met |

> The key phase-2 reality was simple: SPSR was the live consumer lane, while the
> DFO-side requirement closed through the provider-verification note rather than
> a fictional separate live-runtime smoke run.

## 3) Historical execution sequence (Pacific time)

- Preferred window used for coordination: Tuesday-Thursday, 09:00-12:00.
- Expected duration: 45-60 minutes.
- Freeze period used: no ontology/module edits after T-24h except blocker fixes.

### T-5 business days

- Confirmed merged PR #2 follow-up scope was stable and checklist state was current.
- Confirmed SPSR smoke-run owner and meeting time.
- Confirmed the DFO provider-verification note reflected the no-separate-runtime reality.
- Confirmed Tier-3 triage register carried explicit dispositions.

### T-1 business day

- Dry-ran the SPSR smoke template with representative datasets or controlled fixture data.
- Prepared DFO provider-verification evidence links for issue #3 closure.
- Confirmed rollback contacts were reachable.

### T-0 cutover day

1. Go/no-go checkpoint held.
   - Owner: cutover coordinator
   - Inputs: provider verification note, SPSR smoke evidence, triage register,
     rollback readiness
2. Canonical artifacts and references were published/updated.
   - Owner: ontology maintainer
3. DFO provider verification was recorded and the SPSR smoke run was treated as
   the operative downstream execution proof.
   - Owners: DFO provider verification owner + SPSR smoke-run owner
4. Results were logged in the issue #3 closure package and linked evidence.
   - Owner: cutover coordinator

### T+1 business day

- Verified no post-cutover integration regressions were reported.
- Retired completed blocker checklist items.
- Cut the `0.0.0` pre-alpha stabilization tag from the live namespace state.

## 4) Phase-2 closeout checklist

- [x] Go/no-go call held; SPSR owner present or delegated.
- [x] DFO provider-verification note recorded with evidence link.
- [x] SPSR smoke-run executed with evidence link.
- [x] Tier-3 mapping triage dispositions reviewed and accepted for production posture.
- [x] Publish-ready decision packaged with timestamp and approver before the `0.0.0` stabilization cut.

## 5) Rollback triggers

Rollback was mandatory if any of the following occurred:

1. SPSR smoke run failed on critical query/output paths.
2. DFO provider verification revealed boundary/docs drift that changed cutover
   meaning materially.
3. Tier-3 mapping behavior would require unsafe auto-canonicalization.
4. Broken namespace/prefix resolution in downstream integration scripts.
5. Missing evidence for the DFO provider-verification note or the required SPSR
   smoke run.

## 6) Rollback procedure

1. Announce rollback in the issue #3 closure thread/log immediately.
2. Revert consumer pointers/config to the last known-good release artifact.
3. Mark failed cutover as `deferred` and capture root cause.
4. Open follow-up blocker item with owner + due date before rescheduling.

Rollback completion criteria:

- Previous known-good outputs restored for the operative consumer lane(s).
- New blocker entry and next cutover attempt date recorded.

## 7) Evidence format (required)

Every cutover action included:

- Owner
- Timestamp (Pacific)
- Build target/commit reference
- Evidence link (log, query output, or checklist result)
- Status (`pass`, `fail`, `deferred`)
