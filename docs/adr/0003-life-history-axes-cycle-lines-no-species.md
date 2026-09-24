# ADR-0003: Life-history axes, cycle lines, and no species vocabulary

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

**Q6-8 — whether the three Sockeye types are flat peers — is deliberately
NOT decided here.** The evidence gathered for this revision bears on it, and
runs against flat peers; it is set out at the end so it can be ruled on, and
the terms are shaped so either ruling is cheap. Nothing in this change mints
the hierarchy that ruling would settle.

## Context

A review of the Salmon Population Summary Repository (SPSR) extract raised
three held ontology-term requests, tracked as `dfo-salmon-ontology` issues
[#68](https://github.com/dfo-pacific-science/dfo-salmon-ontology/issues/68),
[#74](https://github.com/dfo-pacific-science/dfo-salmon-ontology/issues/74),
and [#70](https://github.com/dfo-pacific-science/dfo-salmon-ontology/issues/70).
The evidence pass recorded on those issues established four facts.

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

### 1. Species is a literal plus a WoRMS identifier, and smn mints no species term (Brett Johnson, 2026-08-24)

> "you can use dwc:scientificName literal and a WoRMS ID. No minting species
> concepts or classes, but literal species annotations are definitely
> allowed." — Brett Johnson, 2026-08-24 (Q6-1)

This settles what the 2026-08-17 draft left open. `smn:SalmonSpeciesScheme`
and its five species concepts stay **withdrawn**, and nothing replaces them —
now as a standing rule rather than as a scoping decision for one PR. Species
reference in `smn` is:

```turtle
dwc:scientificName    "Oncorhynchus nerka" ;
dwc:scientificNameID  "urn:lsid:marinespecies.org:taxname:254569" ;
rdfs:seeAlso          <https://www.marinespecies.org/aphia.php?p=taxdetails&id=254569> ;
```

carried on each of the three named life-history types. The WoRMS record was
checked by request on 2026-08-25: AphiaID 254569, *Oncorhynchus nerka*
(Walbaum, 1792), `status: accepted`, LSID
`urn:lsid:marinespecies.org:taxname:254569`.

**The `rdfs:seeAlso` is included because WoRMS passes the test NCBI failed.**
The first draft's five NCBI `rdfs:seeAlso` links were removed because the OBO
PURL served `text/html` under every RDF `Accept` header, so they resolved to
documentation rather than data. WoRMS, requested the same way on 2026-08-25,
redirects `Accept: application/rdf+xml` to
`.../authority/metadata.php?lsid=urn:lsid:marinespecies.org:taxname:254569`
and returns `application/rdf+xml` — an `rdf:Description` about the LSID itself,
using Darwin Core terms. The identifier is therefore actionable, not
decorative. That check is the reason this link is admitted where the earlier
ones were not, and re-running it is what would retire the link if WoRMS ever
stops.

The reasons the species *scheme* was withdrawn are unchanged and still hold,
so they are kept rather than rewritten:

**Steelhead is in scope** (Brett Johnson, 2026-08-17), and steelhead has **no
taxonomic identifier in ITIS, WoRMS, NCBI, GBIF, or Catalogue of Life**. It is
a vernacular for the anadromous form of *Oncorhynchus mykiss* in every one of
them, and is managed by NOAA as eleven Distinct Population Segments. A
vocabulary that must be able to carry steelhead is not a species vocabulary;
calling it one guarantees that the first term it cannot represent is one of
the ones it was built for. Note that Q6-1 does not make steelhead expressible
either — it makes the gap **honest**, because a `dwc:scientificName` literal
can say `"Oncorhynchus mykiss"` and stop, where a minted `smn:Steelhead`
concept would have implied a taxon that no authority recognises.

**The source data holds administrative codes, not taxa.** `SEL` is sockeye
crossed with a life-history type and `PKO` is pink crossed with a cycle line.
Four of the seven CU codes correspond to no taxon at all, and neither does
steelhead or kokanee. Building a *species* vocabulary to serve a *code* list
misdescribes what the codes are, which is the same error as minting the
composite code whole, one level down.

**The authorities disagree, actively.** WoRMS, Catalogue of Life, and GBIF
have elevated Lahontan and Rio Grande cutthroat to species while ITIS and NCBI
still hold them as subspecies, and *Oncorhynchus lewisi* — the current
American Fisheries Society name for westslope cutthroat — appears in none of
the five. Minting an `smn:` species concept means picking a side in a live
nomenclatural dispute and then owning the divergence. Q6-1 avoids this rather
than resolving it: a literal plus an identifier records *what one authority
says*, attributably, and a consumer that prefers a different authority can
disagree with the identifier without disagreeing with `smn`.

**The tension the first revision could not resolve is now resolved.** That
draft recorded two of Brett's statements pulling in different directions — a
species reference, if minted, goes in `smn` and never `gcdfo`; and the likely
future shape is a `gcdfo` **code** vocabulary carrying `dwc:scientificName`
plus a WoRMS `dwc:scientificNameID` directly — and asked which was intended.
Q6-1 answers it: **neither namespace mints a species concept**, so the
question of where it would live does not arise. The gcdfo codes carry the
literal and the identifier themselves and have no `smn:` species concept to
point at, which is exactly the condition under which the draft said the two
statements were compatible.

`dfo-salmon-ontology` issue #74 (species) can now be answered rather than left
open: the answer is that species is not a term, it is two annotations.

### 2. Life-history assertion takes three properties, not one and not five (Brett Johnson, 2026-08-24)

> "Take hasLifeHistory plus two specific axis properties." — Brett Johnson,
> 2026-08-24 (Q6-3)

Three properties for the life-history construct, and **the generic
`smn:hasLifeHistoryAxisValue` floated as an alternative in the first
revision's open question 3 is not minted**:

| Property | Module | What it says |
|---|---|---|
| `smn:hasLifeHistory` | 01 | assigns a named type to a Conservation Unit, population, or stock |
| `smn:hasJuvenileFreshwaterResidenceDuration` | 02 | decomposes a named type onto the duration axis |
| `smn:hasJuvenileRearingHabitat` | 02 | decomposes a named type onto the habitat axis |

The two cycle-line properties of decision 4 are a separate construct and are
not part of this count.

**The names, argued, because the ruling gives the first one and asks for the
other two to be named from what the axes are.**

`smn:hasLifeHistory` replaces the draft's `smn:hasLifeHistoryType`. Beyond
being the name in the ruling, it is the one that agrees with its own range:
the values are IRIs ending `…LifeHistory` — `smn:SockeyeLakeTypeLifeHistory`
and its siblings — so `smn:hasLifeHistory smn:SockeyeLakeTypeLifeHistory`
reads as a sentence, where `hasLifeHistoryType` named something the range does
not contain. Dropping "Type" also removes a term that a reader can mistake for
`rdf:type`.

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

### 3. Life-history type is asserted at Conservation Unit, population, or stock level (Brett Johnson, 2026-08-17)

Not for individual fish. This collapses the level problem the first draft left
open — whether a life-history type is a property of a fish, a brood, or a
group — by ruling that the assertion is population-level, and the design
follows the ruling: `smn:hasLifeHistory` relates a CU, population, or stock to
a named type, and nothing in the scheme is shaped for an individual. The
2026-08-24 rename does not disturb this; the level ruling is carried on the
property's `rdfs:comment`.

### 4. Life-history type is decomposed into axes; named types are species-scoped combinations

The first draft's two flat concepts, `smn:LakeTypeLifeHistory` and
`smn:RiverTypeLifeHistory`, are replaced. They were too thin in two ways that
compound.

**Sockeye's three terms encode two axes, not one.** Sea-type, lake-type, and
river-type resolve into a *duration* axis (sea-type is under a year in fresh
water; lake- and river-type are a year or more) and a *rearing habitat* axis
(lake versus flowing water). Chinook's stream-type/ocean-type distinction is
the duration axis **only**, plus an adult behavioural syndrome that sockeye's
terms do not carry. A flat list of named types hides both facts and makes the
cross-species arithmetic look easy.

**And the names are actively dangerous** — though *which* name is dangerous
was got wrong in the first revision, and is corrected in decision 9. Sockeye
river-type is **not** chinook stream-type despite near-identical English. And
"ocean-type" is used by DFO in two mutually exclusive senses that are both
current. A flat cross-species enum of these strings produces silent errors,
which is the failure mode this decision exists to prevent.

So: two species-neutral **axis schemes** hold the primitives, and
`smn:LifeHistoryTypeScheme` holds **named types, each scoped to one species**
and each defined as a combination of axis values.

| Scheme | Top concept | Narrower concepts |
|---|---|---|
| `smn:JuvenileFreshwaterResidenceDurationScheme` | `smn:JuvenileFreshwaterResidenceDuration` | `smn:SubyearlingFreshwaterResidence`, `smn:YearlingFreshwaterResidence` |
| `smn:JuvenileRearingHabitatScheme` | `smn:JuvenileRearingHabitat` | `smn:LakeRearingHabitat`, `smn:RiverineRearingHabitat` |
| `smn:LifeHistoryTypeScheme` | `smn:LifeHistoryType` | `smn:SockeyeLakeTypeLifeHistory`, `smn:SockeyeRiverTypeLifeHistory`, `smn:SockeyeSeaTypeLifeHistory` |
| `smn:CycleLineScheme` | `smn:CycleLine` | `smn:OddYearCycleLine`, `smn:EvenYearCycleLine` |

The decomposition is machine-readable, not prose: each named type carries
`smn:hasJuvenileFreshwaterResidenceDuration` and
`smn:hasJuvenileRearingHabitat`.

| Named type | Duration | Rearing habitat |
|---|---|---|
| `smn:SockeyeLakeTypeLifeHistory` | yearling or older | lake |
| `smn:SockeyeRiverTypeLifeHistory` | yearling or older | riverine |
| `smn:SockeyeSeaTypeLifeHistory` | subyearling | riverine |

**The two axes cross-classify, and that is the evidence they are separable.**
The duration axis groups lake with river against sea; the habitat axis groups
river with sea against lake. Two axes that partition the same three types two
different ways cannot be one bundled type wearing a disguise. This replaces
the first revision's argument, which rested on
`smn:SockeyeSeaTypeLifeHistory` carrying *no* habitat value — "a group that
leaves in its first year has no freshwater nursery worth naming". That claim
is false and is withdrawn; see decision 9. Beacham and Withler (2017) report
that sea-type and river-type juveniles both rear in river habitats, with
sea-type juveniles rearing for several months in estuarine waters, so the
habitat value is now asserted. The replacement argument is stronger than the
one it replaces: an asymmetry is one term declining to answer, whereas a
cross-classification is both axes answering and disagreeing.

It also does something the first revision's model could not: it makes **both**
answers to the still-open Q6-8 derivable from the axes without minting
anything. See the Q6-8 section below.

**Chinook ocean-type and stream-type are deliberately not minted**, and the
reason is evidential rather than procedural. Healey's own model is two-level:
a race-defining bundle plus *tactical* variation within it, with age at
maturity and precocity explicitly not race-defining. He states he cannot
classify the Sacramento winter run, which pairs stream-type adult behaviour
with ocean-type juvenile behaviour — primary evidence that the axes come
apart. And the bundle is not stable across the range: in the interior Columbia
the split is a deep genetic division (G_ST ≈ 0.15), while coastally run timing
explains about 10% of G_ST and within-basin run types differ by G_ST < 0.02
(Waples et al. 2004), with Moran et al. (2013) finding the two-race model does
not hold coast-wide. Minting `smn:ChinookOceanType` as a primitive would assert
a bundle whose extension changes with latitude. The axes let such a group be
described exactly, one axis at a time, with no named type forced on it.

**DFO reached the same conclusion, and its reasoning is now on record here
rather than inferred.** Holtby and Ciruna (2007, p. 9) considered separating
chinook into ocean- and stream-types at the ecotypic step of Conservation Unit
delimitation and declined: *"We decided not to make such a split in part
because many populations in Canada are mixtures of the two types and because
those situations where the two types are distinctive are fully captured in the
subsequent analysis."* Two things follow, and the second is easy to miss.
First, **mixture is the obstacle**, and nothing in this proposal's vocabulary
can express a mixture — a population that is 60% one type has no
representation here, and `smn:hasLifeHistory` would have to be asserted twice
or not at all. Second, the refusal was **local to that step**: the same
document partitions sockeye and pink there, and then uses the chinook
ocean/stream dichotomy heavily in the per-CU genetic analysis. So DFO's
position is not that the chinook types are unreal; it is that they are not a
*partition*. That is a warning about this scheme's shape, not about chinook.

**`adfluvial`/`fluvial`/`lacustrine` is not this vocabulary.** It is a
potamodromous classification (Rieman and McIntyre 1993), and it treats anadromy
as a *separate category alongside* those terms rather than as something they
qualify. Applying "adfluvial" to an anadromous sockeye population is a category
error; applying it to kokanee is defensible and would be a different scheme.
The surface similarity — lacustrine resembles lake, fluvial resembles river —
is exactly why the rearing-habitat scheme says so in a scope note.


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

DFO's own data individuates the two cases. Pink CUs are split by line —
19 `PKO` and 14 `PKE`, with `FRASER RIVER` appearing as both `PKO-01` and
`PKE-9005` — while **zero** sockeye CUs anywhere are split by cycle line. DFO
also records Fraser Pink as `Cyclic = FALSE`, which is a useful reminder that
the dominance fields cut across this scheme rather than along it.

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

Worse than being non-source, the label collides with the model this scheme
*defers*: in Fraser Sockeye practice a "cycle line" is one of the four lines of
the cyclic-dominance model, which `smn:CycleLine`'s own scope note excludes. So
the scheme is currently named after the thing it says it is not about. This is
recorded, not fixed — it reopens the first revision's open question about
"cycle line" versus issue #70's "dominant cycle" with a third candidate,
**broodline**, which is DFO's own word and carries no dominance connotation.
That naming choice is left to review; the terms are otherwise complete either
way, and a rename costs four IRIs on an unmerged branch.

**The deferred dominance model now names its successor.** The first draft
excluded cyclic dominance without saying what would replace it, which is how a
deferral outlives its cause. The successor is DFO's three Conservation Unit
fields: `Cyclic` (a boolean of the CU), `Cyc_Dom`, and `Cyc_Dom_Year` (which
line, for that CU, in that period), with values dominant, subdominant, and
off-cycle. Modelling those three fields retires the deferral.

### 6. Mint from the source vocabulary, always (Brett Johnson, 2026-08-24)

> "Mint from the source vocabulary always." — Brett Johnson, 2026-08-24 (Q6-4)

The first draft argued for this position; the ruling settles it, **with reach
beyond this PR**. It is therefore written into `CONVENTIONS.md` as new section
**8b) Vocabulary extent — mint from the source vocabulary**, which is the
citable statement of it. Cite that section rather than re-deriving the
argument; this decision records only what it settles here.

- `smn:EvenYearCycleLine` is minted although the SPSR extract holds no
  even-year row. `PKE` is a code DFO maintains — the open-data catalogue
  publishes a separate *Even Year Pink Salmon Conservation Units* dataset —
  and its absence from one extract is a property of that extract.
- `smn:SockeyeSeaTypeLifeHistory` is minted although no coded value in the
  source data says "sea type". The literature documents the type, which under
  Q6-4 is sufficient on its own. **It also turns out to be in the source data
  after all, latently**: DFO's `SER` code covers it (decision 8), so declining
  to mint it would have left `SER` mapping to a concept that is wrong for two
  of its Conservation Units. The ruling and the defect point the same way,
  independently, which is the strongest argument available for the ruling.

ADR-0002's neutral consequence — age-class values 1 through 7 minted "because
those are evidenced by the motivating use case and DFO source" — is **not**
reversed. CONVENTIONS 8b scopes the rule to closed, enumerated code lists and
named typologies; integer ages are an open value space that no source
enumerates the end of, so "as evidenced" remains right there.

### 7. The class/concept boundary is explicit, and no `skos:*Match` crosses it

All thirteen vocabulary terms are `skos:Concept`, in `skos:ConceptScheme`s, in
module 07. None is an `owl:Class`, and none reuses the IRI of one. The five new
object properties are `owl:ObjectProperty` in modules 01 and 02; none is a
concept.

`smn:Life-HistoryCharacteristic` stays an `owl:Class` — it is a characteristic
that can be observed, the parent of `smn:Run`, and a legitimate
`sosa:observedProperty` filler. It is **not** a vocabulary identifier for a
coded column, and this ADR adds an `rdfs:comment` saying so on the term itself,
because the SPSR inventory script currently uses it as one.

Withdrawing the species scheme removes the five `rdfs:seeAlso` links into NCBI
Taxonomy, and with them the question of whether a SKOS mapping predicate may
point at an `owl:Class`. None is asserted anywhere in this change, so the
smn closure adds no rows to the report `dfo-salmon-ontology`'s
`scripts/sparql/skos-match-on-owl-classes.rq` produces.

The three new properties that range on `skos:Concept` do so deliberately:
values come from a named scheme, pointed at with `rdfs:seeAlso`, in the same
way `smn:broodYear` points at `smn:BroodYearBasis`. `rdfs:domain` is omitted on
all five properties, with the omission and its retirement condition recorded in
the module comments — the legitimate subjects have no common superclass in this
build, and an OWL 2 EL-safe union domain is not expressible.

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
| `SEL` | *O. nerka* | `smn:SockeyeLakeTypeLifeHistory` |
| `SER` | *O. nerka* | **`smn:RiverineRearingHabitat` only** — the axis value, not a named type |
| `PKO` | *O. gorbuscha* | `smn:OddYearCycleLine` |
| `PKE` | *O. gorbuscha* | `smn:EvenYearCycleLine` |

`SER` spans two named types that disagree on the duration axis, so no named
type is a correct target for it; the one thing it does assert about every
member is the rearing habitat. Decision 9 is the evidence. A `gcdfo:SER`
concept must therefore **not** carry `skos:exactMatch` or `skos:closeMatch` to
`smn:SockeyeRiverTypeLifeHistory` — the honest mapping is the species
annotations plus `smn:RiverineRearingHabitat`, and anything narrower is a
claim DFO's own data contradicts for `SER-02` and `SER-03`.

**This is what the axes were for.** A design that minted only named types
would have had nothing correct to say about `SER` at all. The axis layer gives
the composite code somewhere true to land, which is an argument for the
two-level shape that was not available when the shape was chosen.

### 9. A defect and a provenance audit that nobody asked for (2026-08-25)

Neither of these was in scope for the 2026-08-24 rulings. Both are corrected
here because the terms are unmerged and the cost of correcting them now is a
diff.

#### 9a. `smn:SockeyeRiverTypeLifeHistory` asserted two things that cannot both be true

The first revision defined the concept as **yearling-or-older** river
residence, and its scope note called it *"One half of the composite DFO
Conservation Unit species code SER, whose other half is the species."* Those
two statements are not jointly satisfiable. Verified 2026-08-25 against DFO's
own published open data and the primary literature:

1. **DFO's Conservation Unit data dictionary** (sheet
   `Data_Dictionary_CU_20260210`, distributed with the Pacific salmon
   Conservation Unit datasets on `open.canada.ca`) glosses the `SP_QUAL`
   field's codes and gives: *"SER - River or Ocean Type Sockeye Salmon"*. The
   French column agrees: *"SER – saumon rouge de type rivière ou océan."* The
   code covers **two** life-history types.
2. **The same dictionary's `LIFE_HISTORY_TYPE` entry** documents the Sockeye
   values as *"(Lake Type, River Type)"* and nothing else. DFO's coded column
   therefore cannot express the second half of DFO's own code. This is why the
   extract's crosstab looked perfectly diagonal.
3. **DFO's CU lookup table** (`CULookuptable_EN.csv`, same distribution)
   renders the code with the shorter label `RIVER TYPE SOCKEYE SALMON`,
   dropping the "or Ocean" half, and files under it — among 20 `SER`
   Conservation Units — `WIDGEON` and `HARRISON RIVER`, whose `FULL_CU_IN`
   values are **`SER-02`** and **`SER-03`**, both `CU_TYPE = Current`.
   Confirmed independently in the dataset's own `SER_CU_SITES_En.csv` and
   `SER_CU_BOUNDARY_En.csv`. (Note for anyone matching on a column called "CU
   index": the field literally named `CU_INDEX` holds `R-02`/`R-03`; the
   `SER-` form is in `FULL_CU_IN`.)
4. **Those two are the sea-type populations.** Beacham & Withler (2017, PLOS
   ONE 12(9):e0183713) study exactly Harrison River and Widgeon Slough as
   sea-type — their Figure 1 caption states that *"Harrison and Widgeon Slough
   are two sea-type Sockeye Salmon populations"* — and give the discriminator:
   sea-type juveniles *"do not spend a winter in fresh water, and thus lack a
   freshwater annulus."* Wood et al. (2008) likewise name *"the small sea-type
   populations in the lower Fraser River (Widgeon Slough and Harrison
   Rapids)"*.
5. **DFO says so itself, in a published Science Advisory Report.** CSAS SAR
   2022/003 (*Recovery Potential Assessment for Fraser River Sockeye Salmon —
   Nine Designatable Units — Part 2*) states: *"DU24 (Widgeon-RT) is the only
   ocean-type population considered in this RPA. It is noted that while DU24 is
   referred to as a river-type population it is not a true river-type
   population; these fish migrate to sea in their first year and do not
   overwinter in freshwater stream habitat"*, and repeats it under Sources of
   Uncertainty: *"Despite being classified as a river-type population, this
   population is closer in life-history to ocean-type Sockeye Salmon in other
   regions"*. **DFO is disowning its own label in its own advice.** That
   single citation is sufficient on its own; the rest of this list is why it
   happened.
6. **The breadth is deliberate and traceable, not a typo.** Holtby & Ciruna
   (2007) — the framework DFO cites for its Conservation Units — names the
   second Sockeye life-history type *"The ocean-, stream- or river-type"*,
   says its juveniles *"rear in flowing water and may smolt soon after
   emergence"*, and glosses it in the document glossary under the heading
   *"River/ocean-types of sockeye"* as juveniles *"adapted to rearing in
   flowing water instead of lakes"*.
7. **And the mechanism is a residual rule, which is why nothing else could
   have happened.** `SER` is not a positive definition. Holtby & Ciruna
   assigned type by asking whether sockeye were seen at, in, or above a lake
   *"larger than approximately 50 ha, then the population was considered of
   the lake-type **otherwise it was considered river-type**."* Everything that
   fails the lake test lands in `SER` by default, so an age-`.0` population has
   nowhere else to go — no evidence about its duration is ever consulted. The
   same document flags the specific case: footnote 27 records that the
   Harrison population's *"spawning location … is unclear. It could be part of
   the Harrison (U/S) lake-type CU or it could be river-type population. **We
   have assumed the latter.**"* The label was an assumption, marked as one, in
   the framework document, and it hardened into a code.

So DFO's category is cut on the **rearing habitat** axis — flowing water
instead of lakes — and the literature's "river-type" is cut on the **duration**
axis. Same string, two different axes, both current. The concept's definition
was right about the literature and wrong about `SER`.

**One more datum, because it shows DFO is not confused about the word so much
as inconsistent about where it applies it.** In the same CU lookup
distribution, Chinook CU `CK-03` is `LOWER FRASER RIVER_FA_0.3` with the
COSEWIC designatable-unit name *"Lower Fraser, Ocean, Fall (Harrison)"* — where
the Gilbert–Rich `0.x` is precisely "no freshwater winter". DFO uses "Ocean"
to mean freshwater age zero, correctly, for chinook in the same file in which
it declines to use it for sockeye. The `SP_QUAL` gloss is the one place in the
CU metadata where the sockeye lump is admitted at all: the dataset title, the
`LIFE_HISTORY_TYPE` vocabulary, the CU names, and the COSEWIC DU names
(*"Harrison River (River-Type) population"*, DU 23; *"Widgeon (River-Type)
population"*, DU 24) all say River Type without qualification.

**Fixed by:** keeping the definition's substance (one to two years, riverine,
at least one freshwater annulus) and replacing the scope note with the
above, stated as a mapping prohibition rather than a caveat. Decision 8's
table is the machine-facing half of the same correction.

#### 9b. The sea-type homograph story was backwards

The first revision's scope note said sea-type *"was Gilbert's 1913 name for
what is now called ocean-type chinook, so the same altLabel denotes a chinook
race in the older literature and a sockeye type in current use."* Gilbert 1913
was read for this revision (Bulletin of the U.S. Bureau of Fisheries 32:1–22;
NOAA SPO scan, cross-checked against an independent archive.org OCR — both
give the same term counts, "sea type" ×19, "stream type" ×16):

- "sea type" first appears on **p. 8, inside the Sockeye section** (pp. 5–11).
  The chinook section does not begin until p. 11.
- Gilbert applies it across **all five species**, and the **chinook** section
  defines its types *by reference to sockeye*: *"king salmon scales exhibit
  the same two types characteristic of the sockeye"* (p. 13).
- Gilbert's contrasting term is **"stream type"**, not lake-type or
  river-type. "lake type" and "river type" appear **zero** times in the
  paper. (The first revision implied otherwise; river-type traces to Semko
  1954, via Wood et al. 2008.)
- It was **chinook that renamed.** Healey (1991, p. 314) designates the
  chinook form *"ocean-type" ("sea-type" in Gilbert 1913)*.

So the sockeye sense of "sea-type" is the **original and continuous** one, and
there is no sockeye/chinook homograph on that string to warn about. The
scope note is **replaced, not softened**.

**The real hazard is "ocean-type", and it is a live one.** DFO uses it in two
mutually exclusive senses:

- **Broad** — CSAS Res. Doc. 2017/074, p. 3: *"River-type is synonymous with
  ocean-type (Holtby and Ciruna, 2007)."* With only two anadromous categories
  in play, "ocean-type" there is the complement of lake-type.
- **Narrow** — CSAS Res. Doc. 2023/003, p. 5: *"'ocean-type' Sockeye migrate
  downstream as subyearlings"* and *"'river-type' Sockeye rear in riverine
  habitats for one to two years"* — two disjoint categories.

The demonstration that they are incompatible is 2023/003's own DU24 footnote
(item 5 above): under 2017/074's stated synonymy, nothing can be river-type
but not ocean-type, so that sentence is not expressible there.

**Fixed by:** keeping `sea-type` as the `skos:prefLabel`; carrying
`skos:altLabel "Ocean Type"@en` because DFO does use it for this concept, but
flagged **AMBIGUOUS and not to be used as a matching key** in the first
sentences of the scope note, with both senses cited; and putting the real
discriminator — **freshwater age zero, no freshwater annulus** — in the
`skos:definition`, so a consumer that matches on meaning rather than string
gets the right answer. A `skos:historyNote` records that the previous
assertion was backwards, because a term that quietly reverses its own history
is worse than one that never had it.

#### 9c. Provenance notes cited sources that do not say what was attributed to them

Every `iao:0000119` in the proposal was checked against its cited source.
Three distinct problems, all now fixed:

| Term(s) | Was cited for | Finding |
|---|---|---|
| all four cycle-line terms | Holtby & Ciruna 2007, "cycle-line axis … which separates odd-year and even-year Pink Salmon" | **"cycle line" occurs zero times** in the 358-page document. Its term is **broodline**, defined in the glossary (p. 327). Substance corroborated, label not — see decision 5. |
| `smn:SockeyeSeaTypeLifeHistory` | Burgner 1991 for "Sockeye sea-type life history" | **Burgner is cited for lake-type, never for sea-type**, by every accessible source that cites him (Gustafson et al. 1997, which cites him 40+ times but not in the paragraph defining the three types; Wood et al. 2008; Beacham & Withler 2017; Hargrove et al. 2016). Replaced with the split attribution below. |
| both axis schemes and all six axis concepts, plus lake- and river-type | Burgner 1991 for the axis distinctions | Burgner 1991 is a paywalled UBC Press chapter that **could not be read**, so nothing in this change should have rested on it. Replaced throughout with sources that were read: Gilbert 1913, Beacham & Withler 2017, Wood et al. 2008. |
| `smn:LifeHistoryTypeScheme`, `smn:LifeHistoryType` | Holtby & Ciruna 2007 for life history as a CU-delimiting axis | **Stands.** DFO's own dataset descriptions state that Holtby and Ciruna aggregated the five species into CUs "based on three primary characteristics: ecotypology, life history and genetics". Wording tightened to claim only that. |

**The corrected attributions, which are a split rather than a swap.** Three
different things were being conflated under one citation:

| What | Correct source |
|---|---|
| the scale-reading term "sea type", and the phrase itself | **Gilbert 1913**, p. 8, Sockeye section — read directly for this revision |
| the *ecotype label* "sea-type sockeye salmon" | **Wood, Riddell & Rutherford 1987**, Can. Spec. Publ. Fish. Aquat. Sci. 96:12–24, which introduces the three labels together in scare quotes and credits Gilbert and Semko separately |
| the label "river-type sockeye" | **Semko 1954** (translated 1960 — one work, two citation years), per Wood et al. 1987 and restated in Wood et al. 2008 |
| lake-type, the spawning-habitat classification, and European age notation | **Burgner 1991** — genuinely, which is why it is now cited on `smn:SockeyeLakeTypeLifeHistory` and nowhere else |

Two honesty notes carried into the terms themselves. Burgner 1991 is a
paywalled UBC Press chapter that **could not be read**, so its citation on
lake-type is recorded as the customary attribution rather than relied on, and
says so. And the pairing is **contested**: Pavey et al. 2010 inverts it,
crediting Semko with sea-type and Gilbert with river-type. Wood et al. 1987 is
earlier and is the coining paper, so it is followed — but the dispute is
recorded on the term rather than silently resolved, which is what a
provenance note is for.

The load-bearing lesson is narrower than "check citations". Holtby & Ciruna
2007 *does* contain the string "sea-type" — exactly once, on p. 80, inside a
**reference-list entry** for Gustafson & Winans 1999, whose title is
*"Distribution and population genetic structure of river- and sea-type sockeye
salmon"*. A full-text search for the term therefore **succeeds**, and a reader
who stops at the hit count concludes the document supports a lake/river/sea
trio. It does not: its sockeye trio is lake-type, river/ocean-type, and
**kokanee**, and it excludes kokanee from CU definition explicitly (footnote
19, p. 17), leaving two. A hit in a bibliography is a citation of someone
else's claim, and it is indistinguishable from a real hit until you look at
the page.

### 10. The prefix rewrite stands (Brett Johnson, 2026-08-24)

> "Yeah fix that once and be done with it, accepting the ugly diff." — Brett
> Johnson, 2026-08-24 (Q6-5)

The generator fix in `scripts/build_flat_smn_ttl.py` and the resulting
one-time rewrite of `salmon-domain-ontology.ttl` and `docs/smn.ttl` from
`<https://w3id.org/smn/Term>` to `smn:Term` are confirmed rather than reduced
to a narrower fix. Details are in the Neutral consequences below and in
`knowledge/data/builds-and-import-graph.md`.

## Consequences

### Positive

- The axes become independently statable, queryable, and mappable. A consumer
  that needs only juvenile rearing duration is not forced to adopt a named
  race, a species claim, or a genetic-structure claim.
- The label hazards are documented at term level, where a contributor or a
  matcher will encounter them, rather than in an ADR nobody reads at mapping
  time — and, after decision 9b, they are documented on the label that is
  actually hazardous.
- A consumer that maps DFO's `SER` code by string similarity now has a term
  that tells it not to. That is the single highest-value output of this
  change, and it is the one nobody asked for.
- The cycle-line terms now say something true for every population rather than
  something true for pink. The strong claim is still available, on its own
  property, for the populations that support it.
- The redundancy finding is resolvable at the source: once `CU_ID` decomposes,
  `LIFE_HISTORY_TYPE` carries no information the CU identifier does not, and
  SPSR can drop it rather than mint a term for it.
- No taxonomic-authority dispute is imported into `smn:`, and the one
  `rdfs:seeAlso` that is asserted was verified to content-negotiate to
  RDF/XML rather than to an HTML page.
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
- `smn:LifeHistoryTypeScheme` holds Sockeye types only, so it is broad in
  definition before it is broad in content — and deliberately stays that way
  until a species' bundle is shown to be stable enough to name.
- Anyone who needs a species **IRI** still has none from `smn:`, and under
  Q6-1 never will. A `dwc:scientificNameID` literal is not a graph node: you
  cannot traverse it, and a consumer wanting to reason over taxonomy must
  bring its own taxon graph and join on the LSID string.
- Species is now asserted on three concepts by repetition. If a fourth Sockeye
  type is minted the literal and the identifier are copied again, and nothing
  in the artifact stops the fourth copy from disagreeing with the first three.
  A validator, not a term, is the answer if that becomes real.
- The `SER` correction makes the vocabulary **less** able to close
  `dfo-salmon-ontology` issue #68 cleanly than the first revision claimed: a
  `gcdfo:SER` code has no named type to point at, so the gcdfo work is larger
  than "decompose each code onto one shared term".

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
- Using `smn:` and `dwc:` in predicate position for the first time exposed a
  reproducibility defect in `scripts/build_flat_smn_ttl.py`: the merged graph
  carried no prefix bindings, so rdflib numbered predicate namespaces `ns1:`,
  `ns2:`, ... in hash-randomized order. One such namespace had been stable by
  luck; two were not, and eight runs of the generator on this branch produced
  four distinct files. Fixed in this change by binding the prefixes the modules
  declare, which also rewrites every `<https://w3id.org/smn/Term>` in the flat
  TTL and `docs/smn.ttl` as `smn:Term`. That is a large, semantically empty
  diff and it is unrelated to the terms proposed here; it is included because
  the proposal is what made the defect live. See
  `knowledge/data/builds-and-import-graph.md`.

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

**`dfo-salmon-ontology` and DFO data stewardship** — the finding in decision 9a
is about DFO's published data, not about this ontology, and it outlives this
PR. DFO's `LIFE_HISTORY_TYPE` column cannot express a life-history type that
DFO's own `SP_QUAL` code admits, so every `SER` row in every downstream extract
is labelled `River Type` regardless of which type it is. Worth raising with the
CU data stewards independently of whether this ADR is accepted.

**SPSR** — stop using `smn:Life-HistoryCharacteristic` as a `vocabulary_iri`
for SKOS codes (`spsr-inventory.r:842`); it is an `owl:Class`. Point
life-history codes at `smn:LifeHistoryTypeScheme` and cycle codes at
`smn:CycleLineScheme`. Given the redundancy finding, the better change is to
derive both from `CU_ID` and retire `LIFE_HISTORY_TYPE` — but note that
deriving life-history type from `CU_ID` is **not** correct for `SER`, and the
derivation must yield the rearing-habitat axis value rather than a named type
for those rows.

**PSC** — no change required, and nothing to retract. If PSC wants to map into
these schemes it appends the IRIs to `allowed_object_ids` in
`data/external-sources.json`, adds reviewed rows to
`data/external-mapping-review.csv`, and cuts a release.

## Q6-8 — are the three Sockeye types flat peers? NOT RULED

This is the one open question that changes what the artifact contains, and it
is deliberately left to Brett. **As proposed, the three types are flat
siblings**, each `skos:broader smn:LifeHistoryType`. That is the status quo
carried forward from the first revision, not a finding — and the evidence
gathered for this revision says it is wrong. What it does **not** say is which
of two replacements is right.

### The evidence, and what it actually says

Every source groups river with sea, against lake. But the grouping is stated as
a **nesting**, not as a pairing, and the difference matters:

- **Wood, Bickham, Nelson, Foote & Patton 2008** (Evolutionary Applications
  1:207–221): *"We consider the river-type form to be a special case of the
  sea-type life history because, by definition, neither sea-type nor
  river-type sockeye rear in lakes."* And then, in the same passage: *"For
  clarity, we will refer to them collectively as the 'sea/river ecotype'."*
  They run three ecotypes: lake, **sea/river**, kokanee.
- **Beacham & Withler 2017** restate it — *"The river-type form has been
  considered to be a special case of the sea-type form"* — and run three
  ecotypes with **no river-type**: sea-type, lake-type, kokanee. "river-type"
  appears 6 times against sea-type's 51, all in the definitional
  introduction.
- **DFO carries two values, not three:** `SEL` and `SER`, the latter glossed
  "River **or Ocean** Type", with Holtby & Ciruna's glossary heading
  *"River/ocean-types of sockeye"*, defined as rearing *"in flowing water
  instead of lakes"* — and assigned by the residual rule in decision 9a item
  7. The lake/non-lake cut is DFO's operative one.
- **NOAA** writes "river/sea-type" in 20 of 37 uses.

**The nesting is a terminological artifact, and the sources themselves fix
it.** Wood et al.'s sentence uses "sea-type" twice in two different senses: the
*broad* sense (anything not rearing in a lake), under which river-type is a
special case, and the *narrow* sense (rears weeks to months, no freshwater
winter), under which river-type is its opposite on the duration axis. That is
the same broad/narrow collapse that makes "ocean-type" unusable in decision 9b,
one species-term over. Wood et al. resolve it by coining a **third name** for
the broad sense — *"For clarity"*, in their words — rather than by nesting one
narrow term under another.

This matters for what gets minted, because the literal nested encoding is
**incoherent given what the terms now assert**. `smn:SockeyeRiverTypeLifeHistory`
carries `smn:YearlingFreshwaterResidence`; `smn:SockeyeSeaTypeLifeHistory`
carries `smn:SubyearlingFreshwaterResidence`. Making the first
`skos:broader` the second would say every river-type fish is a sea-type fish
while the two disagree on the axis that defines them. **A `skos:broader` edge
between them would import the very ambiguity the sources coined a term to
escape.**

### What each answer costs, from here

**(a) Flat peers — confirm the status quo. Cost: nothing.** No IRI changes, no
regeneration. Delete the "pending a ruling" clause from
`smn:LifeHistoryType`'s scope note and the scheme is done. Consumers wanting
the sea/river grouping select on
`smn:hasJuvenileRearingHabitat smn:RiverineRearingHabitat`, which is exact,
already present, and one triple pattern. **The honest argument for (a) is that
the grouping is already derivable and a named concept adds a level to every
query that does not want it.** The honest argument against is that no source
treats these as three coordinate peers, so the artifact would be asserting a
structure nobody uses.

**(b) Mint the group concept — the faithful encoding of the nesting. Cost: one
concept, two edited triples.** Mint
`smn:SockeyeSeaRiverTypeLifeHistory`, prefLabel "Sea/river-type Sockeye life
history" — Wood et al.'s own term, with a citation behind it — give it
`skos:broader smn:LifeHistoryType` and
`smn:hasJuvenileRearingHabitat smn:RiverineRearingHabitat`, and re-point the
`skos:broader` on `smn:SockeyeRiverTypeLifeHistory` and
`smn:SockeyeSeaTypeLifeHistory` from `smn:LifeHistoryType` to it. Regenerate.
Module 07 goes 14 schemes / 62 concepts to 14 / 63. Consequences:

  - **PSC is unaffected.** Its pipeline composes `skos:broadMatch` through
    `skos:broader*` chains of any depth, and its SHACL requires *at most one*
    `skos:broader` per concept, which a three-level chain still satisfies.
  - **`gcdfo:SER` gains a named target**, which decision 8 says it currently
    lacks — `skos:closeMatch` to `smn:SockeyeSeaRiverTypeLifeHistory` becomes
    the cleanest available statement of what the code means. This argument did
    not exist before the `SER` defect was understood, and it is the strongest
    one for (b).
  - Decision 4's table, the `smn:LifeHistoryType` scope note, and decision 8's
    mapping row are edited to match. Roughly a 40-line ADR diff.

**(b′) The literal nesting — `river skos:broader sea`. Cost: one edited triple,
and a contradiction.** Cheapest of all in triples, and refused above: it
asserts that a yearling migrant is a subyearling migrant. If it is wanted
anyway, the axis assertions on `smn:SockeyeRiverTypeLifeHistory` would have to
be removed, which dismantles decision 4. Recorded so the option is visibly
considered rather than quietly skipped.

### The two things that argue for waiting

1. **Nothing in this vocabulary can say "mixed."** A population that is part
   one type and part another has no representation, and a named group makes
   that gap sharper rather than softer. Holtby & Ciruna (2007, p. 9) refused to
   split chinook CUs by life-history type for exactly this reason — *"many
   populations in Canada are mixtures of the two types"* — and the same
   objection is available against any partition this scheme asserts.
2. **(b) stays exactly as cheap later as it is today**, because no released IRI
   is involved either way, and it becomes easier to justify once `gcdfo`
   actually needs a target for `SER`.

**What is NOT prepared, deliberately.** No `smn:SockeyeSeaRiverTypeLifeHistory`
is minted, commented out, or referenced in the artifact. No mixture model is
proposed. Both are Brett's to call.


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
3. **Is `"Ocean Type"` wanted as an `skos:altLabel` at all?** Decision 9b
   carries it because DFO uses it for this concept, flagged ambiguous in the
   scope note. The case against is that an `altLabel` is a matching key and a
   scope note is not, so flagging it in prose does not stop a lexical matcher
   from using it. Dropping it costs one line and loses the ability to find the
   concept from DFO's own word.

**Resolved since the first revision, and recorded here so the review does not
re-litigate them:** species (Q6-1, decision 1); `dwc:scientificName` on a
life-history concept (Q6-2 — *"OK yeah. I guess that makes sense so that it's
clear that some life histories only apply to certain species"*); two axis
properties rather than one generic one (Q6-3, decision 2); whether
`smn:SockeyeSeaTypeLifeHistory` is wanted (Q6-4, decision 6 — and decision 9a
shows it is in the source data after all); the prefix rewrite (Q6-5,
decision 10).


## More Information

### Sources read for the 2026-08-25 revision

Everything in decisions 9 and Q6-8 rests on a source that was retrieved and
read for this revision, not on a report of one. Where that was not possible it
is said so explicitly.

**DFO published data** (all retrieved 2026-08-25 from the *River Type Sockeye
Salmon (Oncorhynchus nerka) Conservation Units, Sites & Status* dataset on
`open.canada.ca`, dataset id `6c8bc9b9-5f99-48fc-bd28-3c0af2ec379e`):

- `Data_Dictionary_CU_EN_FR.xlsx`, sheet `Data_Dictionary_CU_20260210` — the
  `SP_QUAL` gloss *"SER - River or Ocean Type Sockeye Salmon"* and the
  `LIFE_HISTORY_TYPE` value list *"Sockeye Salmon (Lake Type, River Type)"*.
  The same string appears in an archived July-2025 edition of the dictionary,
  so it is not a one-off.
- `CULookuptable_EN.csv`, `SER_CU_SITES_En.csv`, `SER_CU_BOUNDARY_En.csv` —
  `WIDGEON` / `SER-02` and `HARRISON RIVER` / `SER-03`, both `CU_TYPE =
  Current`, among 20 `SER` Conservation Units.
- `REFERENCE INFORMATION_SERiver.docx` — DFO's own reference list for the
  dataset, which names Holtby & Ciruna 2007 as the Conservation Unit
  framework.

**DFO advice and framework documents:**

- Holtby, L.B. and Ciruna, K.A. 2007. *Conservation Units for Pacific Salmon
  under the Wild Salmon Policy.* DFO Can. Sci. Advis. Sec. Res. Doc. 2007/070.
  **Read in full (358 pp.).** Verified in it: "sea-type" occurs exactly once,
  in a reference-list entry (p. 80); "cycle line" occurs zero times; the
  **Broodline** glossary entry (p. 327); the sockeye trio at §9.2 and the
  glossary heading *"River/ocean-types of sockeye"*; the 50-ha residual rule;
  footnote 27 on the Harrison assumption; and the chinook non-split at p. 9.
- DFO Can. Sci. Advis. Sec. **Sci. Advis. Rep. 2022/003.** *Recovery Potential
  Assessment for Fraser River Sockeye Salmon (Oncorhynchus nerka) — Nine
  Designatable Units — Part 2.* **Read.** The DU24 Widgeon-RT disavowal, in
  both the life-history section and Sources of Uncertainty.
- DFO Can. Sci. Advis. Sec. Res. Doc. **2017/074** (broad "ocean-type", p. 3:
  *"River-type is synonymous with ocean-type"*) and **2023/003** (narrow
  "ocean-type", p. 5). The pair is the evidence that the label is ambiguous
  in current DFO usage.

**Literature:**

- Gilbert, C.H. 1913. *Age at maturity of the Pacific coast salmon of the
  genus Oncorhynchus.* Bulletin of the United States Bureau of Fisheries
  32:1–22. **Read, and cross-checked against an independent OCR of the same
  volume**; both give the same counts ("sea type" ×19, "stream type" ×16,
  "lake type"/"river type" ×0). Note that two citations for this paper are in
  circulation — the U.S. Bulletin version above, and a British Columbia
  Commissioner of Fisheries reprint (1912 report, pp. 57–70). Only the
  Bulletin version was read.
- Wood, C.C., Riddell, B.E., and Rutherford, D.T. 1987. Can. Spec. Publ. Fish.
  Aquat. Sci. 96:12–24 — the paper that establishes the sea-type/river-type/
  lake-type *labels*.
- Wood, C.C., Bickham, J.W., Nelson, R.J., Foote, C.J., and Patton, J.C. 2008.
  *Recurrent evolution of life history ecotypes in sockeye salmon.*
  Evolutionary Applications 1:207–221. **Read.** The "sea/river ecotype"
  coinage and the special-case sentence.
- Beacham, T.D. and Withler, R.E. 2017. *Population structure of sea-type and
  lake-type sockeye salmon and kokanee in the Fraser River and Columbia River
  drainages.* PLOS ONE 12(9):e0183713. **Read.** The freshwater-annulus
  discriminator; Harrison and Widgeon Slough as the sea-type populations; and
  that both sea-type and river-type juveniles rear in river habitats.
- Semko 1954 (translated 1960) — the origin of "river-type", cited via Wood et
  al. 1987 and 2008, **not read**.
- Healey, M.C. 1991. *Life history of chinook salmon (Oncorhynchus
  tshawytscha).* In Groot, C. and Margolis, L. (eds.), *Pacific Salmon Life
  Histories*, UBC Press. **Read** (p. 314 for the ocean-type/sea-type gloss;
  also the source for tactical versus race-defining variation and the
  Sacramento winter run).
- Burgner, R.L. 1991. *Life history of sockeye salmon (Oncorhynchus nerka).*
  In the same volume, pp. 3–117. **NOT read** — paywalled. It is the customary
  citation for lake-type, recorded as such on one term and relied on nowhere.
  The first draft cited it for sea-type and for both axes; see decision 9c.
- Waples, R.S., Teel, D.J., Myers, J.M., and Marshall, A.R. 2004.
  *Life-history divergence in Chinook salmon: historic contingency and
  parallel evolution.* Evolution. Moran, P., Teel, D.J., Banks, M.A., et al.
  2013. *Divergent life-history races do not represent Chinook salmon
  coast-wide.* Canadian Journal of Fisheries and Aquatic Sciences.
- Rieman, B.E. and McIntyre, J.D. 1993. *Demographic and habitat requirements
  for conservation of bull trout.* USDA Forest Service GTR INT-302 — the
  potamodromous vocabulary refused in the rearing-habitat scope note.
- Pavey et al. 2010 (TAFS 139:1584–1594) — records the **inverted** attribution
  of "sea-type" to Semko and "river-type" to Gilbert. Noted as contested on
  `smn:SockeyeRiverTypeLifeHistory` rather than silently resolved.

**Identifier checks, by request rather than by report:**

- WoRMS, 2026-08-25: AphiaID 254569, *Oncorhynchus nerka* (Walbaum, 1792),
  `status: accepted`, LSID `urn:lsid:marinespecies.org:taxname:254569`. Under
  `Accept: application/rdf+xml` the taxon page redirects to
  `authority/metadata.php?lsid=…` and returns `application/rdf+xml`.
- NCBI Taxonomy OBO PURL, 2026-08-17: `text/html` under `text/turtle`,
  `application/rdf+xml`, and `application/ld+json` alike. This is the contrast
  that admits the WoRMS link and excluded the NCBI ones.

### Rulings recorded in this ADR

- **2026-08-17 (Brett Johnson):** steelhead is in scope; life-history type is
  asserted at CU / population / stock level and not for individual fish; a
  species reference, if needed later, belongs in `smn` and never in `gcdfo`.
- **2026-08-24/25 (Brett Johnson):** Q6-1 species as literal + WoRMS ID, no
  minted species concepts or classes (decision 1); Q6-2 keep
  `dwc:scientificName` on life-history concepts (decision 1); Q6-3
  `hasLifeHistory` plus two specific axis properties (decision 2); Q6-4 mint
  from the source vocabulary always (decision 6, and `CONVENTIONS.md` §8b);
  Q6-5 the prefix rewrite stands (decision 10). **Q6-8 is not ruled.**

### Other evidence

- `dfo-salmon-ontology` issues #68, #74, #70 (evidence pass 2026-08-16);
  taxonomic-authority and life-history literature review 2026-08-17.
- Source code list: SPSR data dictionary crosswalk, `demo_cu`/`CU_ID` notes
  column. CU individuation counts (19 `PKO`, 14 `PKE`, `FRASER RIVER` as both
  `PKO-01` and `PKE-9005`, no sockeye CU split by line, Fraser Pink
  `Cyclic = FALSE`) from the DFO Conservation Unit tables.


## Related

- [ADR-0002](0002-year-age-basis-dimensions-and-abundance.md) — the
  orthogonal-schemes precedent, and the mint-from-evidence consequence that
  decision 6 scopes rather than reverses.
- `CONVENTIONS.md` **section 8b**, *Vocabulary extent — mint from the source
  vocabulary*, which decision 6 adds and which has reach beyond this ADR: it
  also governs `PKE` and the Pacific Fishery Management Area subareas. Cite it
  rather than re-deriving the argument.
- `CONVENTIONS.md` sections 2, 3, 4, 8, 10, and 11.
- `knowledge/data/builds-and-import-graph.md` — the flat-TTL determinism
  defect and its retirement condition (decision 10).
