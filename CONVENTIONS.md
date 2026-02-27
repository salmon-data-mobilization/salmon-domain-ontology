## Conventions

### Alignment Layers (Top-Down)

```
BFO (Basic Formal Ontology) - Top-Level Ontology
  └── IAO (Information Artifact Ontology)
        └── PROV-O (Provenance Ontology)
              └── SOSA/SSN (Observations & Sensors)
                    └── I-ADOPT (Variable Decomposition)
                          └── Darwin Core (Biodiversity)
                                └── salmon: (Shared Salmon Domain Layer)
```

### Ontology Usage

| Question | Primary Ontology | Secondary |
|----------|------------------|-----------|
| What kind of thing is this? | BFO | - |
| Is this information or physical? | IAO | BFO |
| Who/what produced this data? | PROV-O | - |
| How was this measured? | SOSA/SSN | PROV-O |
| What property was measured? | I-ADOPT | SOSA |
| How do I publish to GBIF? | Darwin Core | SOSA |
| What constraints apply? | I-ADOPT | `salmon:` SKOS |

### Standard Prefixes

```turtle
@prefix salmon: <http://w3id.org/salmon/> .
@prefix bfo:    <http://purl.obolibrary.org/obo/BFO_> .
@prefix iao:    <http://purl.obolibrary.org/obo/IAO_> .
@prefix prov:   <http://www.w3.org/ns/prov#> .
@prefix sosa:   <http://www.w3.org/ns/sosa/> .
@prefix ssn:    <http://www.w3.org/ns/ssn/> .
@prefix iop:    <https://w3id.org/iadopt/ont/> .
@prefix dwc:    <http://rs.tdwg.org/dwc/terms/> .
@prefix dwciri: <http://rs.tdwg.org/dwc/iri/> .
@prefix qudt:   <http://qudt.org/schema/qudt/> .
@prefix unit:   <http://qudt.org/vocab/unit/> .
@prefix qk:     <http://qudt.org/vocab/quantitykind/> .
```

### Rules of Thumb

- **Check `salmon:` first** for reusable salmon-domain concepts.
- Use **external standards** (SOSA, I-ADOPT, Darwin Core, QUDT, etc.) where they are clearly canonical.
- **Never invent IRIs casually**; document gaps and open issues when terms are missing.
- Use **QUDT units** consistently (`http://qudt.org/vocab/unit/`).

### BFO Alignment Guidance

| `salmon:` class type | BFO alignment | Example |
|----------------------|---------------|---------|
| Physical entities (salmon, samples) | `bfo:0000040` (material entity) | `salmon:SalmonSpecimen rdfs:subClassOf bfo:0000040` |
| Qualities/properties | `bfo:0000019` (quality) | `salmon:ForkLength rdfs:subClassOf bfo:0000019` |
| Roles | `bfo:0000023` (role) | `salmon:BreederRole rdfs:subClassOf bfo:0000023` |
| Processes/activities | `bfo:0000015` (process) | `salmon:SpawningEvent rdfs:subClassOf bfo:0000015` |
| Temporal regions | `bfo:0000008` (temporal region) | Return-year interval |

### I-ADOPT Variable Decomposition

Variables should be decomposed with I-ADOPT components:

| Component | Class IRI | Description |
|-----------|-----------|-------------|
| **Variable** | `iop:Variable` | The complete observable property |
| **Property** | `iop:Property` | The characteristic being measured |
| **ObjectOfInterest** | `iop:ObjectOfInterest` | Primary entity being observed |
| **ContextObject** | `iop:ContextObject` | Additional contextual entity |
| **Matrix** | `iop:Matrix` | Medium or environment |
| **Constraint** | `iop:Constraint` | Limits scope of observation |

### Darwin Core Usage

Darwin Core is an interoperability scaffold. Use:
- `dwc:` when objects are literals
- `dwciri:` when objects are IRIs (controlled vocab references)

### Scope

This ontology is the shared interoperability layer for salmon data across organizations and jurisdictions. Keep class/property names broadly reusable. Agency-specific governance or implementation details should remain in separate profile ontologies that import this shared layer.
