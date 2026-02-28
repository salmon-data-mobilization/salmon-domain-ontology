# RDA graph concept coverage (juvenile-condition case study)

## Source artifacts

- GraphML: `mapping-neville-observation.graphml`
  - Drive: <https://drive.google.com/file/d/1-WPKX6XwDiyLGZGT-bcF36N4ankpNi1o/view>
- Context doc: "Juvenile Salmon Condition Case-Study Description"
  - <https://docs.google.com/document/d/1myb-EsbtiJS7-x5wyuzMT9anrQyFC6zELy-WwykChRE/edit>
- Data decomposition folder:
  - <https://drive.google.com/drive/folders/1lM-qrgRib_vob-YEYzpqYqGCG_xBwo1V>

## Coverage result

The yEd graph contains 37 `salmon:` node labels. After this pass, all 37 are represented in the Salmon Domain Ontology codebase as shared terms or profile bridges.

## Shared-layer additions made in this pass

Added to `ontology/modules/02-observation-measurement.ttl`:

1. `salmon:EnumerationMethod` (OWL class)
2. `salmon:NCBITaxon_8018` (OWL class proxy linked to `obo:NCBITaxon_8018`)
3. `salmon:orbitalLength`
4. `salmon:standardLength`
5. `salmon:totalLength`
6. Taxonomy bridge axiom: `obo:NCBITaxon_8018 rdfs:subClassOf obo:NCBITaxon_8015`

## Profile-bridge additions from graph source terms

Added module: `ontology/modules/08-rda-case-study-profile-bridges.ttl`

Mapped Hakai source terms to shared salmon terms using conservative `skos:closeMatch` links:

1. `hakai:Fork_Length_Measurement_Method` -> `salmon:FishForkLengthMeasurementMethod`
2. `hakai:fork_length_measurement_field_method` -> `salmon:ForkLengthMeasurementFieldMethod`
3. `hakai:fork_length_measurement_lab_method` -> `salmon:ForkLengthMeasurementLabMethod`
4. `hakai:Fork_Length_Field_Measurement` -> `salmon:ForkLengthMeasurement`
5. `hakai:Fork_Length_Lab_Measurement` -> `salmon:ForkLengthMeasurement`

## Build wiring

Added case-study build file:

- `ontology/salmon-domain-ontology-rda-case-study.ttl`
  - imports shared base build + module 08 profile bridges

## Boundary posture retained

This pass keeps previously agreed conservative boundaries intact:

- DFO/policy-program specific schemes remain profile-scoped.
- Shared layer remains OWL-centric with a small curated SKOS layer.
- Source/profile terms can be bridged without promoting them into shared core by default.
