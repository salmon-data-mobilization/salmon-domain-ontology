# Wave 1 term inventory (gcdfo -> salmon)

## Scope rule used

- Migrated: terms that are reusable across organizations, jurisdictions, and salmon assessment programs.
- Deferred: terms that are DFO-admin-specific or require governance confirmation before re-homing.

## Migrated in wave 1

See the machine-readable map: `gcdfo-to-salmon-wave1.csv`.

Priority examples migrated:

- `ExploitationRate`, `TotalExploitationRate`
- `Escapement`, `EscapementSurveyEvent`, `EscapementMeasurement`
- `ConservationUnit`, `StockManagementUnit`, `Population`, `Stock`
- `LowerBenchmark`, `UpperBenchmark`
- `EnumerationMethodScheme`, `EstimateMethodScheme`, `EstimateTypeScheme`

## Deferred (explicitly not moved in this wave)

- DFO-specific implementation and governance metadata that still require profile-layer treatment.
- Terms with unresolved semantic boundaries (for example, where policy framing and jurisdiction-specific legal interpretation are tightly coupled).

## Non-destructive migration stance

No term removals are made in `dfo-salmon-ontology` during wave 1.
The DFO ontology remains intact while this reusable layer is built out in `salmon-domain-ontology`.
