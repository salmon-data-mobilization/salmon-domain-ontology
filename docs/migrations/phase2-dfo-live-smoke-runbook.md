# Phase 2 DFO provider verification note (supersedes final live smoke gate)

This document records the phase-2 cutover reality check for the DFO side:
there is **no separate DFO downstream consumer runtime/check-out/baseline
artifact currently available** for this migration wave.

Because of that, the previous "final live DFO smoke gate" cannot be satisfied
honestly and is **superseded** by an explicit provider-verification note in
issue #3.

## 1) What is already pre-cleared

The following checks are already evidenced from fixture and ontology-level
validation:

- Migrated-term presence in shared modules (`smn:`): **pre-cleared**
- Deferred-profile terms (`ConservationUnit`, `StockManagementUnit`) not
  promoted into shared core: **pre-cleared**
- Bridge handling safety posture for deferred profile terms:
  **pre-cleared (fixture)**

Evidence package:

- `docs/migrations/evidence/2026-03-02-dfo-smoke-run.md`
- `docs/migrations/evidence/2026-03-02-phase2-smoke-fixture-results.md`
- `docs/migrations/evidence/2026-03-02-phase2-smoke-fixture-results.json`
- `docs/migrations/evidence/2026-03-02-dfo-live-smoke-prereq-package.md`

## 2) Reality check (authoritative as of 2026-03-13)

The former live-smoke gate assumed assets that do not actually exist in the
current cutover context:

- no separate DFO downstream consumer repo/runtime has been identified
- no authoritative DFO smoke command exists for a separate consumer pipeline
- no last-known-good DFO output artifact exists for parity comparison
- browser/public-repo inspection cannot manufacture missing operational evidence

Therefore a required PASS based on a fictional runtime would be fabricated and
should not remain in the gate contract.

## 3) Replacement gate for issue #3

Instead of demanding nonexistent live-runtime artifacts, issue #3 should require
all of the following:

1. **DFO provider verification note**
   - explicitly state that no separate DFO downstream consumer runtime exists
     for this phase
   - confirm DFO provider-side docs/route-bundle references align to the locked
     boundary: `smn:` shared layer, `gcdfo:` DFO-specific/profile layer
   - confirm the canonical machine-readable route-contract home is merged **SPSR
     PR #247**, with closed DFO PR #54 treated only as the transfer/pointer
     trail (not the enduring evidence anchor)
2. **Pre-cleared fixture/prereq evidence retained**
   - keep the existing prerequisite package linked; do not pretend it is a live
     consumer run
3. **SPSR remains the operative downstream consumer smoke lane**
   - SPSR smoke evidence remains the real downstream-consumer execution proof
     for this phase
4. **Final go/no-go note still required**
   - issue #3 must still carry an explicit cutover decision with timestamp and
     owner

## 4) Minimum evidence package for closure

The replacement DFO-side closure package is:

- the provider-verification issue note described below
- `docs/migrations/evidence/2026-03-02-dfo-live-smoke-prereq-package.md`
- the SPSR smoke evidence comment/artifacts already linked in issue #3
- merged SPSR route-contract evidence (PR #247), with DFO PR #54 retained only as the closed transfer/pointer trail if needed
- final issue #3 go/no-go note

## 5) Provider-verification note template for issue #3

```markdown
#### DFO provider verification — <YYYY-MM-DD>
- Owner: <name>
- Result: PASS | FAIL
- Statement: No separate DFO downstream consumer runtime/check-out/baseline artifact exists for this phase-2 cutover, so the former live DFO smoke gate is not applicable.
- Provider-side checks:
  - DFO docs/route bundle align to `smn:` shared / `gcdfo:` DFO-specific boundary
  - merged SPSR PR #247 serves as the canonical route-contract/provider-side evidence anchor; closed DFO PR #54 is only transfer/pointer context if cited
  - Existing DFO prerequisite/fixture evidence is retained as non-live supporting evidence only
  - SPSR remains the operative downstream consumer smoke lane for this phase
- Evidence:
  - <link to prereq package>
  - <link to SPSR PR #247 or merged artifact>
  - <link to SPSR smoke evidence comment>
- Notes: <regressions or none>
```

## 6) Gate decision rule

- Do **not** require fabricated DFO live-smoke artifacts when no separate DFO
  downstream consumer runtime exists.
- Close the former DFO blocker when the provider-verification note is recorded
  in issue #3 and the SPSR downstream smoke evidence remains intact.
- Final cutover still requires an explicit go/no-go note in issue #3.
