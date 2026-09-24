---
type: InformationObject
title: OWL/SKOS conventions — stated vs practiced
description: Where the repository's modelling practice diverges from CONVENTIONS.md, with the eight adversarially verified metamodel findings (F1–F8) from the 2026-08-12 recon and the upstream-spec facts they rest on.
status: draft
tags: [owl, skos, conventions, metamodel, iadopt, sosa]
psc:
  id: smn:data:owl-skos-conventions-state
  contexts: [smn:context:ontology-alignment-pass-2026]
---

Originally verified 2026-08-12 (main at `3995a17`); inventory refreshed
2026-08-13 after S9 steps 1/2/5 landed. Fix plan: step 1 of
`metasalmon/knowledge/plans/2026-08-12-ontology-alignment-pass.md`.

## What holds

- File-level OWL/SKOS separation is clean: modules 01–05 pure OWL, module
  07 pure SKOS (**10 schemes, 49 concepts** as of 2026-08-13 — the original
  recon counted 8/36 before `smn:MethodScheme` and
  `smn:StatisticalModifierScheme` landed; six method concepts carry
  `sosa:Procedure` and seven carry `iadopt:StatisticalModifier` instance
  typing per the CONVENTIONS §3 instance-typing rule), bridges 08/09 pure
  profile-namespace SKOS.
- The dual-representation rule (`CONVENTIONS.md:72`) holds at the
  explicit-typing level: **no IRI in `ontology/modules/` is declared both
  `owl:Class` and `skos:Concept`** (scripted scan).
- The §12 basis-vs-dimension split is honored (e.g. `smn:BroodYearBasis`
  concept at `07:181` vs `smn:broodYear` datatype property at `02:303`), and
  `ontology/examples/fraser-stock-recruit-year-age.ttl` follows it —
  including using **native** `iadopt:hasProperty/hasObjectOfInterest/hasConstraint`.
- Annotation completeness is bimodal by design history: modules 03/05/07
  ~100% complete against §10; modules 01/02/04 carry exactly the 43 missing
  definitions already tracked in `docs/annotation-gap-ledger.md`.
  *(Updated 2026-09-24, recounted on `d45f8f7`: still 43, but they now fall
  7/29/2/5 across modules 01/02/04/07, because the 2026-08-13 methods-as-SKOS
  migration moved five method terms into 07. The list has moved too: it is
  `ontology/definition-exemptions.csv`, and `make verify-term-definitions`
  fails on an undefined term with no row there and on a row whose term has
  since been defined or removed.)*

## Verified divergences (adversarial verdicts, 2026-08-12)

> **Status 2026-08-13 (S9 step 1, PR pending):** F1–F7 fixed and F8's
> property-side fixed on branch `feat/s9-step1-alignment-semantics` — the
> W3C SOSA–PROV alignment is now *imported* (new module `alignment-upper`,
> vendored snapshot + `catalog-v001.xml`), module 06's equivalences are
> demoted to reviewed Tier-3 bridges in `alignment-main`, the views are
> axiom-light with `smnv:` properties bridged to native `iop:` properties,
> `smn:EscapementMeasurement` is renamed `smn:EscapementEstimate`, module
> 02's class-level property assertions are gone, and CONVENTIONS §5b now
> states the one-strongest-mapping and foreign-subject rules (verified by
> one-off rdflib checks: 0 violations; CI wiring is the follow-up PR).
> F8's scheme landed 2026-08-13 with steps 2+5: `smn:MethodScheme` (six
> migrated method concepts, instance-typed `sosa:Procedure`) and
> `smn:StatisticalModifierScheme` (seven concepts, instance-typed
> `iadopt:StatisticalModifier`, advisory ODM2 links) both live in module 07.

- **F1 (nuanced)** — the views assert OWL axioms on foreign subjects
  (`iadopt:Variable rdfs:subClassOf iao:0000030, sosa:Property`
  `views/salmon-data-metamodel-variable.ttl:14-15`; `sosa:Observation ⊑
  prov:Activity` `event-observation:15`; three `sosa:* ⊑ prov:*` property
  axioms `provenance:14-16`). Not an exposure incident (views unreachable —
  see the builds card) but a policy gap: CONVENTIONS never says whether
  foreign-subject Tier-1 axioms are permitted anywhere.
- **F2 (confirmed)** — Tier-mixed pairs: `iadopt:Variable` gets Tier-1
  `subClassOf` **and** Tier-3 `closeMatch` to `sosa:Property`
  (`variable.ttl:14,69`); worse, the **default build** carries module 06's
  `owl:equivalentClass sosa:Observation ≡ dwc:Occurrence` (`06:22`) alongside
  alignment-main's `closeMatch` on the same pair (`alignment-main:81`).
- **F3 (confirmed)** — `smnv:variableRepresentsProperty/…Entity/…UsesConstraint/…UsesStatisticalModifier`
  duplicate I-ADOPT's native `iop:hasProperty/hasObjectOfInterest/hasConstraint/hasStatisticalModifier`
  with no `subPropertyOf` bridges — while `smnv:constraintConstrains` *is*
  bridged (`variable.ttl:65`) and the fraser example uses `iop:` directly.
  Case-study walkthrough instance data is therefore invisible to
  I-ADOPT-aware consumers.
- **F4 (confirmed)** — relative `owl:imports` in the composite view; no
  catalog; no w3id `views/` route (see the builds card).
- **F5 (nuanced)** — `iadopt:Property ⊑ iao:0000030` is wrong by I-ADOPT's own
  definition (Property = "a type of a characteristic", not a description) and
  collides with module 06's `iadopt:Property owl:equivalentClass
  sosa:Property`; ICE typing of `Variable`/`Constraint` is defensible by
  I-ADOPT's wording.
- **F6 (confirmed)** — `smn:EscapementMeasurement` (a **datum**,
  ⊑ `iao:0000109`, `02:253`) is the lone `*Measurement` class that is not a
  subclass of the **activity** `smn:Measurement` (`02:147`). The name
  (inherited from gcdfo) is the defect; the view mappings are correct.
- **F7 (nuanced)** — TDWG **redefined `dwc:Occurrence` on 2026-05-26** ("A
  dwc:Event that establishes the state of a dwc:Organism…"), which makes
  `sosa:Observation closeMatch dwc:Occurrence` defensible, but module 06's
  `equivalentClass` versions (`06:22-23`) are indefensible under any DwC
  vintage; `sosa:Sampling closeMatch dwc:Event` should weaken to
  `broadMatch` (Event is strictly broader).
- **F8 (nuanced)** — `smnv:variableUsesStatisticalModifier rdfs:range
  owl:Thing` is an unnecessary placeholder: **I-ADOPT 1.1.0 has
  `StatisticalModifier` + `iop:hasStatisticalModifier`**. No smn statistical
  scheme exists among module 07's eight schemes.

## F9 — duplicate English labels in the research closure (2026-08-16, fixed)

Found while checking a downstream report against this repo. The report said
`smn:EscapementSurveyEvent` carried two English `rdfs:label`s plus a
`skos:prefLabel`. **It does not, and never did here** — module 02 gives it one
label, "Escapement survey event"@en, with no `skos:prefLabel` and no
`skos:altLabel`, and that is what every published serialization carries. The
second label is asserted *downstream*: `dfo-salmon-ontology` re-declares the
smn-owned IRI in its own source with `rdfs:label`/`skos:prefLabel`
"Escapement Survey Event"@en (title case, gcdfo's house style), and its docs
pipeline merges that file with a pinned copy of smn. The duplicate exists only
in that merged graph. Ownership, not casing, is the defect: gcdfo renames a
term it does not own.

The same defect class **was** live here, in the opposite direction.
`modules/alignment-research.ttl` carried "external class stubs (readability)"
labelling six SOSA IRIs — `sosa:Observation` as "SOSA Observation" and so on —
inherited verbatim from the gcdfo alignment branch at the `46a4a51` bootstrap.
That predates both `ontology/imports/` vendoring SOSA (`034cb1f`) and
CONVENTIONS §5b rule 3. Once SOSA was vendored, merging the research build gave
each of those six subjects two English labels, upstream's and ours. Confirmed
with `robot merge --catalog` over both build roots: **6 duplicated subjects in
the research closure, 0 in the default closure** — which is why no published
artifact ever showed it and no gate caught it. Five parallel I-ADOPT stubs were
latent rather than live only because I-ADOPT is not vendored.

Fixed 2026-08-16 by dropping the labels and keeping the bare `owl:Class`
declaration stubs. Because `alignment-research` is outside the default build,
the flat TTL and all of `docs/smn.{ttl,owl,jsonld}` are **byte-identical**
across the fix. Now enforced by `scripts/verify_mapping_policy.py` checks 4
and 5, and stated as CONVENTIONS §5b rule 6.

Unrelated pre-existing finding, first seen the same day and **misdiagnosed**:
`make verify-generated-artifacts` failed on a clean `main` because WIDOCO
regenerates `<div id="changelog">` as a real "Changes from last version" block
where the committed HTML has `null`. That was recorded here as "environment-
(likely network-) dependent" drift. **It was not, and that reading is
withdrawn (2026-08-17).** The regenerated block is deterministic: CI run
`31959130307` and a local `make docs-refresh` produced *byte-identical*
`docs/index.html` and `docs/index-en.html` — both blob `7e7c1fd`, both
replacing the committed `6da2d3d`. Two independent environments agreeing to
the byte is not environment dependence; the committed `null` is simply
**stale**, and the gate was reporting a real, one-directional drift.

Provenance of the stale byte: `null` entered at `5279971` (the 0.0.3
re-cut on the release branch), replacing a populated changelog. WIDOCO builds
the block by downloading the `owl:priorVersion` — `https://w3id.org/smn/0.0.3`
— and at that commit the 0.0.3 snapshot had not yet reached GitHub Pages, so
the fetch returned nothing and WIDOCO wrote `null`. Since #25 merged and Pages
published 0.0.3, the fetch resolves, and because the root ontology declares
`priorVersion` equal to its own `versionIRI` (0.0.3), the honest current block
is the heading with an empty change list. Fixed 2026-08-17 by regenerating and
committing the two HTML files; no RDF artifact drifts either way.

Residual sensitivity, stated so it is not rediscovered as a mystery: the block
is a function of a **network fetch**, so `make ci` on a machine that cannot
reach `w3id.org` still writes `null` and will show drift in the opposite
direction. Online — which is the gate's environment — the output is stable.
This stops being a footnote when `priorVersion` is advanced to a genuinely
earlier release, at which point the block gains real content and changes with
every release rather than every network state.

## Upstream facts these rest on (fetched 2026-08-12)

- I-ADOPT current release **1.1.0** (2025-05-28): 9 classes (incl.
  `StatisticalModifier`, `VariableSet`), 17 object properties;
  ObjectOfInterest/ContextObject/Matrix are **roles, not classes**; no
  unit/method component; **no published SOSA alignment**.
- SOSA/SSN 2017 REC: all five published alignments (incl. PROV-O) are
  **non-normative**; a 2023 Edition exists only as a First Public Working
  Draft (2025-09-16) — do not pin conventions to it.
- **Unresolved:** one verifier claimed the views' PROV axioms diverge from
  W3C's `sosa-prov-mapping.ttl` (`hasFeatureOfInterest ⊑ prov:used`); the
  upstream surveyor read that file and found they match. Read the mapping
  file directly before writing any alignment-core module.
- No authoritative DwC↔SOSA mapping exists anywhere; any assertion is a
  local editorial commitment and belongs in a clearly-labeled alignment
  module (SSN practice), never in a core module.

## Module 02 latent modeling errors

`02:213-214` applies object properties **between classes**
(`sosa:FeatureOfInterest sosa:hasSample sosa:Sample`;
`sosa:Sample sosa:isResultOf sosa:Sampling`). This is *legal* OWL 2 DL —
using a class IRI in individual position is punning, and the two meanings are
kept semantically separate — so a DL-profile gate will **not** flag it. That
separation is exactly the problem: the triples relate the class-individuals
and say **nothing about any instance**, while the author almost certainly
intended instance-level semantics (e.g.
`sosa:FeatureOfInterest ⊑ hasSample some sosa:Sample` restrictions) or a
mere schema-level pointer (`rdfs:seeAlso`). Remedy (step 1): rewrite the
axioms to say what is meant, and add a **targeted** CI report (a SPARQL query
flagging object-property assertions whose subject or object is also an
`owl:Class`) — the generic reasoner gate alone cannot catch this class of
mistake.
