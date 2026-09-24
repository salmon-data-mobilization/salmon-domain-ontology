# Annotation Gap Ledger

Purpose: track unresolved annotation-completeness gaps in the Salmon Domain Ontology without inventing new definitions, sources, or ownership assertions.

## Ground rules

- Do **not** invent definitions or provenance just to satisfy a checklist.
- For migrated/shared terms, reuse existing wording exactly when authoritative text already exists.
- For imported external terms, prefer source-owned annotations or explicit exclusion from local completeness checks rather than hand-authoring local wording.
- `rdfs:comment` is for editorial scope notes / mapping rationale, not the primary definition field.

## Scope of this ledger

Current counts below cover **local typed terms in `ontology/modules/*.ttl`** with `smn:` / `smn/profile/...` IRIs:
- OWL classes / properties / annotation properties
- SKOS concepts / concept schemes

Imported external IRIs are intentionally out of scope for these counts.

## Current status (2026-05-13)

- Missing `rdfs:isDefinedBy`: **0**
- Missing definitions: no longer counted here; see [Definition gaps](#definition-gaps)
- Missing provenance (`iao:0000119` / `dcterms:source`): **50**

## 2026-05-13 backfill note

Source-backed provenance was backfilled only where the term could be tied to a prior GCDFO Salmon Ontology release, the RDA case-study source sheet, or the Hakai GraphML source already used by the profile bridge modules.

No new definition was added where the only available text was inferred, generalized beyond the source term, or not present in the checked GCDFO/RDA/Hakai sources.

## Definition gaps

This ledger no longer keeps that list. It lives in
[`ontology/definition-exemptions.csv`](https://github.com/salmon-data-mobilization/salmon-domain-ontology/blob/main/ontology/definition-exemptions.csv):
one row per local term with no definition, and each row names the item that will
write the definition or delete the term. The ids are items in the
[metasalmon hub queue](https://github.com/salmon-data-mobilization/metasalmon/tree/main/queue/items),
where cross-vocabulary work is sequenced.

`make verify-term-definitions`, part of `make test` and of CI, holds the file to
the ontology in both directions. It fails on a local term with no definition and
no row, so a new gap cannot go unrecorded. It also fails on a row whose term now
has a definition or is no longer a local term, so the change that closes a gap
deletes its row too, and a row cannot outlive the gap it records. The definition
must be in the property CONVENTIONS section 10 names for the term's kind:
`skos:definition` for a SKOS concept or scheme, `iao:0000115` for an OWL class
or property.

The ground rules above still govern how a gap is closed.

## Provenance gaps by module

### `ontology/modules/01-entity-systematics.ttl`
- `Entity`
- `GeographicFeature`
- `HabitatUnit`
- `SalmonGroup`
- `SalmonIndividual`
- `SalmonPopulationGroup`
- `SalmonStockUnit`
- `hasPopulation`
- `populationOf`

### `ontology/modules/02-observation-measurement.ttl`
- `AggregatedMeasurement`
- `BodyShape`
- `Characteristic`
- `FishForkLengthMeasurementMethod`
- `FishLength`
- `FishLengthMeasurementMethod`
- `FishLengthMeasurementType`
- `FishWeight`
- `ForkLengthMeasurement`
- `ForkLengthMeasurementFieldMethod`
- `ForkLengthMeasurementLabMethod`
- `ForkLengthMeasurementMethod`
- `IndividualMeasurement`
- `Life-HistoryCharacteristic`
- `Measurement`
- `ModelMeasurement`
- `MorphologicalCharacteristic`
- `NCBITaxon_8018`
- `Observation`
- `Run`
- `SalmonLifeStage`
- `SamplingEvent`
- `StandardLengthMeasurement`
- `TotalLengthMeasurement`
- `alevin`
- `basedOn`
- `characteristicFor`
- `forkLength`
- `fusiform`
- `hasEventType`
- `hasMeasurement`
- `observedTaxonFamily`
- `observedTaxonSpecies`
- `orbitalLength`
- `standardLength`
- `totalLength`

### `ontology/modules/04-management-governance.ttl`
- `EventType`
- `FishingType`
- `seiningEvent`

### `ontology/modules/05-provenance-quality.ttl`
- `DataQualityAssessment`
- `MethodDocumentation`
