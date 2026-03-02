# Phase 2 Tier-3 mapping triage register

This register records explicit dispositions for Tier-3 mappings (`skos:closeMatch`, `skos:relatedMatch`, `skos:broadMatch`, `skos:narrowMatch`) before publish-ready cutover.

## Production policy baseline

- Tier-3 mappings are **advisory by default**.
- No Tier-3 mapping is auto-canonicalized into production transforms without explicit promotion.
- Promotion requires consumer sign-off and traceable evidence in issue #3.

## Triage checklist

| Mapping cohort | Current disposition | Owner | Evidence | Status |
| --- | --- | --- | --- | --- |
| `ontology/modules/alignment-main.ttl` shared-to-SOSA/I-ADOPT/DWC `skos:closeMatch` bridges | Keep Tier-3 advisory only; permitted for discovery/query hints, not canonical transform rules | Ontology maintainer (`@Br-Johnson`) | `alignment-main.ttl` + `phase2-boundary-rules.md` Tier policy | Triaged |
| `ontology/modules/08-rda-case-study-profile-bridges.ttl` Hakai `skos:closeMatch` links | Keep advisory for crosswalk guidance; no auto-promotion of Hakai terms into shared core | Ontology maintainer + SPSR smoke-run owner | Module 08 bridge mappings + SPSR smoke-run evidence (issue #3) | Triaged |
| `ontology/modules/09-rda-neville-decomposition-profile-bridges.ttl` Neville `skos:closeMatch` links | Keep advisory; candidate promotion only for explicitly validated report paths | Ontology maintainer + SPSR smoke-run owner | Module 09 bridge mappings + SPSR smoke-run evidence (issue #3) | Triaged |
| `ontology/modules/09-rda-neville-decomposition-profile-bridges.ttl` Neville `skos:relatedMatch` links | Keep strictly non-canonical; semantic context only | Ontology maintainer | Module 09 related-match links | Triaged |

## Promotion gate (required before any Tier-3 uplift)

A Tier-3 mapping may be promoted only when all conditions are met:

1. DFO and/or SPSR smoke run demonstrates stable downstream behavior for the exact mapping.
2. Mapping decision is recorded in issue #3 with owner and evidence links.
3. Mapping is reclassified into Tier-1/2 equivalent policy in docs + module update.
4. Reviewer sign-off confirms no adverse semantic collapse.

## Open follow-up tasks

- [ ] Attach DFO smoke-run evidence proving Tier-3 safety posture holds in DFO consumer path.
- [ ] Attach SPSR smoke-run evidence proving bridge mappings do not require unsafe auto-canonicalization.
- [ ] Revisit triage entries after first post-cutover production cycle.
