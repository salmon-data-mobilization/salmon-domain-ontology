# ADR-0006: Cycle lines as a year-series construct

> **Split note (2026-09-24), not part of the original text.** This ADR is one
> of four into which ADR-0003, *Life-history axes, cycle lines, and no species
> vocabulary*, was split, one per part of salmon-domain-ontology pull request
> 27 (file `docs/adr/0003-life-history-axes-cycle-lines-no-species.md` at
> commit `949ed95`). It is the part that mints the cycle-line scheme, its
> three concepts, `smn:hasCycleLine` and `smn:stratifiedByCycleLine`. The
> split rewords nothing. Every paragraph that is not a split note is the
> original text, copied verbatim, and a passage that concerns more than one
> part is copied into each. The only additions are split notes like this one,
> and HTML comments that mark passages which are salmon-domain evidence rather
> than decisions. Knowledge-log entries dated 2026-08-17 and 2026-08-25 that
> cite ADR-0003 mean the combined ADR, not this file.
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

| Scheme | Top concept | Narrower concepts |
|---|---|---|
| `smn:CycleLineScheme` | `smn:CycleLine` | `smn:OddYearCycleLine`, `smn:EvenYearCycleLine` |

> **Split note.** This row is from decision 4's scheme table. The table's other
> rows are the life-history schemes of ADR-0004 and ADR-0005.

### 5. Cycle line is a year-series construct; reproductive independence is an additional claim

The first draft was closer to right than it looked: it already scoped both
minted concepts to a "two-year-cycle population" and already excluded dominance
in a scope note. Two specific defects are corrected.

**The scheme definition said "largely independent *reproductive* lines."** That
states a fact about period-2 populations as though it were the definition of
the construct. It is not. A cycle line is the set of years congruent to one
another modulo the population's cycle period, under a declared year basis —
a partition of a year series. Whether the resulting class is also
reproductively independent is a further claim, true in some populations and
false in others, and it is now asserted where it holds rather than assumed
everywhere.

<!-- commons-evidence E11 begin: salmon-domain evidence, not a decision (pink age at return is invariant and Fraser sockeye's is not, so cycle-line classes differ in kind); a candidate for salmon-knowledge-commons -->

**The first draft's section 3 claimed that a four-year Fraser Sockeye cycle
"extends the same scheme without redefinition." It does not, and that claim is
withdrawn.** For pink, age at return is invariantly 2, so a year's residue
class is **closed under reproduction**: every fish spawned on the odd line
returns on the odd line, and the class is a lineage. For Fraser sockeye,
roughly 89–92% return at age 4 with real age-3 and age-5 components, so a fish
spawned on one line can return on another. The class is **not closed**, and
brood-year and return-year bases give **non-equivalent partitions of the same
fish**. Declaring a year basis does not reconcile those partitions; it selects
which assertion is being made.

<!-- commons-evidence E11 end -->

<!-- commons-evidence E12 begin: salmon-domain evidence, not a decision (DFO CU tables split pink by line (19 PKO, 14 PKE) and no sockeye CU by line); a candidate for salmon-knowledge-commons -->

DFO's own data individuates the two cases. Pink CUs are split by line —
19 `PKO` and 14 `PKE`, with `FRASER RIVER` appearing as both `PKO-01` and
`PKE-9005` — while **zero** sockeye CUs anywhere are split by cycle line. DFO
also records Fraser Pink as `Cyclic = FALSE`, which is a useful reminder that
the dominance fields cut across this scheme rather than along it.

<!-- commons-evidence E12 end -->

**Two properties, because the subject and the semantics differ even though the
range is shared:**

- `smn:hasCycleLine` — subject is a CU, population, or stock; the line is
  **lineage-defining**. Valid only where age at return is invariant. This is
  also the only condition under which assigning a line to an individual **fish**
  is valid.
- `smn:stratifiedByCycleLine` — subject is a record or observation carrying a
  return year; the line is a **stratification of the year series only**, with
  no reproductive claim. This is the correct property for Fraser sockeye.

A single property with a scope note would have been acceptable and cheaper. Two
is chosen because the distinction is the whole content of the correction above,
and a scope note is the part of a term that consumers skip.

<!-- commons-evidence E13 begin: salmon-domain evidence, not a decision (Holtby & Ciruna 2007 say broodline, never cycle line (glossary p. 327)); a candidate for salmon-knowledge-commons -->

**The name "cycle line" is this vocabulary's coinage, and the 2026-08-25
source check found it is doubly unsupported.** Holtby and Ciruna 2007 — the
framework this scheme draws on — contains the string "cycle line" **zero
times**. Its term is **broodline**, and its glossary (printed p. 327) defines
it in terms this scheme should have been written from in the first place: *"if
the age of reproduction is fixed or nearly so then all (or nearly all) of the
fish spawning in a particular year are the offspring of fish that spawned in a
single year"*, with "even-year and odd-year broodlines" in pink salmon named
as the case. That conditional — *if the age of reproduction is fixed or nearly
so* — is precisely the invariance condition this decision splits
`smn:hasCycleLine` from `smn:stratifiedByCycleLine` over. **The substance of
this decision is corroborated by the source; only the label is not.** The
provenance notes on all four cycle-line terms were rewritten accordingly, and
`smn:CycleLine` now carries `skos:altLabel "Broodline"@en`.

<!-- commons-evidence E13 end -->

<!-- commons-evidence E14 begin: salmon-domain evidence, not a decision (in Fraser sockeye practice a cycle line is a cyclic-dominance line); a candidate for salmon-knowledge-commons -->

Worse than being non-source, the label collides with the model this scheme
*defers*: in Fraser Sockeye practice a "cycle line" is one of the four lines of
the cyclic-dominance model, which `smn:CycleLine`'s own scope note excludes. So
the scheme is currently named after the thing it says it is not about. This is
recorded, not fixed — it reopens the first revision's open question about
"cycle line" versus issue #70's "dominant cycle" with a third candidate,
**broodline**, which is DFO's own word and carries no dominance connotation.
That naming choice is left to review; the terms are otherwise complete either
way, and a rename costs four IRIs on an unmerged branch.

<!-- commons-evidence E14 end -->

<!-- commons-evidence E15 begin: salmon-domain evidence, not a decision (DFO's CU dominance fields Cyclic, Cyc_Dom, Cyc_Dom_Year); a candidate for salmon-knowledge-commons -->

**The deferred dominance model now names its successor.** The first draft
excluded cyclic dominance without saying what would replace it, which is how a
deferral outlives its cause. The successor is DFO's three Conservation Unit
fields: `Cyclic` (a boolean of the CU), `Cyc_Dom`, and `Cyc_Dom_Year` (which
line, for that CU, in that period), with values dominant, subdominant, and
off-cycle. Modelling those three fields retires the deferral.

<!-- commons-evidence E15 end -->

### 6. Mint from the source vocabulary, always (Brett Johnson, 2026-08-24)

> "Mint from the source vocabulary always." — Brett Johnson, 2026-08-24 (Q6-4)

The first draft argued for this position; the ruling settles it, **with reach
beyond this PR**. It is therefore written into `CONVENTIONS.md` as new section
**8b) Vocabulary extent — mint from the source vocabulary**, which is the
citable statement of it. Cite that section rather than re-deriving the
argument; this decision records only what it settles here.

<!-- commons-evidence E16 begin: salmon-domain evidence, not a decision (DFO maintains PKE, with a separate even-year pink CU dataset); a candidate for salmon-knowledge-commons -->

- `smn:EvenYearCycleLine` is minted although the SPSR extract holds no
  even-year row. `PKE` is a code DFO maintains — the open-data catalogue
  publishes a separate *Even Year Pink Salmon Conservation Units* dataset —
  and its absence from one extract is a property of that extract.

<!-- commons-evidence E16 end -->

> **Split note.** Decision 6's other application is in ADR-0005. Its paragraph
> on ADR-0002's age classes is in ADR-0003, with the rule, on which this part is
> stacked.

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
> part's share is three concepts in one scheme, and two object properties, one
> in module 01 and one in module 02.

### 8. The composite DFO code list stays out of the shared layer, and one of its codes does not decompose

`SEL`/`SER`/`PKE`/`PKO`/`CK`/`CM`/`CO` is a DFO Conservation Unit indexing
convention. Under CONVENTIONS section 2 it is Layer C — an agency code list —
and under section 8 it fails the "non-reliance on agency-specific policy
interpretation" criterion. It belongs in `gcdfo:`, where each code carries its
`skos:notation` and decomposes onto the shared terms.

No concept minted here carries a `skos:notation`, because no code in the DFO
list denotes any of these concepts alone. `SEL` is not a code for lake-type;
it is a code for sockeye-and-lake-type. That the composite codes are tempting
to attach is the clearest single symptom of the conflation.

**The decomposition table, corrected 2026-08-25.** The first revision said the
codes decompose as "life-history type for `SEL`/`SER`, cycle line for
`PKE`/`PKO`". That is right for three of the four and wrong for `SER`:

| Code | Species half | Other half decomposes onto |
|---|---|---|
| `PKO` | *O. gorbuscha* | `smn:OddYearCycleLine` |
| `PKE` | *O. gorbuscha* | `smn:EvenYearCycleLine` |

> **Split note.** The `SEL` and `SER` rows, and the evidence that `SER` does not
> decompose onto a named type, are in ADR-0005.

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
| all four cycle-line terms | Holtby & Ciruna 2007, "cycle-line axis … which separates odd-year and even-year Pink Salmon" | **"cycle line" occurs zero times** in the 358-page document. Its term is **broodline**, defined in the glossary (p. 327). Substance corroborated, label not — see decision 5. |

<!-- commons-evidence E19 end -->

> **Split note.** The table's other rows are in ADR-0004 and ADR-0005.

## Consequences

### Positive

- The cycle-line terms now say something true for every population rather than
  something true for pink. The strong claim is still available, on its own
  property, for the populations that support it.
- The redundancy finding is resolvable at the source: once `CU_ID` decomposes,
  `LIFE_HISTORY_TYPE` carries no information the CU identifier does not, and
  SPSR can drop it rather than mint a term for it.
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

> **Split note.** The twenty-two-term figure is the combined proposal's. This
> part's share is six terms: one scheme, three concepts and two properties.

### Neutral

- Module 07 would go from 10 schemes / 49 concepts to 14 / 62.
  `knowledge/data/owl-skos-conventions-state.md` records the pre-merge figure
  and is updated when and if this merges, not before.
- Module 07 remains free of OWL declarations: the new properties are declared
  in modules 01 and 02 and only *used* on concepts in 07.

> **Split note.** On module 07, this part's share is 10 → 11 schemes and 49 → 52
> concepts.

## What would have to change downstream

**`gcdfo`** — mint the composite CU species-code vocabulary as a `gcdfo:`
scheme, each code carrying its `skos:notation` and a decomposition onto the
shared terms, **per decision 8's corrected table**. `SER` is the one that needs
care: it decomposes onto `smn:RiverineRearingHabitat` and the species
annotations only, and must not carry an `exactMatch` or `closeMatch` to
`smn:SockeyeRiverTypeLifeHistory`. `gcdfo:Species` keeps its role as a WSP
output *field* handle. Its scope note asking for taxonomic IRIs is
**satisfied differently than it asks**: under Q6-1 the answer is
`dwc:scientificName` plus a WoRMS `dwc:scientificNameID` on the gcdfo codes
themselves, and there is no IRI to supply. Issue #70 closes by reference to
this ADR; **#74 (species) can now close too**, with Q6-1 as the answer; #68
closes only once the `SER` subtlety is carried into the gcdfo code, since
closing it against a single named type would encode the defect this revision
removed.

> **Split note.** The `SER` guidance and the species annotations in this
> paragraph concern the terms of ADR-0004 and ADR-0005. This ADR's share is the
> decomposition of `PKO` and `PKE` and issue #70, the cycle-line request.

**SPSR** — stop using `smn:Life-HistoryCharacteristic` as a `vocabulary_iri`
for SKOS codes (`spsr-inventory.r:842`); it is an `owl:Class`. Point
life-history codes at `smn:LifeHistoryTypeScheme` and cycle codes at
`smn:CycleLineScheme`. Given the redundancy finding, the better change is to
derive both from `CU_ID` and retire `LIFE_HISTORY_TYPE` — but note that
deriving life-history type from `CU_ID` is **not** correct for `SER`, and the
derivation must yield the rearing-habitat axis value rather than a named type
for those rows.

> **Split note.** This ADR's share of the paragraph above is the cycle codes and
> `smn:CycleLineScheme`. The rest is ADR-0005's.

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
2. **What is the cycle-line scheme called?** Three candidates now, not two:
   "cycle line" as proposed; "dominant cycle" from issue #70; and
   **"broodline"**, which decision 5's source check found is DFO's own term and
   which avoids the collision with the deferred cyclic-dominance model. A
   rename is four IRIs on an unmerged branch.

## More Information

### Sources read for the 2026-08-25 revision

Everything in decisions 9 and Q6-8 rests on a source that was retrieved and
read for this revision, not on a report of one. Where that was not possible it
is said so explicitly.

> **Split note.** Only the source this part's terms cite is listed here.
> ADR-0005 carries the full list.

**DFO advice and framework documents:**

- Holtby, L.B. and Ciruna, K.A. 2007. *Conservation Units for Pacific Salmon
  under the Wild Salmon Policy.* DFO Can. Sci. Advis. Sec. Res. Doc. 2007/070.
  **Read in full (358 pp.).** Verified in it: "sea-type" occurs exactly once,
  in a reference-list entry (p. 80); "cycle line" occurs zero times; the
  **Broodline** glossary entry (p. 327); the sockeye trio at §9.2 and the
  glossary heading *"River/ocean-types of sockeye"*; the 50-ha residual rule;
  footnote 27 on the Harrison assumption; and the chinook non-split at p. 9.

### Rulings recorded in this ADR

- **2026-08-24/25 (Brett Johnson):** Q6-1 species as literal + WoRMS ID, no
  minted species concepts or classes (decision 1); Q6-2 keep
  `dwc:scientificName` on life-history concepts (decision 1); Q6-3
  `hasLifeHistory` plus two specific axis properties (decision 2); Q6-4 mint
  from the source vocabulary always (decision 6, and `CONVENTIONS.md` §8b);
  Q6-5 the prefix rewrite stands (decision 10). **Q6-8 is not ruled.**

> **Split note.** This ADR rests on Q6-4, recorded in ADR-0003, applied to
> `PKE`. The other rulings in the bullet are recorded in ADR-0004 and ADR-0005.

### Other evidence

<!-- commons-evidence E24 begin: salmon-domain evidence, not a decision (evidence pass on the gcdfo issues; CU individuation counts); a candidate for salmon-knowledge-commons -->

- `dfo-salmon-ontology` issues #68, #74, #70 (evidence pass 2026-08-16);
  taxonomic-authority and life-history literature review 2026-08-17.
- Source code list: SPSR data dictionary crosswalk, `demo_cu`/`CU_ID` notes
  column. CU individuation counts (19 `PKO`, 14 `PKE`, `FRASER RIVER` as both
  `PKO-01` and `PKE-9005`, no sockeye CU split by line, Fraser Pink
  `Cyclic = FALSE`) from the DFO Conservation Unit tables.

<!-- commons-evidence E24 end -->

## Related

- [ADR-0002](0002-year-age-basis-dimensions-and-abundance.md) — the
  orthogonal-schemes precedent, and the mint-from-evidence consequence that
  decision 6 scopes rather than reverses.
- `CONVENTIONS.md` **section 8b**, *Vocabulary extent — mint from the source
  vocabulary*, which decision 6 adds and which has reach beyond this ADR: it
  also governs `PKE` and the Pacific Fishery Management Area subareas. Cite it
  rather than re-deriving the argument.
- `CONVENTIONS.md` sections 2, 3, 4, 8, 10, and 11.
