# Draft shared terms and bridge for PSC-CV-000035

Prepared 2026-10-28 at Brett's request. This is an unapproved proposal, outside
every ontology import spine, flattened artifact, documentation build and
release. The `smn:` identifiers below are proposed names, not minted terms.
The original PSC definition is retained verbatim in the bridge.

## Recommendation

Reuse the existing NERC/BODC S10 female concept, propose a shared
unspawned-egg adjustment procedure, and consider a shared spawner-abundance
**result class**. Keep the precise EFS variable in the PSC vocabulary and
`smn:Abundance` as its measured characteristic. The result class answers a
different question from the variable: it identifies results about spawners
without declaring all of their underlying quantities interchangeable.

This follows [SDO ADR-0002](../../adr/0002-year-age-basis-dimensions-and-abundance.md):
compound variables remain in a profile, characteristics and result data have
different roles, and procedures remain outside year/age/sex constraints.
The existing [Fraser example](../../../ontology/examples/fraser-stock-recruit-year-age.ttl)
provides the I-ADOPT and SOSA pattern. The live SDO main checked for this
draft is `66571e05a49296688ac60fb6d007671fb06fccbd`.

## Existing sex vocabulary review

| Source | Existing resource and role | Proposed use |
|---|---|---|
| NERC/BODC S10 | `http://vocab.nerc.ac.uk/collection/S10/current/S102/`, female; an accepted, non-deprecated SKOS concept | Reuse the female category as the source of a PSC-scoped I-ADOPT constraint. |
| PATO | `http://purl.obolibrary.org/obo/PATO_0000383`, female; an OWL class of phenotypic sex qualities | Keep as an informative biological reference. Do not assert a SKOS match between this class and a constraint or sex-value concept. |
| Darwin Core | `dwc:sex` and `dwciri:sex`, RDF properties for recording organism sex | Useful field/property bindings, but neither supplies the female value. |

[NERC S102 version 2](https://vocab.nerc.ac.uk/collection/S10/current/S102/2/)
defines a sample containing specimens identified as female. The term is
sample-oriented; applying it to the selected female spawning-stock component
represented by an estimate is a stated **application interpretation**, not an
assertion of equivalence published by NERC. The
[S10 collection](https://vocab.nerc.ac.uk/collection/S10/current/) is maintained
by BODC, published by NERC and licensed CC BY 4.0. Version 2 is dated
2013-11-12. The preserved Turtle receipt is
[`evidence/nerc-s10-s102-v2.ttl`](evidence/nerc-s10-s102-v2.ttl), SHA-256
`b0e884a4593d9791df61f8f1c7dacbe650c90a30637f9e3dbfc1fac6087d35ff`,
retrieved at 2026-10-29T03:38:09Z (2026-10-28 Pacific time).

[PATO's source](https://raw.githubusercontent.com/pato-ontology/pato/master/pato.owl)
was checked at version IRI
`http://purl.obolibrary.org/obo/pato/releases/2026-10-01/pato.owl`; its female
class is under phenotypic sex and the ontology declares CC BY 3.0. The current
[Darwin Core terms](https://dwc.tdwg.org/list/#dwc_sex) describe sex as a
property of an organism; the string-valued and IRI-valued variants were
modified 2026-05-26. None of these observations establishes the sex assessment
method used in an individual PSC dataset.

The bridge uses a local `femaleScope` constraint with `dcterms:source`
pointing to the pinned NERC concept. This records the reused meaning without
asserting that NERC's reusable concept itself constrains every stock node in
every merged variable graph. It also avoids declaring either a replacement
female value or a new shared `FemaleSexConstraint` term. The local constraint
has its own `iadopt:constrains` target. No label or definition is overwritten
on a NERC, PATO or Darwin Core resource. This role separation follows the
[I-ADOPT model](https://i-adopt.github.io/ontology/) and
[SKOS mapping semantics](https://www.w3.org/TR/skos-reference/#mapping).

## Draft term 1: Unspawned-egg adjustment

Proposed IRI: `smn:UnspawnedEggAdjustment`.
Proposed type: `skos:Concept` and `sosa:Procedure`, in `smn:MethodScheme`.

> A calculation procedure that derives effective female spawner abundance by
> reducing estimated female spawner abundance according to the estimated
> proportion of eggs not spawned.

For matching components, `EFS = F × (1 − u) = F × s`, where `u` is the
proportion of eggs not spawned and `s` is the proportion spawned. Partial
spawning contributes proportionally; aggregation must preserve the matching
female-abundance and success estimates. The definition is a proposed synthesis
of [PSC Table 3, page 9](https://www.psc.org/download/130/frp-data/19739/stock-recruit-data-documentation.pdf#page=9)
and [Grant et al. (2011), printed page 27](https://waves-vagues.dfo-mpo.gc.ca/library-bibliotheque/344553.pdf#page=35).
It does not make the 0/50/100 carcass scores described by Grant et al. a
universal requirement for every implementation.

Sampling, expansion, imputation, stock aggregation and uncertainty remain
documented provenance. This calculation does not establish fertilisation,
egg survival, recruitment or genetic effective population size. The procedure
is not a field enumeration method, so the draft does not put it below
`smn:EnumerationMethod` merely to reuse an existing hierarchy.

## Draft term 2: Spawner abundance

Proposed IRI: `smn:SpawnerAbundance`.
Proposed type: an OWL result class under `smn:ObservedRateOrAbundance`.

> A measurement datum recording the abundance of salmon in a declared
> spawning-stage population component for a specified assessment unit and time.

I recommend this class for the competency question: **which results concern
spawners, while retaining their precise variable and adjustment provenance?**
It parallels the existing `smn:CatchAbundance` and `smn:RecruitAbundance`
result classes. The property remains `smn:Abundance`; the proposal does not
create a second characteristic with the same name.

The class leaves sex, origin, jack inclusion, observation boundary and
spawning-success adjustment explicit. It does not assert that all fish
actually spawned. A raw female count and an EFS result can both be instances
without being the same variable or comparable without further checks.
This broad result category is a design proposal supported by the distinctions
in PSC's spawner fields and Grant et al.; it is not a verbatim agency
definition.

The existing [DFO SpawnerAbundance class](https://github.com/dfo-pacific-science/dfo-salmon-ontology/blob/26d7c388a2c97b4098cf267eddca44857f81b36b/ontology/dfo-salmon.ttl)
is a result datum defined around adult salmon reaching spawning grounds. It
supplies useful prior modelling, but its scope is narrower than the proposed
category of declared raw or adjusted components. No equivalence, replacement,
or automatic migration of that DFO term is proposed. Similarly, the
[DFO Pacific glossary](https://www.pac.dfo-mpo.gc.ca/fm-gp/salmon-saumon/gloss-eng.html)
and the Commons' [escapement card](https://github.com/salmon-data-mobilization/salmon-knowledge-commons/blob/main/concepts/escapement-and-spawner-abundance.md)
give reason to state the measurement boundary rather than impose a universal
synonym between escapement and spawner abundance.

## The PSC bridge

[`psc-cv-000035-bridge.ttl`](psc-cv-000035-bridge.ttl) preserves the PSC
definition supplied by Brett exactly, including its EFS prefix. The bridge
adds I-ADOPT variable-instance typing to the PSC SKOS concept in an agency
overlay; it does not turn that identifier into an OWL class or change the
SKOS-only PSC authoring/release contract.

| Role | Binding |
|---|---|
| Exact variable | `PSC-CV-000035`, with the original PSC definition |
| Measured characteristic | A description instance of `smn:Abundance`, also typed `iadopt:Property` |
| Entity role | A schematic production-stock description, typed `smn:Stock` and `iadopt:Entity`; real data binds actual stock identifiers |
| Female scope | A variable-specific `iadopt:Constraint`, sourced to NERC S102 version 2 |
| Fixed contexts | `smn:SpawnerStageContext` and `smn:BroodYearBasis` |
| Row coordinate | `smn:broodYear` with an `xsd:gYear` value |
| Procedure | `sosa:usedProcedure smn:UnspawnedEggAdjustment` on the observation |
| Result category | `smn:SpawnerAbundance` on the result, with the precise variable still linked from the observation |
| Units | Individual/female-equivalent abundance, recorded on results, outside I-ADOPT's component list |

[`example-observations.ttl`](example-observations.ttl) is explicitly synthetic.
It separates an unadjusted female result of 100 from an EFS result of 50 when
the estimated proportion of eggs spawned is 0.5. Both results use the proposed
spawner-abundance result class and the same general characteristic; their
variable identifiers and derivation remain different. This example is not a
reconstruction or validation of any PSC stock-year row.

## Validation and review

Run `python validate-draft.py` from this directory in an environment containing
`rdflib`. The check parses the draft and the pinned NERC receipt, compares the
PSC literal with Brett's supplied text and, when a sibling PSC checkout is
available, its authoring CSV. CI reports whether that additional authoring
comparison was available. The check also
checks component roles and the result/procedure distinction, checks the
synthetic derivation, and rejects cross-kind SKOS matching or class/concept
punning. It also checks that the normative core import closure cannot reach
these proposal files. Mutation controls demonstrate that literal drift,
class/concept punning and replacing EFS with the raw count are rejected.

These are structural and synthetic checks. They are not biological approval,
an exhaustive OWL consistency proof or a release gate. Domain review still
needs to accept the NERC sample-to-population-component interpretation, the
shared procedure's reuse scope, and the proposed result class's boundary.
Only after domain review should the two shared terms enter their owning
modules or the bridge be adopted for production. Merging these proposal
files retains their draft status; it does not admit the terms, assert
biological approval, or add them to the published ontology core.
