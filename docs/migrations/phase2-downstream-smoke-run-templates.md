# Phase 2 downstream evidence templates (DFO provider + SPSR consumer)

Use these templates to produce minimum publish-ready evidence for issue #3.

## 1) Evidence requirements

For each evidence note, record:

- owner
- date/time (Pacific)
- build target (file/branch/commit)
- dataset/input used (if applicable)
- pass/fail per checkpoint
- links to logs/screenshots/query outputs

Paste completed records as comments on issue #3.

---

## 2) DFO provider-verification template

Use this template when there is **no separate DFO downstream consumer runtime**
for the current phase. It replaces the old live-smoke expectation.

### Metadata

| Field | Value |
| --- | --- |
| Owner |  |
| Date/time (PT) |  |
| Build target | `ontology/salmon-domain-ontology.ttl` (or case-study build if used) |
| Branch/commit |  |
| Environment | DFO provider / ontology-maintainer context |

### Checklist

- [ ] **No-runtime confirmation**: no separate DFO downstream consumer runtime/check-out/baseline artifact exists for this phase.
- [ ] **Boundary alignment check**: DFO docs/provider references align to `smn:` shared terms and `gcdfo:` DFO-specific/profile terms.
- [ ] **Route-contract anchor check**: merged SPSR PR #247 is linked as the canonical machine-readable route-contract evidence; closed DFO PR #54 is treated only as transfer/pointer context if referenced.
- [ ] **Fixture evidence retention check**: existing prereq/fixture evidence is retained as non-live supporting evidence.
- [ ] **Consumer-lane handoff check**: SPSR remains the operative downstream smoke lane for this phase.

### Result block (paste in issue #3)

```markdown
#### DFO provider verification — <date>
- Owner: <name>
- Build/commit: <ref>
- Result: PASS | FAIL
- Evidence:
  - <link to prereq package>
  - <link to SPSR PR #247 or merged artifact>
  - <link to SPSR smoke evidence comment>
- Notes: No separate DFO downstream consumer runtime exists for this phase, so the former live-smoke gate is not applicable.
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

- [ ] **Prefix/query update check**: SPSR query/report layer uses `smn:` canonical terms.
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

- If the **SPSR** live execution lane is unavailable, use a controlled fixture
  dataset and mark result as `DEFERRED` only when blocked by external
  environment constraints (not by missing prep).
- If a **separate DFO downstream runtime does not exist at all**, do **not**
  fabricate a deferred live run. Record the DFO provider-verification note
  instead.

Required for deferred SPSR runs:

- explicit blocker reason
- owner for unblock action
- next execution date
