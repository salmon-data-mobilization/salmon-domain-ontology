# Phase 2 downstream smoke-run templates (DFO + SPSR)

Use these templates to produce minimum publish-ready evidence for issue #3.

## 1) Evidence requirements (both consumers)

For each smoke run, record:

- owner
- date/time (Pacific)
- build target (file/branch/commit)
- dataset/input used
- pass/fail per checkpoint
- links to logs/screenshots/query outputs

Paste completed records as comments on issue #3.

---

## 2) DFO smoke-run template

### Metadata

| Field | Value |
| --- | --- |
| Owner |  |
| Date/time (PT) |  |
| Build target | `ontology/salmon-domain-ontology.ttl` (or case-study build if used) |
| Branch/commit |  |
| Dataset/input snapshot |  |
| Environment |  |

### Checklist

- [ ] **Prefix migration check**: consumer configs bind shared namespace to `http://w3id.org/salmon/`.
- [ ] **Migrated-term check**: at least 3 `status=migrated` terms from `gcdfo-to-salmon-wave1.csv` resolve in pipeline/query output.
- [ ] **Deferred-profile check**: at least 2 `status=deferred_profile` terms remain profile-resolved (not promoted to shared).
- [ ] **Bridge handling check**: profile bridge terms are accepted without forcing canonical promotion.
- [ ] **Output parity check**: key output fields match expected structure from last known-good run.

### Minimum query/inspection set (recommended)

1. One class/entity lookup (example: `salmon:Stock` or `salmon:ReportingOrManagementStratum`).
2. One event/measurement lookup (example: `salmon:SurveyEvent`, `salmon:EscapementMeasurement`).
3. One deferred profile term path (example: `ConservationUnit` or `StockManagementUnit`) proving profile-only handling still works.

### Result block (paste in issue #3)

```markdown
#### DFO smoke run — <date>
- Owner: <name>
- Build/commit: <ref>
- Dataset: <ref>
- Result: PASS | FAIL | DEFERRED
- Evidence:
  - <link 1>
  - <link 2>
- Notes: <regressions or none>
```

---

## 3) SPSR smoke-run template

### Metadata

| Field | Value |
| --- | --- |
| Owner |  |
| Date/time (PT) |  |
| Build target | `ontology/salmon-domain-ontology-rda-case-study.ttl` (if bridge terms required) |
| Branch/commit |  |
| Dataset/input snapshot |  |
| Environment |  |

### Checklist

- [ ] **Prefix/query update check**: SPSR query/report layer uses `salmon:` canonical terms.
- [ ] **Bridge resolution check**: at least 2 bridge mappings from modules 08/09 resolve in query results.
- [ ] **Tier-3 safety check**: Tier-3 mappings are treated as advisory (no automatic production canonicalization).
- [ ] **Report continuity check**: one end-to-end report/extract completes with expected key metrics.
- [ ] **Regression scan**: no critical missing fields, null spikes, or join failures in core report outputs.

### Minimum query/inspection set (recommended)

1. One shared-term report path (e.g., stock/stratum aggregation).
2. One bridge-dependent report path (Hakai/Neville mapped measurement concept).
3. One Tier-3 advisory path confirming no auto-promotion behavior.

### Result block (paste in issue #3)

```markdown
#### SPSR smoke run — <date>
- Owner: <name>
- Build/commit: <ref>
- Dataset: <ref>
- Result: PASS | FAIL | DEFERRED
- Evidence:
  - <link 1>
  - <link 2>
- Notes: <regressions or none>
```

---

## 4) If live execution is unavailable

Use a controlled fixture dataset and run the same checklist. Mark result as `DEFERRED` only when blocked by external environment constraints (not by missing prep).

Required for deferred runs:

- explicit blocker reason
- owner for unblock action
- next execution date
