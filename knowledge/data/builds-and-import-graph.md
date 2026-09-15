---
type: InformationObject
title: Builds and import graph
description: What each build variant buys, the exact import graph including its cycle and the views' relative imports, where generated output mixes with source, the w3id dereference gaps, and why the reasoner gate cannot see an undeclared superclass IRI.
status: draft
tags: [builds, imports, w3id, tooling, ci-gates]
psc:
  id: smn:data:builds-and-import-graph
  contexts: [smn:context:ontology-alignment-pass-2026]
---

Verified 2026-08-12 against the working tree at commit `3995a17` (main).

## The four build artifacts

| Artifact | Nature | Imports |
|---|---|---|
| `ontology/salmon-domain-ontology.ttl` | hand-authored MAIN composition root (21 lines) | modules 01–07 + `alignment-main`, by **absolute w3id IRIs** |
| `ontology/salmon-domain-ontology-research.ttl` | research root (9 lines) | `<https://w3id.org/smn>` + `alignment-research` |
| `ontology/salmon-domain-ontology-rda-case-study.ttl` | case-study root (10 lines) | `<https://w3id.org/smn>` + generated bridge modules 08/09 |
| `salmon-domain-ontology.ttl` (repo root) | **generated** import-stripped flattening of MAIN (`scripts/build_flat_smn_ttl.py`), drift-guarded by `make verify-flat-ttl` + CI | none |

The root flat artifact shares a basename with the modular source — only a
header comment distinguishes them, which invites wrong-file edits.

**The flat artifact was not reproducible, and now is (2026-08-17).**
`build_flat_smn_ttl.py` merges the modules by copying triples only, so the
merged graph inherited none of their prefix bindings. rdflib's Turtle
serializer then invented `ns1:`, `ns2:`, ... for each namespace it met in
**predicate** position — and only there, which is why subjects and objects
were written as full IRIs — numbering them in store-iteration order, which is
hash-randomized per process. With exactly one such namespace
(`http://purl.obolibrary.org/obo/`, reached through `iao:` annotation
predicates) the numbering was stable by luck, so `make verify-flat-ttl` passed
on every commit up to 0.0.3. Measured 2026-08-17: eight runs of the generator
on `main`'s content produced one hash; eight runs on a branch whose module 07
had gained an `smn:` and a `dwc:` predicate produced **four distinct hashes**.
The gate would have flaked in CI with no source change behind it.

Fixed by binding the prefixes the modules already declare
(`apply_stable_prefixes`), so nothing is auto-numbered and the artifact reads
`smn:hasCycleLine` rather than `ns3:hasCycleLine`. Anything the sources do not
name falls back to rdflib's numbering, applied in sorted IRI order so the
fallback is deterministic too. Consequence: the flat TTL and the ROBOT-derived
`docs/smn.ttl` rewrite every `<https://w3id.org/smn/Term>` as `smn:Term` and
`ns1:` as `obo:` — one large, semantically empty diff, taken once. Retire the
function only if the merge itself starts carrying the source bindings.

## Import-graph facts that surprise people

- **Cycle:** `<https://w3id.org/smn>` imports `alignment-main`
  (`ontology/salmon-domain-ontology.ttl:21`) and `alignment-main.ttl:14`
  imports `<https://w3id.org/smn>` back. Legal OWL, but the module cannot be
  loaded standalone without pulling the whole ontology.
- **Views are unreachable from every build**, the flat artifact, and both
  sibling repos; `views/README.md` states this is deliberate. The composite
  view `ontology/views/salmon-data-metamodel.ttl:7-14` is the **only** file
  using relative (filename) `owl:imports` — resolvable solely from a local
  checkout with siblings intact.
- ~~No catalog file exists~~ **Fixed 2026-08-13:** `ontology/catalog-v001.xml`
  and `ontology/views/catalog-v001.xml` now map every module, view, and the
  vendored W3C SOSA–PROV snapshot (`ontology/imports/sosa-prov.ttl`) to local
  files; the composite view imports by ontology IRI. The main build now also
  imports `modules/alignment-upper` (which imports the W3C alignment — the
  first remote import in the graph; offline loading resolves it via the
  catalog).

## Generated vs hand-authored mixing

- Bridge modules `08`/`09` under `ontology/modules/` are **generated**
  (concatenated from `ontology/case-studies/` fragments) beside
  hand-authored modules. ~~Drift-gate gap and verify-mutates-source~~
  **Fixed 2026-08-13 (step 1b):** `make test` runs
  `build_rda_case_study_modules.py --check` (compose in memory, diff, fail
  on drift) — verification is read-only and hand-edits to 08/09 now fail CI.
- ~~Phantom "auto-generated" markers~~ **Fixed 2026-08-13:** the markers
  (which never had a generator — authored in `2549f74`) are replaced with
  honest hand-authored markers in the fragments.
- **CI gates since step 1b:** `verify_mapping_policy.py` (CONVENTIONS §5b:
  foreign-subject statements, tier-mixing per-file and across the spine,
  dual typing), `verify_method_shapes.py` (pyshacl behavioural fixture),
  and an ELK reasoner-gate job over the catalog-resolved closure.
- **`verify_superclass_declarations.py` (added 2026-09-15, staged).**
  See "What the reasoner gate does not cover" below for why it exists.

## What the reasoner gate does not cover

Verified 2026-09-15 against the working tree at commit `d45f8f7` (main).

**A superclass IRI that nothing declares does not make the closure
inconsistent, so the reasoner gate passes over it.** ELK reads an
un-axiomatised IRI as a class about which nothing is known: nothing is
entailed, nothing contradicts, no class is unsatisfiable. Measured by adding
`smn:X rdfs:subClassOf <http://example.invalid/…/Undeclared>` to module 04 and
running `make verify-reasoner` — "Reasoner gate passed: consistent, no
unsatisfiable classes", exit 0. That is how `sosa:Property` sat under
`smn:Characteristic` from 2026-08-10 to 2026-09-14, through every CI run, with
the whole characteristic hierarchy hanging off an IRI SOSA does not publish.

The lesson generalises past this one check: **a consistency gate answers
"do these axioms contradict each other", never "does this name refer to
anything"**, and the second question needs its own gate. Before reaching for
the reasoner to cover a referential-integrity defect, check which of the two
questions you are actually asking.

`scripts/verify_superclass_declarations.py` asks the second one. Measured on
the same commit: **9 of the 35 distinct named superclass IRIs asserted in
`ontology/modules/` are undeclared** — 63 named `rdfs:subClassOf` objects
across 12 modules, plus 9 anonymous class expressions the check skips by
design, resolved against 109 class declarations in the modules and the 3
vendored imports. One of the nine (`sosa:Property`) is a wrong term in a
namespace that *is* vendored; the other eight are namespaces never vendored at
all (`obo:`/BFO/IAO/NCBITaxon, `dwc:`, `geosparql:`). The full table, with
lines and subjects, is in `docs/tech-debt.md`. The check is staged rather than
enforcing until that list is empty; `sosa:Property` is hub item B-107, blocked
on smn PR 27.

## w3id dereference gaps (live-checked 2026-08-12)

- No rewrite rule matches `views/...` paths or the `smnv:` fragment
  namespace — view IRIs 404 (`docs/publishing/w3id-htaccess.example:66-84`
  mirrors the live rules).
- Module IRIs dereference to **mutable** `raw.githubusercontent.com`
  main-branch files, unlike the root/SemVer paths which hit the immutable
  Pages release surface.
- Profile **term** IRIs (e.g. `.../profile/hakai/...`) asserted in modules
  08/09 have no dereference route either.
