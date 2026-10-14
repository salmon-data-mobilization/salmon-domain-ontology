---
type: InformationObject
title: Cross-vocabulary alignment state
description: The verified relationship between smn, gcdfo 0.0.8, and the PSC controlled vocabulary as of 2026-08-12 — the live pun, the minted term, the unbridged duplication, and why PSC maps to gcdfo but refuses smn.
status: draft
tags: [gcdfo, psc, sssom, alignment, methods]
psc:
  id: smn:data:cross-vocabulary-alignment-state
  contexts: [smn:context:ontology-alignment-pass-2026]
---

Verified 2026-08-12: smn main `3995a17`, gcdfo main `c7a5425` (release
0.0.8), psc-salmon-vocabularies branch `feature/fair-mapping-products-roadmap`
(`8e50d81`). The step-3 resolutions below are verified against gcdfo
main `48b5dbb` (PR #78 merged 2026-08-14 with Brett's approval via
admin bypass of the review ruleset).

## The boundary is now structural, not prose

`dfo-salmon.ttl:200` `owl:imports <https://w3id.org/smn>`; gcdfo subclasses
smn upper classes 26 times and re-declares 39 `smn:` subjects as MIREOT-style
mirrors (with `rdfs:isDefinedBy` pointed at smn per gcdfo's ownership rule).
Any earlier claim that the smn/gcdfo boundary is "prose-only" is stale.

## Defects in the merged closure

- ~~Live pun~~ **Resolved 2026-08-13 (step 2):** smn migrated its six method
  OWL classes to SKOS concepts in `smn:MethodScheme` (module 07), each
  instance-typed `sosa:Procedure`, IRIs unchanged — so `smn:EnumerationMethod`
  is now `skos:Concept` on both sides and the merged closure has zero
  dual-typed IRIs (verified against the flat build). PSC's wrong-kind
  objection (`sdo-alignment-gap.md`) no longer applies; updating their doc
  and drafting psc→smn SSSOM rows is step 4.
- ~~Minted foreign term~~ **Resolved 2026-08-13 (step 3, gcdfo PR #78):**
  `smn:FisheriesReferencePointLower` is re-namespaced to
  `gcdfo:FisheriesReferencePointLower` (policy-scoped like its sibling
  reference-point terms); smn's two alignment rows retargeted.
- ~~Unbridged duplication~~ **Resolved 2026-08-13 (step 3, gcdfo PR #78):**
  `mappings/gcdfo-to-smn.sssom.tsv` publishes the boundary as data — 32
  reviewed rows (incl. four replacement rows for the removed duplicate
  properties) covering the age/year family, the renamed age classes,
  CatchYear, and EscapementEstimate, with predicates graded by smn's own
  migration provenance (Migrated → exactMatch, Adapted → closeMatch) and
  both sides version-pinned. The 2026-08-13 recon found **zero**
  same-name-different-semantics collisions — the old "~55 collisions" figure
  counted MIREOT mirrors and migrated-identical pairs.
- ~~Zero-delta duplicates~~ **Resolved 2026-08-13 (step 3, gcdfo PR #78):**
  the four duplicate object properties are removed; consumers use the smn
  twins directly.

## Why PSC maps to gcdfo but refuses smn — the decisive field evidence

The PSC CV is SKOS-only, CSV-authoritative, with mappings living exclusively
in SSSOM TSVs gated by a review CSV and an allow-list of pinned sources.
Released: **18 `skos:exactMatch` + 2 `closeMatch` to gcdfo** (pinned to gcdfo
0.0.8, commit `c7a54251`) and 3 AGROVOC `closeMatch`. And
`docs/sdo-alignment-gap.md` **explicitly refuses any psc→smn mapping set
because smn's method anchor is an `owl:Class`, not a `skos:Concept`** — the
"wrong-kind" objection. gcdfo's ADR-001 ("Methods as SKOS Concepts") is
therefore winning in practice: the OWL-vs-SKOS methods decision is already
determining which cross-vocabulary mappings exist.

Consequences for the alignment pass (steps 2–4 of the execplan): migrating
smn methods to SKOS (with thin `sosa:Procedure` instance typing) resolves the
pun and dissolves PSC's objection in one move; the smn↔gcdfo boundary then
gets one SSSOM set covering the ~55 term-name collisions and the age/year
family.

## What PSC actually anchors on smn today (verified 2026-08-17)

Verified against `psc-salmon-vocabularies` `v0.1.0-alpha.3` (4 schemes, 38
concepts). The step-2 methods migration worked: PSC's refusal is lifted and a
`psc-to-smn` mapping set now exists.

- **One released smn target, one predicate.** `dist/mappings/psc-to-smn.sssom.tsv`
  holds 9 rows, all `skos:broadMatch`, all onto `https://w3id.org/smn/EnumerationMethod`,
  pinned to `object_source_version 0.0.3-f7205ee…`. That is the entire live
  psc→smn surface. `psc-to-gcdfo` (19 rows) and `psc-to-agrovoc` (3) contain
  no smn objects.
- **The allow-list is a hard gate.** `data/external-sources.json` permits
  exactly three smn IRIs — `EnumerationMethod`, `Stock`, `SpawnerStageContext`
  — and `src/psc_vocab/build.py` raises on any object outside it. Adding a new
  smn target costs PSC three coordinated edits plus a release; it is not a
  free-form mapping surface.
- **`broadMatch` composes only through `exactMatch`.** PSC deferred
  PSC-CV-000017 → `smn:EnumerationMethod` because its psc→gcdfo predicate is
  `closeMatch`, which does not support the composition. An smn term reachable
  only through a `closeMatch` chain is, in practice, unmappable by PSC.
- **Wrong-kind rejection is enforced, not rhetorical.** PSC's
  `semantic-search-receipt.json` records `smn:ObservedRateOrAbundance` rejected
  `rejected_wrong_kind_and_too_broad` with `native_type: owl:Class`, and
  `smn:LifePhase` rejected `rejected_too_broad` for both smolt and fry. Breadth
  fails PSC as surely as wrong kind does.
- **Recorded, unfilled asks on smn.** `candidates/stock-recruit-measurements/data/decomposition-review.csv`
  carries four blank-IRI gaps against `component_source: smn` — narrow
  life-stage concepts (fry, smolt), a female-sex constraint, and an
  unspawned-egg adjustment method — held blank on the stated rule that "a broad
  or wrong-kind term is not a substitute." `docs/sdo-alignment-gap.md` names a
  shared analytical-method concept as the natural smn admission proposal.
- **PSC has minted nothing on the species, life-history-type, run-timing,
  cycle-line, or juvenile-rearing axes** — zero concepts, zero schemes, across
  every CSV/TTL/JSON in the repo. Shared terms on those axes have no PSC
  parallel to supersede.

## PSC pipeline constraints to budget for

- SHACL shapes are `sh:closed` — any SKOS enrichment (altLabels, in-graph
  mappings, new statuses) is a build-breaking change requiring coordinated
  shape + `build.py` + CSV edits.
- `build.py:672` hard-codes SSSOM `mapping_date`; `build.py:18-30` hard-codes
  scheme ids and the contiguous concept-id range.
- PSC's promotion gate requires reuse by "two independently governed
  organizations" — anchor via mappings, do not attempt term promotion.
- gcdfo `docs/ADR.md` numbering disagrees with `docs/adr/` files (ADR-005/006
  refer to different decisions in each place).
