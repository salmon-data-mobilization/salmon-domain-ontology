# ADR-0004: Life-history axes — juvenile freshwater residence duration and juvenile rearing habitat

> **Split note (2026-09-24), not part of the original text.** This ADR is one
> of four into which ADR-0003, *Life-history axes, cycle lines, and no species
> vocabulary*, was split, one per part of salmon-domain-ontology pull request
> 27 (file `docs/adr/0003-life-history-axes-cycle-lines-no-species.md` at
> commit `949ed95`). It is the part that mints the two life-history axis
> schemes, their six concepts, and the two axis properties. The split rewords
> nothing. Every paragraph that is not a split note is the original text,
> copied verbatim, and a passage that concerns more than one part is copied
> into each. The only additions are split notes like this one, and HTML
> comments that mark passages which are salmon-domain evidence rather than
> decisions. Knowledge-log entries dated 2026-08-17 and 2026-08-25 that cite
> ADR-0003 mean the combined ADR, not this file.
>
> Decision numbers are the combined ADR's, kept so that its cross-references
> still resolve. Each ADR travels with its own part, so a tree that carries
> only some of the parts does not contain all of them. Where each decision now
> lives:
>
> - 1, 3, 9a, 9b and 10, and the Q6-8 section: ADR-0005.
> - 2: the three-property table and the argument for the `hasLifeHistory` name
>   in ADR-0005; the argument for the two axis-property names in ADR-0004.
> - 4: the opening paragraphs in both ADR-0004 and ADR-0005; the paragraph on
>   the potamodromous vocabulary in ADR-0004; the named types, the
>   cross-classification and the chinook paragraphs in ADR-0005.
> - 5: ADR-0006.
> - 6: the rule in ADR-0003; its two applications in ADR-0005 and ADR-0006.
> - 7: copied into ADR-0004, ADR-0005 and ADR-0006, one copy per part's terms.
> - 8: ADR-0005; its `PKO`/`PKE` half also in ADR-0006.
> - 9c: ADR-0005; its table rows on the axis terms and on the cycle-line terms
>   also in ADR-0004 and ADR-0006.

## Status

Proposed

Date: 2026-08-17. Revised 2026-08-25. This ADR and the terms it describes are
a **proposal for review**, not an accepted decision. The terms are written into
modules 01, 02, and 07 so the proposal is concrete and reviewable rather than
prose about terms that do not exist.

> **Split note.** This part writes into modules 02 and 07 only. Module 01 is
> written by the parts of ADR-0005 and ADR-0006.

**Revision history, because both revisions changed what the proposal mints.**

The first draft proposed three schemes — life-history type, cycle line, and
**salmon species** — with two life-history concepts and five species concepts.
Research on taxonomic authorities and on the life-history literature, plus
three rulings from Brett Johnson on 2026-08-17, withdrew the species scheme,
decomposed life-history type into axes, and redefined cycle line as a
year-series construct.

The 2026-08-25 revision applies five further rulings from Brett Johnson
(2026-08-24/25, recorded below as Q6-1 through Q6-5), and corrects **one
substantive defect and a set of mis-citations that the rulings did not ask
about and that nobody had questioned**. Those corrections are decision 8, and
they are the part of this revision worth reading first: a term in the previous
draft asserted two things that cannot both be true, and several `iao:0000119`
provenance notes cited sources that do not say what was attributed to them.
The reasoning that survived both revisions is kept, not rewritten.

## Context

A review of the Salmon Population Summary Repository (SPSR) extract raised
three held ontology-term requests, tracked as `dfo-salmon-ontology` issues
[#68](https://github.com/dfo-pacific-science/dfo-salmon-ontology/issues/68),
[#74](https://github.com/dfo-pacific-science/dfo-salmon-ontology/issues/74),
and [#70](https://github.com/dfo-pacific-science/dfo-salmon-ontology/issues/70).
The evidence pass recorded on those issues established four facts.

<!-- commons-evidence E01 begin: salmon-domain evidence, not a decision (SPSR LIFE_HISTORY_TYPE values and counts; the DFO Conservation Unit species-code list); a candidate for salmon-knowledge-commons -->

1. SPSR's `LIFE_HISTORY_TYPE` column mixes **two conceptual axes**: Sockeye
   juvenile rearing type (`Lake Type`, 1367 rows; `River Type`, 108) and Pink
   brood cycle (`Odd Year`, 33).
2. The column is **perfectly redundant** with the `CU_ID` prefix. The
   crosstab of prefix against value is diagonal: `SEL` → Lake Type, `SER` →
   River Type, `PKO` → Odd Year, and `CK`/`CM`/`CO` → null. *(Added
   2026-08-25: that diagonal is exactly what conceals the defect decision 8
   corrects. `SER` maps to `River Type` in the extract because DFO's
   `LIFE_HISTORY_TYPE` column has no other value it could map to — the
   dictionary documents the Sockeye values as `Lake Type, River Type` and
   nothing else — while the `SER` code itself covers a second life-history
   type the column cannot name. A perfect diagonal reads as confirmation and
   is here a symptom.)*
3. The DFO Conservation Unit species-code list is `SEL` = Sockeye (Lake
   Type), `SER` = Sockeye (River Type), `PKE` = Pink-Even, `PKO` = Pink-Odd,
   `CK` = Chinook, `CM` = Chum, `CO` = Coho. **`PKE` exists in that list**
   even though the SPSR extract contains no even-year rows — its 33 odd-year
   rows are a single Fraser Pink CU.
4. Neither `smn:` nor `gcdfo:` contains a lake-type, river-type, cycle-line,
   or species concept today. `smn:Life-HistoryCharacteristic` is an
   `owl:Class` whose only subclass is `smn:Run`, and `gcdfo:Species` is a
   bare field handle whose scope note says its values are common-name
   strings.

<!-- commons-evidence E01 end -->

A fifth fact was established on the consumer side. The PSC controlled
vocabulary (`psc-salmon-vocabularies`, `v0.1.0-alpha.3`: 4 schemes, 38
concepts) has **zero** concepts covering species, life-history type, run
timing, cycle line, or juvenile rearing. There is nothing to reconcile and no
supersession problem. Its only live `smn:` anchor is nine `skos:broadMatch`
rows onto `smn:EnumerationMethod`. Its governance file states that PSC "may
publish a one-way PSC assertion to an immutable `smn:` target, but it cannot
mint or approve `smn:` terms," and its candidate review files instruct that
gaps stay blank because "a broad or wrong-kind term is not a substitute."

The obvious economical option was a **single CU species-code vocabulary**
covering `CK`/`CM`/`CO`/`SEL`/`SER`/`PKE`/`PKO`, which would close all three
issues with one scheme. That option is rejected: the code is composite, and
minting it whole would publish the conflation into the shared layer where
every consumer inherits it. That much is unchanged from the first draft, and
it is the reason this ADR exists.

What changed is what the decomposition should produce.

## Decision

### 2. Life-history assertion takes three properties, not one and not five (Brett Johnson, 2026-08-24)

> "Take hasLifeHistory plus two specific axis properties." — Brett Johnson,
> 2026-08-24 (Q6-3)

Three properties for the life-history construct, and **the generic
`smn:hasLifeHistoryAxisValue` floated as an alternative in the first
revision's open question 3 is not minted**:

| Property | Module | What it says |
|---|---|---|
| `smn:hasJuvenileFreshwaterResidenceDuration` | 02 | decomposes a named type onto the duration axis |
| `smn:hasJuvenileRearingHabitat` | 02 | decomposes a named type onto the habitat axis |

> **Split note.** The ruling's third property, and its row of this table, travel
> with ADR-0005, whose part mints it. The two rows above are this part's.

The two cycle-line properties of decision 4 are a separate construct and are
not part of this count.

**The names, argued, because the ruling gives the first one and asks for the
other two to be named from what the axes are.**

`smn:hasJuvenileFreshwaterResidenceDuration` replaces
`smn:hasJuvenileFreshwaterResidence`. **"Duration" is load-bearing.** Without
it the property reads as whether the group has a freshwater residence at all,
which is true of every anadromous salmon and therefore says nothing; the axis
is a length of time, and the values are lengths of time. "Juvenile" is kept
because adults also reside in fresh water, on a spawning migration this axis
does not measure.

`smn:hasJuvenileRearingHabitat` replaces `smn:hasJuvenileNurseryHabitat`.
**"Rearing" rather than "nursery"** because rearing habitat is the settled
term for the juvenile freshwater growth phase in the Pacific salmon
literature, while "nursery area" carries a distinct and largely
marine/estuarine sense; DFO's own framework document uses "nursery lakes" for
the lake case specifically but describes the axis itself as where juveniles
"rear". **"Juvenile" is kept here for a different reason than on the duration
property:** `smn:hasRearingHabitat`, unqualified, is the name a future
property relating a population to an *actual named water body* would want, and
these two must not collide. The value of this property is always a *kind* of
water, never a water body.

The schemes and concepts were renamed to match, so the axis is legible from
the property: `smn:JuvenileFreshwaterResidenceDurationScheme` /
`smn:JuvenileFreshwaterResidenceDuration`, and
`smn:JuvenileRearingHabitatScheme` / `smn:JuvenileRearingHabitat` with
`smn:LakeRearingHabitat` and `smn:RiverineRearingHabitat`. The two duration
values keep their IRIs — `smn:SubyearlingFreshwaterResidence` and
`smn:YearlingFreshwaterResidence` — because they name classes of migrant,
which is how the literature says it, and a value of a duration axis does not
need "Duration" in its own name.

**Why not the generic property.** A single `smn:hasLifeHistoryAxisValue` would
let a third axis be added without minting a term. It is refused because it
makes the cheap query expensive and the expensive query no cheaper: "all types
with a lake nursery" becomes a two-hop join through `skos:inScheme`, and the
axis a triple belongs to stops being readable from the triple. Adding an axis
is rare; reading a decomposition is not.

### 4. Life-history type is decomposed into axes; named types are species-scoped combinations

The first draft's two flat concepts, `smn:LakeTypeLifeHistory` and
`smn:RiverTypeLifeHistory`, are replaced. They were too thin in two ways that
compound.

<!-- commons-evidence E05 begin: salmon-domain evidence, not a decision (sockeye's three life-history terms encode two axes; chinook's encode one plus an adult syndrome); a candidate for salmon-knowledge-commons -->

**Sockeye's three terms encode two axes, not one.** Sea-type, lake-type, and
river-type resolve into a *duration* axis (sea-type is under a year in fresh
water; lake- and river-type are a year or more) and a *rearing habitat* axis
(lake versus flowing water). Chinook's stream-type/ocean-type distinction is
the duration axis **only**, plus an adult behavioural syndrome that sockeye's
terms do not carry. A flat list of named types hides both facts and makes the
cross-species arithmetic look easy.

<!-- commons-evidence E05 end -->

<!-- commons-evidence E06 begin: salmon-domain evidence, not a decision (label hazards: sockeye river-type is not chinook stream-type; DFO uses ocean-type in two senses); a candidate for salmon-knowledge-commons -->

**And the names are actively dangerous** — though *which* name is dangerous
was got wrong in the first revision, and is corrected in decision 9. Sockeye
river-type is **not** chinook stream-type despite near-identical English. And
"ocean-type" is used by DFO in two mutually exclusive senses that are both
current. A flat cross-species enum of these strings produces silent errors,
which is the failure mode this decision exists to prevent.

<!-- commons-evidence E06 end -->

So: two species-neutral **axis schemes** hold the primitives, and
`smn:LifeHistoryTypeScheme` holds **named types, each scoped to one species**
and each defined as a combination of axis values.

> **Split note.** The named-type scheme this sentence names is minted by the
> part of ADR-0005, which is stacked on this one. This part mints the two axis
> schemes only.

| Scheme | Top concept | Narrower concepts |
|---|---|---|
| `smn:JuvenileFreshwaterResidenceDurationScheme` | `smn:JuvenileFreshwaterResidenceDuration` | `smn:SubyearlingFreshwaterResidence`, `smn:YearlingFreshwaterResidence` |
| `smn:JuvenileRearingHabitatScheme` | `smn:JuvenileRearingHabitat` | `smn:LakeRearingHabitat`, `smn:RiverineRearingHabitat` |
| `smn:LifeHistoryTypeScheme` | `smn:LifeHistoryType` | `smn:SockeyeLakeTypeLifeHistory`, `smn:SockeyeRiverTypeLifeHistory`, `smn:SockeyeSeaTypeLifeHistory` |
| `smn:CycleLineScheme` | `smn:CycleLine` | `smn:OddYearCycleLine`, `smn:EvenYearCycleLine` |

> **Split note.** Of this table, this part mints the first two rows. The third
> row is ADR-0005's and the fourth is ADR-0006's.

<!-- commons-evidence E10 begin: salmon-domain evidence, not a decision (adfluvial / fluvial / lacustrine is a potamodromous classification); a candidate for salmon-knowledge-commons -->

**`adfluvial`/`fluvial`/`lacustrine` is not this vocabulary.** It is a
potamodromous classification (Rieman and McIntyre 1993), and it treats anadromy
as a *separate category alongside* those terms rather than as something they
qualify. Applying "adfluvial" to an anadromous sockeye population is a category
error; applying it to kokanee is defensible and would be a different scheme.
The surface similarity — lacustrine resembles lake, fluvial resembles river —
is exactly why the rearing-habitat scheme says so in a scope note.

<!-- commons-evidence E10 end -->

### 7. The class/concept boundary is explicit, and no `skos:*Match` crosses it

All thirteen vocabulary terms are `skos:Concept`, in `skos:ConceptScheme`s, in
module 07. None is an `owl:Class`, and none reuses the IRI of one. The five new
object properties are `owl:ObjectProperty` in modules 01 and 02; none is a
concept.

The three new properties that range on `skos:Concept` do so deliberately:
values come from a named scheme, pointed at with `rdfs:seeAlso`, in the same
way `smn:broodYear` points at `smn:BroodYearBasis`. `rdfs:domain` is omitted on
all five properties, with the omission and its retirement condition recorded in
the module comments — the legitimate subjects have no common superclass in this
build, and an OWL 2 EL-safe union domain is not expressible.

> **Split note.** The counts in this decision are the combined proposal's. This
> part's share is six concepts in two schemes, and two object properties, both
> in module 02. The decision's paragraphs on `smn:Life-HistoryCharacteristic`
> and on the withdrawn NCBI links are in ADR-0005.

### 9. A defect and a provenance audit that nobody asked for (2026-08-25)

Neither of these was in scope for the 2026-08-24 rulings. Both are corrected
here because the terms are unmerged and the cost of correcting them now is a
diff.

#### 9c. Provenance notes cited sources that do not say what was attributed to them

Every `iao:0000119` in the proposal was checked against its cited source.
Three distinct problems, all now fixed:

<!-- commons-evidence E19 begin: salmon-domain evidence, not a decision (provenance findings: cycle line absent from Holtby & Ciruna; Burgner cited for lake-type only); a candidate for salmon-knowledge-commons -->

| Term(s) | Was cited for | Finding |
|---|---|---|
| both axis schemes and all six axis concepts, plus lake- and river-type | Burgner 1991 for the axis distinctions | Burgner 1991 is a paywalled UBC Press chapter that **could not be read**, so nothing in this change should have rested on it. Replaced throughout with sources that were read: Gilbert 1913, Beacham & Withler 2017, Wood et al. 2008. |

<!-- commons-evidence E19 end -->

> **Split note.** The other rows of this table are in ADR-0005 (the life-history
> type and Sea-type terms) and ADR-0006 (the cycle-line terms).

## Consequences

### Positive

- The axes become independently statable, queryable, and mappable. A consumer
  that needs only juvenile rearing duration is not forced to adopt a named
  race, a species claim, or a genetic-structure claim.
- PSC can map to these without restructuring. Its pipeline requires SKOS
  targets — it recorded a rejection of `smn:ObservedRateOrAbundance` as
  `rejected_wrong_kind_and_too_broad` with `native_type: owl:Class` — and
  composes `skos:broadMatch` through documented `skos:broader*` chains, which
  every concept here has. Every concept has exactly one `skos:prefLabel`, one
  `skos:definition`, one `skos:inScheme`, and at most one `skos:broader`,
  which is what PSC's SHACL requires of a mapping target.

### Negative

- Twenty-two new shared terms — 4 schemes, 13 concepts, 5 properties — is the
  largest single admission to the shared layer since the age and year schemes,
  and CONVENTIONS section 1 sets a conservative default of keeping terms in a
  profile first. The count is larger than the first draft's 12 despite dropping
  five species concepts.
- Two levels are more work for a consumer than one flat list: a row that was
  one string becomes a named type plus, if the consumer wants the axes, a
  decomposition lookup.

> **Split note.** The twenty-two-term figure is the combined proposal's. This
> part's share is ten terms: two schemes, six concepts and two properties.

### Neutral

- `smn:Life-HistoryCharacteristic` and `smn:Run` are unchanged apart from an
  editorial comment. No released IRI is renamed, retired, or re-typed; the two
  concepts renamed in the first revision (`smn:LakeTypeLifeHistory` →
  `smn:SockeyeLakeTypeLifeHistory`, and its river counterpart) exist only on
  this unmerged branch. The same is true of everything the 2026-08-25 revision
  renames: `smn:hasLifeHistoryType` → `smn:hasLifeHistory`, the two axis
  properties, and the six axis scheme and concept IRIs. **No released IRI is
  touched by any of it**, which is the whole reason these corrections are
  cheap now and would not be after a release.
- Module 07 would go from 10 schemes / 49 concepts to 14 / 62.
  `knowledge/data/owl-skos-conventions-state.md` records the pre-merge figure
  and is updated when and if this merges, not before.
- Module 07 remains free of OWL declarations: the new properties are declared
  in modules 01 and 02 and only *used* on concepts in 07.

> **Split note.** The first bullet also covers renames of terms minted by the
> part of ADR-0005. On module 07, this part's share is 10 → 12 schemes and 49 →
> 55 concepts.

## What would have to change downstream

**PSC** — no change required, and nothing to retract. If PSC wants to map into
these schemes it appends the IRIs to `allowed_object_ids` in
`data/external-sources.json`, adds reviewed rows to
`data/external-mapping-review.csv`, and cuts a release.

## Open questions still for review

1. **Layer.** These are proposed straight into shared `smn:`, not into a
   `smn/profile/<program>/` bridge. The justification is that two independently
   governed organizations (DFO and PSC) can use them, which is PSC's own
   promotion bar — but PSC has not asked for them, so the multi-agency reuse in
   CONVENTIONS section 8 criterion 1 is expected rather than demonstrated.

**Resolved since the first revision, and recorded here so the review does not
re-litigate them:** species (Q6-1, decision 1); `dwc:scientificName` on a
life-history concept (Q6-2 — *"OK yeah. I guess that makes sense so that it's
clear that some life histories only apply to certain species"*); two axis
properties rather than one generic one (Q6-3, decision 2); whether
`smn:SockeyeSeaTypeLifeHistory` is wanted (Q6-4, decision 6 — and decision 9a
shows it is in the source data after all); the prefix rewrite (Q6-5,
decision 10).

> **Split note.** Of the items above, this ADR carries Q6-3's two axis
> properties. The others are recorded in ADR-0003 and ADR-0005.

## More Information

### Sources read for the 2026-08-25 revision

Everything in decisions 9 and Q6-8 rests on a source that was retrieved and
read for this revision, not on a report of one. Where that was not possible it
is said so explicitly.

> **Split note.** Only the sources this part's terms cite are listed here.
> ADR-0005 carries the full list.

**DFO advice and framework documents:**

- Holtby, L.B. and Ciruna, K.A. 2007. *Conservation Units for Pacific Salmon
  under the Wild Salmon Policy.* DFO Can. Sci. Advis. Sec. Res. Doc. 2007/070.
  **Read in full (358 pp.).** Verified in it: "sea-type" occurs exactly once,
  in a reference-list entry (p. 80); "cycle line" occurs zero times; the
  **Broodline** glossary entry (p. 327); the sockeye trio at §9.2 and the
  glossary heading *"River/ocean-types of sockeye"*; the 50-ha residual rule;
  footnote 27 on the Harrison assumption; and the chinook non-split at p. 9.

**Literature:**

- Gilbert, C.H. 1913. *Age at maturity of the Pacific coast salmon of the
  genus Oncorhynchus.* Bulletin of the United States Bureau of Fisheries
  32:1–22. **Read, and cross-checked against an independent OCR of the same
  volume**; both give the same counts ("sea type" ×19, "stream type" ×16,
  "lake type"/"river type" ×0). Note that two citations for this paper are in
  circulation — the U.S. Bulletin version above, and a British Columbia
  Commissioner of Fisheries reprint (1912 report, pp. 57–70). Only the
  Bulletin version was read.
- Wood, C.C., Bickham, J.W., Nelson, R.J., Foote, C.J., and Patton, J.C. 2008.
  *Recurrent evolution of life history ecotypes in sockeye salmon.*
  Evolutionary Applications 1:207–221. **Read.** The "sea/river ecotype"
  coinage and the special-case sentence.
- Beacham, T.D. and Withler, R.E. 2017. *Population structure of sea-type and
  lake-type sockeye salmon and kokanee in the Fraser River and Columbia River
  drainages.* PLOS ONE 12(9):e0183713. **Read.** The freshwater-annulus
  discriminator; Harrison and Widgeon Slough as the sea-type populations; and
  that both sea-type and river-type juveniles rear in river habitats.
- Healey, M.C. 1991. *Life history of chinook salmon (Oncorhynchus
  tshawytscha).* In Groot, C. and Margolis, L. (eds.), *Pacific Salmon Life
  Histories*, UBC Press. **Read** (p. 314 for the ocean-type/sea-type gloss;
  also the source for tactical versus race-defining variation and the
  Sacramento winter run).
- Burgner, R.L. 1991. *Life history of sockeye salmon (Oncorhynchus nerka).*
  In the same volume, pp. 3–117. **NOT read** — paywalled. It is the customary
  citation for lake-type, recorded as such on one term and relied on nowhere.
  The first draft cited it for sea-type and for both axes; see decision 9c.
- Rieman, B.E. and McIntyre, J.D. 1993. *Demographic and habitat requirements
  for conservation of bull trout.* USDA Forest Service GTR INT-302 — the
  potamodromous vocabulary refused in the rearing-habitat scope note.

### Rulings recorded in this ADR

- **2026-08-24/25 (Brett Johnson):** Q6-1 species as literal + WoRMS ID, no
  minted species concepts or classes (decision 1); Q6-2 keep
  `dwc:scientificName` on life-history concepts (decision 1); Q6-3
  `hasLifeHistory` plus two specific axis properties (decision 2); Q6-4 mint
  from the source vocabulary always (decision 6, and `CONVENTIONS.md` §8b);
  Q6-5 the prefix rewrite stands (decision 10). **Q6-8 is not ruled.**

> **Split note.** This ADR records Q6-3's two axis properties. The other rulings
> in the bullet are recorded in ADR-0003 and ADR-0005.

### Other evidence

- `dfo-salmon-ontology` issues #68, #74, #70 (evidence pass 2026-08-16);
  taxonomic-authority and life-history literature review 2026-08-17.

## Related

- [ADR-0002](0002-year-age-basis-dimensions-and-abundance.md) — the
  orthogonal-schemes precedent, and the mint-from-evidence consequence that
  decision 6 scopes rather than reverses.
- `CONVENTIONS.md` sections 2, 3, 4, 8, 10, and 11.
