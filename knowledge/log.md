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
- 2026-09-15 — Referential-integrity gate for asserted superclasses (hub item
  B-143): `scripts/verify_superclass_declarations.py` plus CONVENTIONS 5b
  rule 7. The finding worth carrying forward is negative and is now on the
  builds card: **the ELK reasoner gate cannot see this defect and never
  could**, because an un-axiomatised IRI is a class about which nothing is
  known, so the closure stays consistent — demonstrated by running
  `make verify-reasoner` against a deliberately broken module and watching it
  pass green. The first run found **9 undeclared superclass IRIs**, not the 1
  the item was cut from: `sosa:Property` (a wrong term in a namespace that is
  vendored — item B-107) and eight in namespaces never vendored at all. Landed
  staged rather than enforcing, because a check that arrives red teaches its
  first reader to weaken it; the two-direction fixture and the
  new-violation half are enforced from day one, and the staged half fails on a
  stale baseline entry so the switch-on cannot be quietly skipped.
