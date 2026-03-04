# Phase 2 DFO live smoke runbook (final parity gate)

This runbook is the **exact final execution checklist** to clear the remaining DFO blocker in issue #3.

Use it only in a DFO runtime that can execute the real downstream consumer smoke flow.

## 1) What is already pre-cleared

The following checks are already evidenced from fixture and ontology-level validation:

- Migrated-term presence in shared modules (`salmon:`): **pre-cleared**
- Deferred-profile terms (`ConservationUnit`, `StockManagementUnit`) not promoted into shared core: **pre-cleared**
- Bridge handling safety posture for deferred profile terms: **pre-cleared (fixture)**

Evidence package:

- `docs/migrations/evidence/2026-03-02-dfo-smoke-run.md`
- `docs/migrations/evidence/2026-03-02-phase2-smoke-fixture-results.md`
- `docs/migrations/evidence/2026-03-02-phase2-smoke-fixture-results.json`
- `docs/migrations/evidence/2026-03-02-dfo-live-smoke-prereq-package.md`

## 2) Remaining blocker (must be executed live)

Two checks still require one real DFO consumer run in operational context:

1. Prefix migration check in **actual consumer config/runtime** (`http://w3id.org/salmon/` binding)
2. Output parity check against last known-good DFO output baseline

## 3) Required inputs (fill before starting)

| Input | Value required | Owner |
| --- | --- | --- |
| `DFO_CONSUMER_REPO` | Absolute path to live DFO consumer repo/runtime checkout | DFO smoke-run owner |
| `DFO_SMOKE_CMD` | Exact command used by DFO team to run smoke pipeline (same command family as last known-good) | DFO smoke-run owner |
| `DFO_OUTPUT_ARTIFACT` | Path to generated output artifact from this run (CSV or JSON) | DFO smoke-run owner |
| `DFO_BASELINE_ARTIFACT` | Path to last known-good output artifact for parity comparison | DFO smoke-run owner |
| `SALMON_DOMAIN_REPO` | Absolute path to this repository checkout (`salmon-domain-ontology`) in the runtime environment | DFO smoke-run owner |
| `EVIDENCE_DIR` | Directory where logs/artifacts for this run will be written | DFO smoke-run owner |

## 4) Final live execution commands

> Run in a shell with access to the real DFO consumer runtime.

```bash
set -euo pipefail

# 0) Required vars (populate these exactly for your environment)
: "${DFO_CONSUMER_REPO:?set DFO_CONSUMER_REPO}"
: "${DFO_SMOKE_CMD:?set DFO_SMOKE_CMD}"
: "${DFO_OUTPUT_ARTIFACT:?set DFO_OUTPUT_ARTIFACT}"
: "${DFO_BASELINE_ARTIFACT:?set DFO_BASELINE_ARTIFACT}"
: "${SALMON_DOMAIN_REPO:?set SALMON_DOMAIN_REPO}"
: "${EVIDENCE_DIR:?set EVIDENCE_DIR}"

mkdir -p "$EVIDENCE_DIR"

# 1) Prefix migration check (must find salmon namespace binding)
# Expected: one or more hits containing http://w3id.org/salmon/
grep -RIn "http://w3id.org/salmon/" "$DFO_CONSUMER_REPO" \
  | tee "$EVIDENCE_DIR/01-prefix-binding.txt"

# 2) Execute live DFO smoke command
# Expected: exit code 0 and no critical errors in log
(
  cd "$DFO_CONSUMER_REPO"
  bash -lc "$DFO_SMOKE_CMD"
) 2>&1 | tee "$EVIDENCE_DIR/02-live-smoke.log"

# 3) Capture immutable hashes for generated output and baseline
# Expected: both files exist; SHA256 lines produced
shasum -a 256 "$DFO_OUTPUT_ARTIFACT" | tee "$EVIDENCE_DIR/03-output-sha256.txt"
shasum -a 256 "$DFO_BASELINE_ARTIFACT" | tee "$EVIDENCE_DIR/04-baseline-sha256.txt"

# 4) Header/key parity check (CSV or JSON)
# Expected: script exits 0 and prints "PARITY PASS"
python3 "$SALMON_DOMAIN_REPO"/docs/migrations/evidence/check_dfo_output_parity.py \
  --candidate "$DFO_OUTPUT_ARTIFACT" \
  --baseline "$DFO_BASELINE_ARTIFACT" \
  --out-json "$EVIDENCE_DIR/05-output-parity.json" \
  --out-md "$EVIDENCE_DIR/05-output-parity.md"
```

## 5) Expected outputs to mark PASS

- `01-prefix-binding.txt`: at least one config hit with `http://w3id.org/salmon/`
- `02-live-smoke.log`: smoke command completed (`exit 0`)
- `03-output-sha256.txt` and `04-baseline-sha256.txt`: both artifact hashes captured
- `05-output-parity.md` and `05-output-parity.json`: parity status `pass`

If any expected output is missing, mark result as `FAIL` or `DEFERRED` (with blocker reason).

## 6) Evidence capture format for issue #3

Post one issue comment with this structure:

```markdown
#### DFO live smoke run — <YYYY-MM-DD>
- Owner: <name>
- Runtime: <environment name>
- Build/commit: <ref>
- Smoke command: `<exact command used>`
- Result: PASS | FAIL | DEFERRED
- Pre-cleared checks reused:
  - <link to 2026-03-02-dfo-live-smoke-prereq-package.md>
- Live evidence:
  - <link 01-prefix-binding.txt>
  - <link 02-live-smoke.log>
  - <link 05-output-parity.md>
  - <link 05-output-parity.json>
- Notes: <regressions or none>
```

## 7) Gate decision rule

- Mark issue #3 DFO blocker complete **only when** prefix check and parity check are both `PASS` with live-run artifacts.
- If either is missing, PR #2 remains draft.
