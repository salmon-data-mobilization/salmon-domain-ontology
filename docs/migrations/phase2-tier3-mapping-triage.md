# Phase 2 Tier-3 mapping triage register

Status: **closed for phase 2; remains the default policy baseline until an explicit promotion decision is recorded**

This register records the explicit dispositions used for phase-2 closeout for
Tier-3 mappings (`skos:closeMatch`, `skos:relatedMatch`, `skos:broadMatch`,
`skos:narrowMatch`).

## Production policy baseline

- Tier-3 mappings are **advisory by default**.
- No Tier-3 mapping is auto-canonicalized into production transforms without explicit promotion.
- Promotion requires consumer sign-off and traceable evidence in the issue #3 closure trail (or its future equivalent).

## Triage checklist

| Mapping cohort | Current disposition | Owner | Evidence | Status |
| --- | --- | --- | --- | --- |
| `ontology/modules/alignment-main.ttl` shared-to-SOSA/I-ADOPT/DWC `skos:closeMatch` bridges | Keep Tier-3 advisory only; permitted for discovery/query hints, not canonical transform rules | Ontology maintainer (`@Br-Johnson`) | `alignment-main.ttl` + `phase2-boundary-rules.md` Tier policy | Triaged |
| `ontology/modules/08-rda-case-study-profile-bridges.ttl` Hakai `skos:closeMatch` links | Keep advisory for crosswalk guidance; no auto-promotion of Hakai terms into shared core | Ontology maintainer + SPSR smoke-run owner | Module 08 bridge mappings + SPSR smoke-run evidence (issue #3) | Triaged |
| `ontology/modules/09-rda-neville-decomposition-profile-bridges.ttl` Neville `skos:closeMatch` links | Keep advisory; candidate promotion only for explicitly validated report paths | Ontology maintainer + SPSR smoke-run owner | Module 09 bridge mappings + SPSR smoke-run evidence (issue #3) | Triaged |
| `ontology/modules/09-rda-neville-decomposition-profile-bridges.ttl` Neville `skos:relatedMatch` links | Keep strictly non-canonical; semantic context only | Ontology maintainer | Module 09 related-match links | Triaged |

## Promotion gate (required before any Tier-3 uplift)

A Tier-3 mapping may be promoted only when all conditions are met:

1. SPSR downstream evidence and/or the DFO provider-verification contract demonstrates stable behavior for the exact mapping in the active consumer path.
2. Mapping decision is recorded in issue #3 (or its successor) with owner and evidence links.
3. Mapping is reclassified into Tier-1/2 equivalent policy in docs + module update.
4. Reviewer sign-off confirms no adverse semantic collapse.

## Closeout follow-up state

- [x] DFO no-runtime provider-verification contract recorded for phase-2 closure.
- [x] SPSR smoke evidence recorded proving bridge mappings did not require unsafe auto-canonicalization in the operative consumer lane.
- [ ] Revisit triage entries after the first post-phase-2 downstream production cycle or any explicit Tier-3 promotion request.
