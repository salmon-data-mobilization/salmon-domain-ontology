# Conventions

This document defines how we model shared salmon semantics versus agency/profile-specific vocabularies.

## 1) Goal

Build a **shared interoperability layer** that supports precise cross-agency integration while still allowing each organization to maintain local policy/program vocabularies.

Conservative default: **if unsure, keep terms in a profile ontology first**. Promote to shared only when reuse is clear.

## 2) Layered model (authoritative)

### Layer A — Shared OWL semantic core (`salmon:`)

Use for cross-agency concepts with stable semantics and reusable logical structure.

Examples:
- biological entities (`Population`, `Deme`)
- reusable monitoring/measurement semantics (`SurveyEvent`, `EscapementMeasurement`)
- reusable quantitative semantics (`ExploitationRate`)

### Layer B — Shared SKOS interoperability layer (`salmon:`)

A **small curated SKOS layer** for truly cross-agency controlled vocabularies.

Use for:
- shared codelists that are expected to be reused by multiple organizations
- concept labels/definitions that support operational data harmonization

### Layer C — Agency/profile ontologies (organization namespaces)

Use for policy/program-specific SKOS schemes and agency-specific interpretation layers.

Examples:
- named policy schemes and statuses that are not broadly governed across agencies
- organization-specific method taxonomies and quality bins

### Layer D — Mapping/bridge artifacts

Machine-readable mappings that connect profile terms to shared domain terms.

Use these to support ingestion, search, and migration without collapsing distinct semantics.

## 3) OWL vs SKOS modeling rules

### Use OWL classes/properties when:
1. You need formal logical structure (subclass/property reasoning, restrictions, constraints).
2. The term represents a durable domain concept rather than a codelist entry.
3. Integration pipelines need deterministic canonicalization.

### Use SKOS concepts/schemes when:
1. You are modeling code values, method bins, status categories, or policy vocabulary.
2. Label hierarchy and human interpretation are primary.
3. Local governance of terms is expected to evolve quickly.

### Dual representation rule

A concept may exist as both OWL and SKOS **only with separate IRIs** and explicit mapping.

## 4) IRI strategy

1. Shared terms use `salmon:` IRIs.
2. Profile-specific terms use the profile namespace.
3. Do not overload a single IRI with incompatible roles.
4. OWL class IRIs and SKOS concept IRIs must remain distinct where both are needed.

## 5) Mapping strength policy

Treat mapping predicates as different evidence strengths:

### Tier 1 (strict / automation-safe)
- `owl:equivalentClass`
- `owl:equivalentProperty`
- `owl:sameAs`
- `rdfs:subClassOf`
- `rdfs:subPropertyOf`

### Tier 2 (strong lexical/conceptual)
- `skos:exactMatch`

### Tier 3 (advisory / candidate only)
- `skos:closeMatch`
- `skos:broadMatch`
- `skos:narrowMatch`
- `skos:relatedMatch`

Operational rule: Tier 3 links should not auto-canonicalize data into the production graph without review/promotion.

## 6) Profile-to-domain bridge pattern

When a profile concept corresponds to shared domain semantics:

1. Keep the profile concept in profile namespace.
2. Link it to shared domain semantics using mapping predicates.
3. Prefer `skos:exactMatch` only when semantics are truly equivalent.
4. Use `skos:closeMatch`/`broadMatch` as provisional links.
5. Attach provenance and reviewer metadata for each bridge.

Example (conceptual):
- `profile:SomeMethodConcept skos:closeMatch salmon:EscapementMeasurement .`
- `profile:SomeMethodConcept prov:wasDerivedFrom <source-doc> .`

## 7) LLM-assisted integration policy

LLMs may propose mappings, but production integration must follow approval gates.

### Required output from mapping assistants
1. proposed shared target
2. mapping predicate suggestion
3. confidence score
4. rationale text
5. recommended action (`accept`, `review`, `defer`, `new-term-request`)

### Ingestion gate

Only approved mappings (Tier 1/2 or explicitly promoted Tier 3) materialize into canonical graph integration transforms.

## 8) Shared-term admission policy

Expert judgment is allowed, but conservative.

Promotion to shared should include:
1. expected multi-agency reuse
2. semantic stability across contexts
3. non-reliance on agency-specific policy interpretation
4. practical integration benefit

If any criterion is weak, keep term in profile and map to shared anchors.

## 9) Versioning and transition

Current posture:
1. migration mode can use direct replacement for alpha transitions when risk is low
2. publish machine-readable old→new mapping for each migration wave
3. maintain explicit migration notes per release
4. endpoint cutover timing may be deferred until profile/shared boundary stabilizes

## 10) Current boundary decisions (working set)

### Keep in shared domain (current)
1. `Stock`
2. `IndicatorRiver`
3. core biological and measurement semantics that are policy-neutral

### Keep in profile layer (current)
1. WSP-specific status and confidence schemes/concepts
2. Enumeration method scheme (organization/program-specific)
3. Estimate method scheme (organization/program-specific)
4. Benchmark level scheme (organization/program-specific)
5. Policy framework scheme terms that are organization-specific
6. Estimate type and downgrade-criteria schemes/concepts

These decisions are revisited only with explicit governance review and evidence.
