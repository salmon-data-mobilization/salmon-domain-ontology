# Wave 1 term inventory (gcdfo -> salmon)

## Scope rule used

- Conservative default: if uncertain, keep term in profile scope first.
- Migrate only terms with clear cross-agency reuse and policy-neutral semantics.
- Keep DFO/program-specific SKOS schemes and policy status vocabularies out of shared core.

## Migrated in wave 1 (shared layer)

See machine-readable map: `gcdfo-to-salmon-wave1.csv` (rows with `status=migrated`).

Representative migrated set:

- Shared biological/reporting anchors: `Stock`, `Population`, `Deme`, `IndicatorRiver`
- Shared event/measurement semantics: `SurveyEvent`, `Escapement`, `EscapementMeasurement`
- Shared quantitative semantics: `ExploitationRate`, `TotalExploitationRate`
- Shared generic benchmark abstractions: `ReferencePoint`, `MetricBenchmark` family
- Shared curated SKOS layer: context, life-phase, and origin concepts only

## Deferred to profile scope (wave 1)

See `status=deferred_profile` rows in `gcdfo-to-salmon-wave1.csv`.

Deferred groups include:

- DFO-specific governance units (`ConservationUnit`, `StockManagementUnit`)
- WSP-specific classes/concepts and confidence/status schemes
- Policy framework concepts/schemes
- Enumeration, estimate method, estimate type, downgrade criteria SKOS families
- Benchmark-level SKOS scheme and its member concepts

## Non-destructive migration stance

No term removals are made in `dfo-salmon-ontology` during wave 1.
DFO remains intact while shared/profile boundaries are hardened in salmon-domain.
