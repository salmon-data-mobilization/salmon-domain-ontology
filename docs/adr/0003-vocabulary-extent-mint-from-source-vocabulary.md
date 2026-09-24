# ADR-0003: Vocabulary extent — mint from the source vocabulary

> **Split note (2026-09-24), not part of the original text.** This ADR is one
> of four into which ADR-0003, *Life-history axes, cycle lines, and no species
> vocabulary*, was split, one per part of salmon-domain-ontology pull request
> 27 (file `docs/adr/0003-life-history-axes-cycle-lines-no-species.md` at
> commit `949ed95`). It is the part that adds `CONVENTIONS.md` section 8b, and
> it mints no term. The split rewords nothing. Every paragraph that is not a
> split note is the original text, copied verbatim, and a passage that
> concerns more than one part is copied into each, except the passages the
> next note lists, which were corrected after the split without a ruling. The
> only additions are split notes like this one, and HTML comments that mark
> passages which are salmon-domain evidence rather than decisions. The DFO
> sockeye and pink codes the one such comment here marks are recorded in
> salmon-knowledge-commons, in `concepts/sockeye-ser-code-scope.md` and
> `concepts/pink-salmon-line-definitions.md`; the SPSR extract's counts are
> not. Knowledge-log entries dated 2026-08-17 and 2026-08-25 that cite
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

> **Corrections after the split (2026-09-24), not part of the original text.**
> The passages below were corrected without a ruling, because each was an
> error of fact, citation or cross-reference that the research on the split
> found. The pull request that carries this ADR lists each correction with its
> original wording and its evidence. Line numbers are the combined ADR's.
>
> - Status: the corrections are decision 9, not decision 8 (a stale
>   cross-reference). (line 24)

## Status

Proposed

Date: 2026-08-17. Revised 2026-08-25. This ADR and the terms it describes are
a **proposal for review**, not an accepted decision. The terms are written into
modules 01, 02, and 07 so the proposal is concrete and reviewable rather than
prose about terms that do not exist.

> **Split note.** This part mints no term; the sentence about modules 01, 02 and
> 07 describes the combined proposal.

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
about and that nobody had questioned**. Those corrections are decision 9, and
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

### 6. Mint from the source vocabulary, always (Brett Johnson, 2026-08-24)

> "Mint from the source vocabulary always." — Brett Johnson, 2026-08-24 (Q6-4)

The first draft argued for this position; the ruling settles it, **with reach
beyond this PR**. It is therefore written into `CONVENTIONS.md` as new section
**8b) Vocabulary extent — mint from the source vocabulary**, which is the
citable statement of it. Cite that section rather than re-deriving the
argument; this decision records only what it settles here.

> **Split note.** The two applications this decision records, one bullet per
> minted term, travel with the parts that mint those terms: ADR-0006 (the
> even-year cycle line) and ADR-0005 (the Sea-type Sockeye life history).

ADR-0002's neutral consequence — age-class values 1 through 7 minted "because
those are evidenced by the motivating use case and DFO source" — is **not**
reversed. CONVENTIONS 8b scopes the rule to closed, enumerated code lists and
named typologies; integer ages are an open value space that no source
enumerates the end of, so "as evidenced" remains right there.

## More Information

### Rulings recorded in this ADR

- **2026-08-24/25 (Brett Johnson):** Q6-1 species as literal + WoRMS ID, no
  minted species concepts or classes (decision 1); Q6-2 keep
  `dwc:scientificName` on life-history concepts (decision 1); Q6-3
  `hasLifeHistory` plus two specific axis properties (decision 2); Q6-4 mint
  from the source vocabulary always (decision 6, and `CONVENTIONS.md` §8b);
  Q6-5 the prefix rewrite stands (decision 10). **Q6-8 is not ruled.**

> **Split note.** Of the five rulings in this bullet, this ADR records Q6-4
> only. Q6-1, Q6-2, Q6-3 and Q6-5 are recorded in ADR-0005, and Q6-3's two axis
> properties in ADR-0004.

## Related

- [ADR-0002](0002-year-age-basis-dimensions-and-abundance.md) — the
  orthogonal-schemes precedent, and the mint-from-evidence consequence that
  decision 6 scopes rather than reverses.
- `CONVENTIONS.md` **section 8b**, *Vocabulary extent — mint from the source
  vocabulary*, which decision 6 adds and which has reach beyond this ADR: it
  also governs `PKE` and the Pacific Fishery Management Area subareas. Cite it
  rather than re-deriving the argument.
- `CONVENTIONS.md` sections 2, 3, 4, 8, 10, and 11.
