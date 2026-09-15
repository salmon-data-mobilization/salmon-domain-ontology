# B-143 — The smn build does not check that an asserted superclass IRI is declared or vendored

Queue item: `metasalmon/queue/items/B-143.yaml` (P3, defect, repo
`salmon-domain-ontology`). Session key `fleet-2026-09-14-B-143`, agent token
`a-5204003c5ea6830d`, branched from `d45f8f7`.

## What I changed and where

| File | Change |
|---|---|
| `scripts/verify_superclass_declarations.py` | **New.** The gate, its two-direction fixture, and the staged baseline. |
| `Makefile` | Two targets: `verify-superclass-declarations` (the real gate, **not** in `test`) and `verify-superclass-declarations-staged` (in `test`). Switch-on condition in a comment above them. |
| `CONVENTIONS.md` | New section 5b rule 7: an asserted superclass names something. States the definition of "declared" and why the reasoner is not this check. |
| `docs/tech-debt.md` | Active entry with the full nine-IRI table, lines, subjects, and the two remedies. |
| `docs/entrypoints.md` | Both targets registered in Build and Test. |
| `knowledge/data/builds-and-import-graph.md` | New section "What the reasoner gate does not cover", verified at `d45f8f7`. |
| `knowledge/log.md` | Dated bundle entry. |

No `.ttl` file was touched, so the generated publication artifacts cannot
drift and `verify-generated-artifacts` needs no rerun.

## The definition the check turns on

An IRI is **declared** when some file in `ontology/modules/` or
`ontology/imports/` carries `rdf:type owl:Class`, `rdf:type rdfs:Class`, or
`rdf:type owl:DeprecatedClass` for it. An IRI appearing only as the *object* of
an `rdfs:subClassOf` is **not** declared by that appearance — that exclusion is
the whole content of the check, and the fixture asserts it in both directions.
`rdfs:Class` is accepted because the vendored SOSA snapshot uses it alongside
`owl:Class` (`sosa:ObservableProperty a rdfs:Class, owl:Class`).

Module/import boundary, since getting it wrong changes the answer: **modules**
are `ontology/modules/*.ttl`, which includes `alignment-main`,
`alignment-research` and `alignment-upper` and the generated bridge modules 08
and 09; **vendored imports** are `ontology/imports/*.ttl`, which is exactly
`prov-o.ttl`, `sosa-prov.ttl` and `sosa.ttl`. `ontology/views/` is excluded from
both: no build imports it, so a declaration there reaches nothing.

Node kinds are handled explicitly rather than by a `URIRef` test alone:
`BNode` objects (restrictions, intersections, `rdf:List` nodes) name no IRI and
are skipped **and counted in the summary line** so the skip is visible; a
`Literal` in superclass position is malformed and is its own failure class.

## THE OFFENDING LIST — complete, at `d45f8f7`, 2026-09-15

`make verify-superclass-declarations` reports **nine** IRIs, not one. 63 named
`rdfs:subClassOf` objects across 12 modules (plus 9 anonymous expressions
skipped), 35 distinct named superclass IRIs, resolved against 109 declarations.

**Shape A — wrong term (namespace IS vendored, IRI absent from it): 1**

1. `http://www.w3.org/ns/sosa/Property`
   - `ontology/modules/02-observation-measurement.ttl:28` — `smn:Characteristic`
   - `ontology/imports/sosa.ttl` is vendored and does **not** contain this IRI.
     SOSA publishes `sosa:ObservableProperty`, which that file declares. This is
     hub item **B-107**, already ruled, held behind smn PR **#27**. Not resolved
     here, by instruction and by scope.

**Shape B — namespace not vendored at all, and no declaration stub: 8**

2. `http://purl.obolibrary.org/obo/BFO_0000015`
   - `02-observation-measurement.ttl:216` — `smn:Escapement`
   - `03-assessment-benchmarks.ttl:53` — `smn:StockAssessment`
3. `http://purl.obolibrary.org/obo/IAO_0000030`
   - `01-entity-systematics.ttl:69` — `smn:ReportingOrManagementStratum`
   - `03-assessment-benchmarks.ttl:65,82` — `smn:MetricBenchmark`, `smn:ReferencePoint`
   - `05-provenance-quality.ttl:13,19` — `smn:DataQualityAssessment`, `smn:MethodDocumentation`
4. `http://purl.obolibrary.org/obo/IAO_0000109`
   - `02-observation-measurement.ttl:241` — `smn:EscapementEstimate`
   - `03-assessment-benchmarks.ttl:18,45` — `smn:ObservedRateOrAbundance`, `smn:TargetOrLimitRateOrAbundance`
5. `http://purl.obolibrary.org/obo/NCBITaxon_8015`
   - `02-observation-measurement.ttl:202` — `obo:NCBITaxon_8018` (the MIREOT mirror)
6. `http://purl.obolibrary.org/obo/NCBITaxon_8018`
   - `02-observation-measurement.ttl:206` — `smn:NCBITaxon_8018`
7. `http://rs.tdwg.org/dwc/terms/Event`
   - `02-observation-measurement.ttl:224` — `smn:SurveyEvent`
8. `http://rs.tdwg.org/dwc/terms/Organism`
   - `01-entity-systematics.ttl:86,94` — `smn:Deme`, `smn:Population`
9. `http://www.opengis.net/ont/geosparql#Feature`
   - `01-entity-systematics.ttl:59` — `smn:GeographicFeature`

**Vendoring omission or typo?** Measured, not guessed: I counted the declared
IRIs this repository holds in each offending namespace.

| Namespace | Declared IRIs here | Reading |
|---|---|---|
| `http://www.w3.org/ns/sosa/` | **13**, including `sosa:ObservableProperty` | vendored; `sosa:Property` is a **wrong term** with a declared near-neighbour |
| `http://purl.obolibrary.org/obo/` | **0** | nothing vendored |
| `http://rs.tdwg.org/dwc/terms/` | **0** | nothing vendored |
| `http://www.opengis.net/ont/geosparql#` | **0** | nothing vendored |

A typo needs a correct neighbour to be a typo *of*, and in three of the four
namespaces there is no declared neighbour at all — nothing is vendored, so
every IRI in them is equally unresolvable. So the eight are **vendoring
omissions**, not typos: more precisely, a decision to reference upstream
without vendoring it, never written down and never checked. `sosa:Property` is
the only wrong term, and the only one vendoring would not fix.

Two IRIs I did check against their source rather than assume, because the
modules make a claim about them: the MIREOT mirror comment at
`02-observation-measurement.ttl:200-201` says `NCBITaxon_8018` is
*Oncorhynchus keta* under `NCBITaxon_8015` *Salmonidae*. EBI OLS4 returns
exactly those two labels for those two IRIs. The comment is correct; no finding.

**So: the list is not "empty except for `sosa:Property`".** Landing B-107 will
not by itself make the gate green; eight more decisions stand between here and
switch-on. That answers the question the item said nobody currently knows.

### Not in scope, but found by the same scan (six more, informational)

Undeclared IRIs in `rdfs:domain`/`rdfs:range` position, which the gate does not
cover because B-143 is scoped to superclasses:

- `http://www.w3.org/ns/sosa/Property` — `02-observation-measurement.ttl:282`,
  `smn:characteristicFor rdfs:domain`. **The second half of the B-107 defect**,
  and B-107's own description names it, so it is already accounted for there.
- `http://purl.obolibrary.org/obo/NCBITaxon_8015` — `02-…:259`, `smn:observedTaxonFamily rdfs:range`
- `http://purl.obolibrary.org/obo/NCBITaxon_8018` — `02-…:265`, `smn:observedTaxonSpecies rdfs:range`
- `http://purl.obolibrary.org/obo/IAO_0000104` — `alignment-research.ttl`, `smn:usesObservationProcedure rdfs:range`
- `http://rs.tdwg.org/dwc/terms/MaterialEntity` — `alignment-research.ttl`, `smn:isSampleOfStratum rdfs:domain`
- `http://www.w3.org/2001/XMLSchema#gYear` — `02-…`, three `rdfs:range`s. **Not a
  defect**: a datatype, correctly used, and it is why a widened check must
  distinguish class position from datatype position rather than reusing this one.

One more, same family: `geosparql:Feature` also appears as an
`owl:someValuesFrom` filler inside a restriction at
`02-observation-measurement.ttl:183`. Restriction fillers are out of scope here
for the same reason.

## Commands run, and their results

### Direction 1 — a module asserting an undeclared foreign superclass turns the gate RED

Appended to `ontology/modules/04-management-governance.ttl` (reverted after;
the file is byte-identical to `HEAD`):

```turtle
smn:DemonstrationBrokenTerm a owl:Class ;
  rdfs:subClassOf <http://example.invalid/nothing-declares-this/Undeclared> ;
  rdfs:isDefinedBy <https://w3id.org/smn> .
```

```
$ make verify-superclass-declarations-staged
undeclared superclass IRI http://example.invalid/nothing-declares-this/Undeclared
      ontology/modules/04-management-governance.ttl:33 — asserted on https://w3id.org/smn/DemonstrationBrokenTerm
      nothing in ontology/modules/ or ontology/imports/ declares it as a class
make: *** [Makefile:159: verify-superclass-declarations-staged] Error 1     # exit 2

$ make test                       # the exact bundle CI runs
... every other check passes ...
Mapping policy verified: ...
Method shapes verified: ...
undeclared superclass IRI http://example.invalid/nothing-declares-this/Undeclared
make: *** [Makefile:159: verify-superclass-declarations-staged] Error 1     # exit 2
```

Note it fails in **staged** mode. The staged state does not stop new breakage;
it only silences the nine already recorded.

### The same fixture, against the reasoner — GREEN

This is the item's central claim, demonstrated rather than argued. With the
broken module still in place:

```
$ make install-robot && make verify-reasoner
Running ELK reasoner over the modular build (catalog-resolved imports)...
Reasoner gate passed: consistent, no unsatisfiable classes.              # exit 0
```

ELK reads an un-axiomatised IRI as a class about which nothing is known, so
nothing is entailed and nothing contradicts. A reasoner asks whether the axioms
contradict each other; this gate asks whether a name refers to anything, and no
amount of reasoning converts the second question into the first. This is why
`sosa:Property` survived 2026-08-10 → 2026-09-14 through every CI run.

### Direction 2 — removing it turns the gate GREEN

```
$ git diff --stat -- ontology/modules/04-management-governance.ttl   # empty: byte-identical to HEAD
$ make verify-superclass-declarations-staged
Superclass declarations verified over 12 modules against 109 declarations
(3 vendored imports; 9 anonymous superclass expressions skipped by design).
STAGED (hub item B-143): 9 known undeclared superclass IRIs are reported but
not failing. ...                                                          # exit 0

$ make test
Validation bundle completed.                                              # exit 0
```

### The committed fixture is load-bearing — RED demonstration of the guard itself

A guard that has not been shown to fail is a claim, not a guard. I injected the
exact mistake the check forbids (treat an IRI appearing only as the object of
`rdfs:subClassOf` as declared) and the in-script fixture caught it:

```
$ make verify-superclass-declarations-staged
The two-direction fixture failed. The gate is not working:
  fixture direction 1: the foreign undeclared superclass ... was NOT reported
  fixture (red): an IRI appearing only as the object of rdfs:subClassOf was
    treated as declared — that is the definition this check turns on
  fixture (green): ... same ...
  fixture (red): unexpected result set []
  fixture (green): unexpected result set []
make: *** Error 1                                                          # exit 2
```

Restored; back to exit 0.

### The staged state cannot quietly become permanent — RED demonstration

Simulating B-107 landing, by putting an already-declared IRI in the baseline:

```
$ make verify-superclass-declarations-staged
stale baseline entry http://www.w3.org/ns/sosa/ObservableProperty: it is
declared now, so delete its KNOWN_UNDECLARED entry in this file. When the
baseline is empty, delete it with --staged and switch the Makefile's test
target from verify-superclass-declarations-staged to
verify-superclass-declarations.
make: *** Error 1                                                          # exit 2
```

So the day B-107 lands, CI goes red until someone deletes that entry, and the
message they get names the switch-on condition.

### Final state

```
$ make test                                   # exit 0, green
$ make verify-superclass-declarations         # exit 1, 9 IRIs — the real gate, not in CI
$ git diff --check                            # clean
$ python3 -m py_compile scripts/verify_superclass_declarations.py   # clean
```

## What I did not do, and why

- **Did not resolve `sosa:Property`.** It is B-107's ruled change (Brett,
  2026-09-14), and B-107 is held behind smn PR #27, which edits the same module
  and regenerates the docs artifacts. Making it here would conflict.
- **Did not resolve the other eight.** Each needs a decision — vendor the
  namespace, or add a declaration stub — and B-143 is structural with no term
  ruling in it. Recorded, not fixed.
- **Did not wire the real gate into CI red.** Per the item: a check that
  arrives red teaches its first reader to weaken it.
- **Did not widen to `rdfs:domain`/`rdfs:range`, `rdfs:subPropertyOf`, or
  restriction fillers.** Out of B-143's scope; listed above as findings and
  below as a new-item candidate.
- **Could not run `psc-okf check knowledge --tier capture`.** No sibling
  `psc-data-systems` checkout exists on this machine (searched
  `/home/user`). The two bundle edits follow the existing card shape — a dated
  "verified against commit" line and a log entry — but the bundle is
  **unvalidated** and someone with that checkout should run it.
- **Did not run `make verify-generated-artifacts`.** It needs WIDOCO and
  rewrites `docs/`; no `.ttl` changed, so no drift is possible.

## Guards, suppressions and skips I added, with their retirement conditions

1. **The staged mode itself** (`--staged`, `KNOWN_UNDECLARED`, the
   `verify-superclass-declarations-staged` target). *Retires when:*
   `KNOWN_UNDECLARED` is empty — then delete it, `REASONS`, `--staged` and the
   staged target, and swap the `test` prerequisite to
   `verify-superclass-declarations`. Enforced rather than merely written down:
   staged mode fails on a stale baseline entry, so the swap cannot be skipped.
   Stated in the script docstring, the Makefile comment, CONVENTIONS 5b rule 7
   and `docs/tech-debt.md`.
2. **Each baseline entry**, via its `REASONS` key, printed on every staged run.
   `B-107` retires when B-107 lands; `not-vendored` retires when the
   vendor-or-stub decision is taken and the declaration lands.
3. **`BUILTIN_CLASSES`** (OWL/RDFS built-ins, which nothing here declares or
   should). *Retires when:* the declared set is seeded from vendored copies of
   the OWL and RDFS vocabularies, so they resolve like any other IRI. Exercised
   by the fixture (`ex:UnderThing rdfs:subClassOf owl:Thing` must not be
   reported), so it is not an untested allowlist.
4. **Skipping anonymous superclass expressions.** Not a suppression — they name
   no IRI — but it is counted in the summary line on every run so the skip is
   visible rather than silent, and the fixture pins the count at 2.
5. **The whole script.** *Retires when:* an upstream gate run identically by
   smn, gcdfo and the PSC vocabularies checks referential integrity of asserted
   axioms across all three, making this repo-local check redundant.

## Belongs to other items / new-item candidates

- **B-107** (`sosa:Property` → `sosa:ObservableProperty`) — the last baseline
  entry to clear, itself blocked on smn PR #27. Its `rdfs:domain` half at
  `02-observation-measurement.ttl:282` is already in its description.
- **New-item candidate: decide vendor-or-stub for the eight unvendored
  namespaces.** BFO, IAO, NCBITaxon, Darwin Core, GeoSPARQL. Evidence: the
  table in `docs/tech-debt.md` and `KNOWN_UNDECLARED`. This is the work that
  stands between B-107 landing and this gate switching on, and it is a
  modelling decision, not a mechanical one. Structural prerequisite for
  retiring the staged state.
- **New-item candidate: widen the check to `rdfs:domain`, `rdfs:range`,
  `rdfs:subPropertyOf` and restriction fillers.** Evidence: the six
  informational findings above, one of which (`xsd:gYear`) shows the widened
  check must distinguish class position from datatype position rather than
  reusing this one unchanged. `geosparql:Feature` at
  `02-observation-measurement.ttl:183` is the restriction-filler case.
- **New-item candidate: per-closure rather than union resolution.** This check
  asks whether an IRI is declared anywhere in modules + imports, which is the
  union B-143 names. It does not ask whether the declaration *reaches* the
  build that uses it — a declaration in module 09 does not reach the main
  build, which imports 01–07 plus `alignment-main` and `alignment-upper`. The
  stronger per-closure question is separable and currently unasked.
- **Documentation defect, unfiled:** `AGENTS.md` in this repo warns that
  `make verify-flat-ttl` "currently rewrites generated modules 08/09 in the
  working tree; run on a clean tree". `knowledge/data/builds-and-import-graph.md`
  records that this was fixed 2026-08-13 (step 1b — verification is read-only
  now), and `make test` left my tree clean across every run above. The
  `AGENTS.md` caution looks stale. Not touched: outside B-143.
