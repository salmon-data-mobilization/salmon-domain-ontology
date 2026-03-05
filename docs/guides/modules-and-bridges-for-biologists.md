# Modules and bridge profiles (for biologists new to ontologies)

This page is a plain-language guide.

If you work with salmon datasets and you are **not** an ontology specialist, start here.

---

## The big idea in one minute

Think of this ontology stack like field work across many organizations:

1. **Shared domain ontology (`salmon:`)** = the common language everyone agrees on.
2. **Organization/program ontology (your local profile)** = your team’s local terms, methods, and policy vocabulary.
3. **Bridge profile** = the translation layer that connects your local terms to shared terms.

So we do **not** force every team to use identical words internally.
We keep local meaning, then map it cleanly.

---

## Why we use modules

Instead of one giant ontology file, this repo is split into focused modules.

Why that helps:

- Easier to read and review
- Easier to update one area without breaking everything
- Easier to reuse only what a project needs

Current module pattern (plain language):

- `01` entities and biological groupings (stock, population, deme)
- `02` observations and measurements
- `03` assessments and benchmarks
- `04` management/governance abstractions
- `05` provenance and quality
- `06` interoperability alignments (how this talks to other standards)
- `07` shared controlled vocabularies
- `08/09` profile bridge examples (case-study mappings; not auto-promoted into shared core)

See: `ontology/modules/README.md`

---

## What is a bridge profile?

A **bridge profile** is a mapping file that says:

- “Our local concept `X` is the same as / close to / related to shared concept `Y`.”

It is the safest way to integrate new datasets because it avoids two bad outcomes:

1. forcing local meaning into shared terms too early
2. creating duplicate shared terms for every program nuance

Bridge profiles are where we record mapping confidence and provenance.

---

## Mapping a new dataset: practical workflow

Use this checklist when onboarding a new dataset.

### Step 1 — Inventory the dataset terms

Make a simple table from columns/variables/method fields:

- local term label
- local definition (in plain English)
- units
- where it came from (SOP, manual, codebook)

### Step 2 — Try to match to existing shared terms

For each local term, ask:

- Is there already a `salmon:` term with the same meaning?

If yes, reuse it.

### Step 3 — If no direct match, keep local term local

Create the term in your organization/program namespace (profile ontology).

Do **not** immediately mint a new shared term unless reuse is clearly cross-organization.

### Step 4 — Add bridge mappings

In a bridge file, map local term -> shared term using the right strength:

- strict equivalence/subclass when truly exact and stable
- `skos:exactMatch` when conceptually equivalent
- `skos:closeMatch`/related mappings when similar but not fully identical

### Step 5 — Record provenance

For each mapping, include source docs and rationale.

Future you (or another team) must be able to answer: “Why did we map this this way?”

### Step 6 — Test with real rows

Run representative records through the mapping and check:

- no lost meaning
- no impossible unit/value conversions
- no accidental collapse of distinct local concepts

### Step 7 — Promote only when justified

Promote a local term into shared `salmon:` only if:

- more than one organization needs it
- semantics are stable across contexts
- promotion clearly improves interoperability

If not, keep it profile-scoped and bridged.

---

## Creating an organization/program ontology (simple pattern)

1. Pick your namespace (for example, `myorg:`).
2. Define your local classes/concepts there.
3. Keep policy/program-specific statuses and method bins local.
4. Add a separate bridge module that links `myorg:` to `salmon:`.
5. Keep bridge mappings conservative until validated with data.

---

## Minimal bridge example

```turtle
@prefix salmon: <https://w3id.org/salmon-domain-ontology/> .
@prefix myorg:  <https://example.org/myorg/salmon/> .
@prefix skos:   <http://www.w3.org/2004/02/skos/core#> .
@prefix prov:   <http://www.w3.org/ns/prov#> .

myorg:SpawnerSurveyEvent
  skos:exactMatch salmon:SurveyEvent ;
  prov:wasDerivedFrom <https://example.org/myorg/sop/survey-protocol-v3> .

myorg:RapidStatusConfidenceBand
  skos:closeMatch salmon:MetricBenchmark .
```

Interpretation:

- first mapping is strong and likely safe
- second mapping is advisory and needs review before canonical production transforms

---

## How to choose mapping strength (quick rule)

- **Exact and stable:** use strong mapping
- **Mostly same but context differs:** use close/related mapping
- **Unsure:** keep local, map conservatively, document uncertainty

When in doubt, choose the less aggressive mapping.

---

## Common mistakes to avoid

- Creating new shared terms too early
- Treating every local code as a shared ontology concept
- Using strong equivalence for “kind of similar” terms
- Skipping provenance notes
- Mixing policy-specific terms into shared core

---

## Definition of done for a new dataset mapping

A mapping is "done" when:

- local terms are inventoried
- shared re-use decisions are documented
- bridge mappings exist with rationale
- sample data passes smoke checks
- unresolved high-risk mappings are explicitly marked for review

---

## Where to go next

- Modeling rules: `CONVENTIONS.md`
- Module map: `ontology/modules/README.md`
- Migration and cutover notes: `docs/migrations/README.md`
- Namespace/publishing status: `docs/publishing/namespace-decision.md`
