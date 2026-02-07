## Conventions

### Namespace

The canonical namespace for salmon-domain semantics is `http://w3id.org/salmon/` (prefix `salmon:`).

Note: We are **not** using the GCDFO namespace in this project. Keep names stable and avoid introducing a second competing namespace. External IRIs are used for alignment, decomposition parts, or broadly reusable concepts.

### Alignment Hierarchy (Top-Down)

```
BFO (Basic Formal Ontology) - Top-Level Ontology
  └── IAO (Information Artifact Ontology)
        └── PROV-O (Provenance Ontology)
              └── SOSA/SSN (Observations & Sensors)
                    └── I-ADOPT (Variable Decomposition)
                          └── Darwin Core (Biodiversity)
                                └── salmon: (Salmon Domain)
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
| What constraints apply? | I-ADOPT | gcdfo: SKOS |

### Standard Prefixes

```turtle
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
@prefix salmon: <http://w3id.org/salmon/> .
```

### Rules of Thumb

- **Check `gcdfo:` first**; reuse an existing term when it fits.
- **Prefer well-governed external vocabularies** when the concept is cross-domain and widely standardized.
- **Never invent IRIs**; if you cannot find a suitable term, document the gap.
- Use **QUDT units** (`http://qudt.org/vocab/unit/`) consistently for all units of measure.

### BFO Alignment Guidance

| gcdfo: Class Type | BFO Alignment | Example |
|-------------------|---------------|---------|
| Physical entities (salmon, samples) | `bfo:0000040` (material entity) | `gcdfo:SalmonSpecimen rdfs:subClassOf bfo:0000040` |
| Qualities/properties | `bfo:0000019` (quality) | `gcdfo:ForkLength rdfs:subClassOf bfo:0000019` |
| Roles | `bfo:0000023` (role) | `gcdfo:BreederRole rdfs:subClassOf bfo:0000023` |
| Processes/activities | `bfo:0000015` (process) | `gcdfo:SpawningEvent rdfs:subClassOf bfo:0000015` |
| Temporal regions | `bfo:0000008` (temporal region) | Return year spans |

### I-ADOPT Variable Decomposition

Variables should be decomposed using I-ADOPT components:

| Component | Class IRI | Description |
|-----------|-----------|-------------|
| **Variable** | `iop:Variable` | The complete observable property |
| **Property** | `iop:Property` | The characteristic being measured |
| **ObjectOfInterest** | `iop:ObjectOfInterest` | Primary entity being observed |
| **ContextObject** | `iop:ContextObject` | Additional contextual entity |
| **Matrix** | `iop:Matrix` | Medium or environment |
| **Constraint** | `iop:Constraint` | Limits scope of observation |

### Darwin Core Usage

Darwin Core is best treated as an **interoperability scaffold**. Use `dwc:` terms when the column is intended to be the Darwin Core property. In RDF:
- `dwc:` terms generally have literal objects
- `dwciri:` terms are used when the object is an IRI (e.g., controlled-vocabulary values)

### Scope

This ontology captures salmon-related terms intended for broad reuse across agencies, organizations, projects, and datasets to maximize interoperability. Keep class/property names and alignments consistent with the chosen upper ontologies; document any exceptions inline.
