# Phase 2 boundary rules (shared `salmon:` vs profile vocabularies)

This document is the operational boundary contract for migration phase 2.

## 1) Goal

Keep the shared `salmon:` layer stable for cross-organization reuse while preserving program/policy specificity in profile namespaces.

Conservative default: **if uncertain, keep terms in profile scope and bridge to shared anchors**.

## 2) Scope boundary (authoritative for phase 2)

### In shared `salmon:` scope

- Policy-neutral domain classes/properties reused across organizations
- Shared event and measurement semantics (`SurveyEvent`, `EscapementMeasurement`, etc.)
- Shared benchmark abstractions (`ReferencePoint`, `MetricBenchmark` family)
- Small curated cross-agency SKOS concepts/schemes only

### Out of shared scope (profile-only in phase 2)

- DFO/WSP policy-program schemes and statuses
- Program-specific method, estimate type, and downgrade criteria vocabularies
- DFO governance units currently deferred (`ConservationUnit`, `StockManagementUnit`)
- Any concept whose semantics depend on a single agency policy framework

## 3) Promotion rules (profile -> shared)

Promote a term to shared only when all are true:

1. Multi-agency reuse is expected in active integrations.
2. Semantics are stable across organizations.
3. Meaning is not policy-program specific.
4. Promotion yields concrete interoperability benefit.

If any criterion fails, keep profile-scoped and map conservatively.

## 4) Mapping strength and automation safety

- **Tier 1 (automation-safe):** `owl:equivalentClass`, `owl:equivalentProperty`, `owl:sameAs`, `rdfs:subClassOf`, `rdfs:subPropertyOf`
- **Tier 2 (strong conceptual):** `skos:exactMatch`
- **Tier 3 (advisory):** `skos:closeMatch`, `skos:broadMatch`, `skos:narrowMatch`, `skos:relatedMatch`

Operational gate: Tier 3 mappings are **not** auto-canonicalized into production integration without explicit review/promotion.

## 5) Current wave 1/2 boundary decisions carried forward

- Remain shared: `Stock`, `IndicatorRiver`, core biological + measurement abstractions
- Remain profile-scoped: WSP status/confidence schemes, policy framework terms, enumeration/estimate/benchmark-level families
- Source ontology remains non-destructive during migration (no removals in DFO source as part of this phase)

See machine map: `gcdfo-to-salmon-wave1.csv`.

## 6) Change-control path for boundary exceptions

1. Open an issue with:
   - proposed move (profile -> shared or shared -> profile)
   - consumer impact (DFO and SPSR)
   - mapping predicate and confidence rationale
2. Update migration map + affected module(s).
3. Add release-readiness impact note before cutover.
4. Merge only after reviewer sign-off on boundary risk.
