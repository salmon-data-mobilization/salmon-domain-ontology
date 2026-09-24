# Bundle log

- 2026-08-12 — Bundle seeded from step-0 recon of the ontology alignment pass
  (metasalmon roadmap S9). Five cards: domain, context, and three
  InformationObject cards carrying the verified builds/imports facts, the
  F1–F8 conventions findings, and the cross-vocabulary alignment state.
  All cards `status: draft`; sources cited inline as file:line against the
  commits named in each card. Validation: `psc-okf check --tier capture`.
- 2026-08-13 — Codex review fixes: corrected the module-02 card (class-level
  property assertions are legal OWL 2 DL punning, not OWL Full; remedy is a
  targeted SPARQL report plus axiom rewrite, not the DL gate) and registered
  the bundle in docs/entrypoints.md.
- 2026-08-13 — Portability pass: removed all absolute filesystem paths (new
  hub rule); validation command is now relative to a sibling psc-data-systems
  checkout. Cross-repo references updated for metasalmon's notes/ -> knowledge/
  migration.
- 2026-08-13 — S9 step 1 (alignment semantics): F1-F7 fixed, F8 property-side
  fixed; conventions cards updated to reflect the landed state.
- 2026-08-13 — S9 steps 2+5: methods-as-SKOS migration (smn:MethodScheme) and
  smn:StatisticalModifierScheme landed; cross-repo pun resolved; cards updated.
- 2026-08-13 — PR 22 review: added ontology/shapes/method-shapes.ttl (the
  enumeration-method value constraint, SKOS-native via skos:broader*,
  behaviourally tested with pyshacl) and refreshed the conventions card's
  module-07 inventory (10 schemes / 49 concepts).
- 2026-08-13 — S9 step 1b (tooling): verify targets are read-only, generated
  modules 08/09 gain a drift gate, CONVENTIONS 5b checks + method-shapes
  behavioural check wired into make test and CI, new ELK reasoner-gate CI job
  (passes: consistent, zero unsatisfiable classes), views documented as
  non-dereferenceable identifiers.
- 2026-08-13 — S9 step 3 (smn side): the two alignment rows referencing the
  never-declared smn:FisheriesReferencePointLower retarget the re-namespaced
  gcdfo:FisheriesReferencePointLower (gcdfo PR 78 carries the rename and the
  new gcdfo-to-smn SSSOM mapping set, 28 rows, pinned both sides).
- 2026-08-25 — ADR-0003 reworked on five rulings (Brett Johnson, 2026-08-24/25)
  plus a defect and a citation audit that were **not** asked for. Rulings:
  species is a `dwc:scientificName` literal plus a WoRMS `dwc:scientificNameID`
  and **smn mints no species concept or class, ever** (Q6-1); keep
  `dwc:scientificName` on life-history concepts (Q6-2); **three** life-history
  properties — `smn:hasLifeHistory`, `smn:hasJuvenileFreshwaterResidenceDuration`,
  `smn:hasJuvenileRearingHabitat` — and no generic axis-value property (Q6-3);
  **mint from the source vocabulary always** (Q6-4), now `CONVENTIONS.md` §8b
  with reach beyond this PR; the flat-TTL prefix rewrite stands (Q6-5).
  **Q6-8 (are the three Sockeye types flat peers) is NOT ruled** and nothing on
  the branch pre-empts it.
- 2026-08-25 — **`SER` is not a code for river-type sockeye, and the shared
  layer must not map it as one.** Verified against DFO's own published data:
  the Conservation Unit data dictionary glosses `SP_QUAL` `SER` as *"River or
  Ocean Type Sockeye Salmon"* (FR: *"type rivière ou océan"*), while the
  `LIFE_HISTORY_TYPE` field it accompanies offers only *"Lake Type, River
  Type"* — DFO's coded column cannot express the second half of DFO's own
  code. `WIDGEON` (`FULL_CU_IN` = `SER-02`) and `HARRISON RIVER` (`SER-03`) are
  filed under it and are the two populations Beacham & Withler (2017) study as
  **sea-type**, defined by lacking a freshwater annulus. DFO CSAS **SAR
  2022/003** says of DU24 Widgeon-RT that *"it is not a true river-type
  population; these fish migrate to sea in their first year"*. The mechanism is
  a residual rule in Holtby & Ciruna 2007 — lake-type if seen at/in/above a
  lake >≈50 ha, *"otherwise it was considered river-type"* — plus footnote 27,
  which records the Harrison assignment as an assumption (*"We have assumed the
  latter"*). Consequence for mapping: `SER` decomposes onto the species
  annotations plus `smn:RiverineRearingHabitat` **only**, never onto a named
  life-history type, and a `gcdfo:SER` concept must carry no `exactMatch` or
  `closeMatch` to `smn:SockeyeRiverTypeLifeHistory`.
- 2026-08-25 — **The sea-type "homograph" in the 2026-08-17 draft was
  backwards.** Gilbert 1913 coined "sea type" **in his Sockeye section**
  (p. 8), applied it across five species, and his chinook section (p. 13)
  defines its types *by reference to sockeye*; his contrasting term is "stream
  type", and "lake type"/"river type" appear zero times. It was **chinook**
  that renamed — Healey 1991 p. 314 designates it *"ocean-type" ("sea-type" in
  Gilbert 1913)*. So the sockeye sense is the original and continuous one and
  there is no homograph on that string. **The genuinely ambiguous label is
  "ocean-type"**: DFO Res. Doc. 2017/074 p. 3 declares *"River-type is
  synonymous with ocean-type"* (broad) while Res. Doc. 2023/003 p. 5 opposes
  the two (narrow). Both current. Carried as an `skos:altLabel` flagged
  ambiguous, with the real discriminator — freshwater age zero, no freshwater
  annulus — in the `skos:definition` instead.
- 2026-08-25 — **WoRMS content-negotiates to RDF where NCBI did not.**
  `https://www.marinespecies.org/aphia.php?p=taxdetails&id=254569` under
  `Accept: application/rdf+xml` redirects to `authority/metadata.php?lsid=…`
  and returns `application/rdf+xml` describing the LSID with Darwin Core terms;
  AphiaID 254569 is `status: accepted`. This is the check that admits the one
  `rdfs:seeAlso` in the proposal, and the contrast with the NCBI OBO PURL
  (HTML under every RDF `Accept`, verified 2026-08-17) is why the earlier ones
  were removed. Re-running it is what would retire the link.
- 2026-08-14 — Release 0.0.3 cut: first release carrying the alignment-pass
  state (imported W3C SOSA-PROV alignment, CONVENTIONS 5b + CI gates,
  methods-as-SKOS in smn:MethodScheme, smn:StatisticalModifierScheme,
  EscapementEstimate rename, step-3 boundary updates). PSC anchoring (S9
  step 4) pins against this release.
- 2026-08-21 — Reproducibility fix split out of PR 27 (found and fixed
  2026-08-17 on branch `feat/spsr-shared-life-history-schemes` while proposing
  the SPSR-derived terms; landed separately because the term proposal is
  contested and this half is not): the generated root flat TTL was
  **hash-order dependent**. The merged graph carried no prefix bindings, so
  rdflib invented `ns1:`/`ns2:`/... for predicate namespaces in
  store-iteration order; one such namespace was stable by luck, two were not.
  Eight generator runs on `main` gave one hash; eight on the branch gave four.
  `make verify-flat-ttl` would have flaked in CI with no source change behind
  it. Fixed by binding the prefixes the modules declare; see the builds card.
  The artifact now reads `smn:Term` instead of `<https://w3id.org/smn/Term>`,
  which is a large one-time diff in `salmon-domain-ontology.ttl` and
  `docs/smn.ttl` with no semantic content.
