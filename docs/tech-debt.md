# Tech Debt Log

This file tracks technical debt with rationale, impact, and remediation notes. Keep it current as debt is identified, addressed, or becomes obsolete.

## Active Technical Debt

### 2026-09-15 — Nine asserted superclass IRIs are neither declared nor vendored

**Description**: `make verify-superclass-declarations` (hub item B-143) is red over
`ontology/modules/` as it stands. Nine IRIs are asserted as superclasses while
nothing in `ontology/modules/` or `ontology/imports/` declares them as classes.
Measured 2026-09-15 at `d45f8f7`; the script prints the live list, and the
Makefile target is deliberately kept out of `make test` until the list is empty.

Two distinct shapes, and they need different remedies:

| IRI | Asserted at | Shape |
|---|---|---|
| `sosa:Property` | `02-observation-measurement.ttl:28` (`smn:Characteristic`) | **Wrong term.** `sosa:` *is* vendored and this IRI is absent from it; SOSA publishes `sosa:ObservableProperty`, which `ontology/imports/sosa.ttl` declares. Hub item B-107. |
| `obo:BFO_0000015` | `02-…:216` (`smn:Escapement`), `03-…:53` (`smn:StockAssessment`) | Namespace not vendored |
| `obo:IAO_0000030` | `01-…:69`, `03-…:65,82`, `05-…:13,19` (5 subjects) | Namespace not vendored |
| `obo:IAO_0000109` | `02-…:241`, `03-…:18,45` (3 subjects) | Namespace not vendored |
| `obo:NCBITaxon_8015` | `02-…:202` (MIREOT mirror) | Namespace not vendored |
| `obo:NCBITaxon_8018` | `02-…:206` (`smn:NCBITaxon_8018`) | Namespace not vendored |
| `dwc:Event` | `02-…:224` (`smn:SurveyEvent`) | Namespace not vendored |
| `dwc:Organism` | `01-…:86,94` (`smn:Deme`, `smn:Population`) | Namespace not vendored |
| `geosparql:Feature` | `01-…:59` (`smn:GeographicFeature`) | Namespace not vendored |

The split is measurable rather than a judgement call. This repository declares
13 IRIs in the `sosa:` namespace (it is vendored) and **zero** in each of
`http://purl.obolibrary.org/obo/`, `http://rs.tdwg.org/dwc/terms/` and
`http://www.opengis.net/ont/geosparql#`. A typo needs a correct neighbour to be
a typo of, and in those three namespaces there is no declared neighbour at all.

A further six undeclared IRIs sit in `rdfs:domain`/`rdfs:range` position rather
than superclass position and are **not** covered by the gate as scoped:
`obo:IAO_0000104`, `obo:NCBITaxon_8015`, `obo:NCBITaxon_8018`,
`dwc:MaterialEntity`, `xsd:gYear`, and `sosa:Property` again (at
`02-observation-measurement.ttl:282`, `smn:characteristicFor rdfs:domain`, the
second half of the B-107 defect). `xsd:gYear` is a datatype rather than a class
and is correct there; the other five are the same debt in a different position.

**Rationale**: The build never checked this. ELK treats an un-axiomatised IRI as
a class about which nothing is known, so the closure stays consistent, no class
is unsatisfiable, and `make verify-reasoner` passes over every one of these —
verified 2026-09-15 by running the reasoner gate against a deliberately broken
module and watching it pass green. `sosa:Property` therefore sat under
`smn:Characteristic` from 2026-08-10 to 2026-09-14 through every CI run.

**Impact**:
- **Severity**: Medium
- **Affected Areas**: the published class hierarchy; anything reasoning over or rendering `smn:` superclasses
- **User Impact**: a consumer resolving an asserted superclass gets nothing back, so the hierarchy is narrower than it reads
- **Maintenance Cost**: low while staged; the gate reports the list on every `make test`

**Remediation**:
- **Effort Estimate**: Small per IRI; the decision is the work, not the edit
- **Approach**: for `sosa:Property`, B-107's ruled replacement with `sosa:ObservableProperty`. For the other eight, either vendor the namespace under `ontology/imports/` or add a bare declaration stub, which CONVENTIONS 5b rule 2 permits anywhere. Which of the two is a modelling decision and was deliberately left open by B-143, which is structural and carries no term ruling.
- **Prerequisites**: B-107 is blocked on smn pull request #27, which edits the same module and regenerates the docs artifacts
- **Risk**: low; each remedy is additive

**Status**: Active — gate landed and staged, backlog recorded, none of the nine resolved

**Related Issues/PRs**:
- `scripts/verify_superclass_declarations.py` (`KNOWN_UNDECLARED` is the machine-readable copy of this table)
- `Makefile` (`verify-superclass-declarations`, `verify-superclass-declarations-staged`)
- hub queue items B-143 (this gate) and B-107 (`sosa:Property`); smn PR #27

### 2026-03-15 — WIDOCO changelog rendering errors on complex restrictions

**Description**: `docs-widoco` can emit `OntologyDifferencesRenderer` errors for several `SubClassOf` restrictions whose fillers are property restrictions rather than OWL classes in import chain assertions.

**Rationale**: This currently does not fail generation, but it degrades changelog readability and creates recurring false signals in CI logs.

**Impact**:
- **Severity**: Low
- **Affected Areas**: changelog artifact and release-note quality
- **User Impact**: no functional breakage; reduced trust in automatically generated release diffs
- **Maintenance Cost**: ongoing log triage

**Remediation**:
- **Effort Estimate**: Medium
- **Approach**: keep changelog generation off by default or post-filter known-safe warnings once WIDOCO behavior is updated
- **Prerequisites**: decision whether changelog is required for this ontology's release rhythm
- **Risk**: low to medium

**Status**: Active

**Related Issues/PRs**:
- `Makefile`
- `docs/context/widoco.md`

## Resolved Technical Debt

### 2026-03-15 — External SOSA/DWC protocol bridge no longer emits docs-refresh serialization noise

**Resolved Date**: 2026-03-15
**Resolution**: replaced the `sosa:ObservingProcedure owl:equivalentClass dwc:Protocol` axiom in `ontology/modules/06-data-interoperability.ttl` with a documentation-level bridge (`rdfs:comment` + `rdfs:seeAlso` to `dwc:protocol` and `dwcdp:Protocol`). `make docs-refresh` now completes without the previous ROBOT conversion warning.
**Lessons Learned**: publication-oriented interoperability hints belong in documentation-level or annotation-level bridges unless both sides are clean OWL classes with compatible semantics.

### 2026-03-15 — Migration scaffolding for build/verify docs path is in place

**Resolved Date**: 2026-03-15
**Resolution**: build flow now has scripted split-module composition + flat TTL generation for deterministic source updates before docs refresh.
**Lessons Learned**: explicit composition scripts lower the risk of manual drift when the case-study modules are touched.
