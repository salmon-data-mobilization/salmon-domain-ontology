# Phase-2 downstream smoke fixture evidence (2026-03-02)

Local fixture execution using workspace assets only.

## DFO consumer smoke-run
Overall: **PARTIAL**

- ✅ **Migrated-term check** (PASS): 3/3 sampled migrated terms resolve in shared modules: ReportingOrManagementStratum, Stock, Deme
- ✅ **Deferred-profile check** (PASS): ConservationUnit + StockManagementUnit are not promoted into shared salmon: namespace.
- ✅ **Bridge handling check** (PASS): Deferred-profile terms remain consumable in local templates (ConservationUnit rows=125, StockManagementUnit rows=84).
- ⏳ **Prefix migration check** (GAP): No local DFO consumer asset in dfo-salmon-ontology currently references w3id.org/salmon/. DFO live consumer config is external/not present in this workspace.
- ⏳ **Output parity check** (GAP): No local DFO consumer run artifact baseline was available to compare field-level output parity. Requires DFO consumer execution output from the operational environment.

## SPSR consumer smoke-run
Overall: **CLEARED**

- ✅ **Prefix/query update check** (PASS): SPSR namespace bridge map contains 7 explicit migrated gcdfo→salmon mappings.
- ✅ **Bridge resolution check** (PASS): 27 bridge mappings resolve to shared typed targets (sample: AggregatedMeasurement, GeographicFeature, Observation).
- ✅ **Tier-3 safety check** (PASS): No owl:equivalentClass / owl:equivalentProperty / skos:exactMatch assertions in bridge modules 08/09.
- ✅ **Report continuity + regression scan** (PASS): Targeted SPSR smoke tests passed (4/4).

## Artifact pointers
- JSON detail: `docs/migrations/evidence/2026-03-02-phase2-smoke-fixture-results.json`
- SPSR test log: `docs/migrations/evidence/2026-03-02-spsr-smoke-managepy-tests.log`
