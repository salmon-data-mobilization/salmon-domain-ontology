# Namespace decision for Salmon Domain Ontology

Status: **proposed for immediate ratification**
Owner: `@Br-Johnson`
Date: 2026-03-05

## Why this is needed now

Current state is not safe for broad downstream migration:

- `https://w3id.org/salmon/` resolves to an unrelated external project (name collision).
- `https://w3id.org/salmon-domain-ontology` is not registered yet (404).
- Internal ontology files currently use `http://w3id.org/salmon/` for `salmon:` terms, which cannot be guaranteed under our control.

Until this is fixed, app-level namespace rewiring should remain paused.

## Canonical namespace decision (proposed)

Use one persistent base under our own path:

- **Term namespace (`salmon:`):** `https://w3id.org/salmon-domain-ontology/`
- **Ontology IRI (main build):** `https://w3id.org/salmon-domain-ontology`
- **Module IRIs:** `https://w3id.org/salmon-domain-ontology/modules/<module-name>`
- **Research build IRI:** `https://w3id.org/salmon-domain-ontology/research`
- **Case-study build IRI:** `https://w3id.org/salmon-domain-ontology/rda-case-study`
- **Profile namespaces:**
  - `https://w3id.org/salmon-domain-ontology/profile/hakai/`
  - `https://w3id.org/salmon-domain-ontology/profile/neville/`
  - `https://w3id.org/salmon-domain-ontology/profile/rda-case-study/`

## Transition mapping (from current draft IRIs)

| Current pattern | Canonical pattern |
| --- | --- |
| `http://w3id.org/salmon/<x>` | `https://w3id.org/salmon-domain-ontology/<x>` |
| `http://w3id.org/salmon-domain-ontology...` | `https://w3id.org/salmon-domain-ontology...` |
| `https://w3id.org/salmon/profile/<p>/...` | `https://w3id.org/salmon-domain-ontology/profile/<p>/...` |

## Freeze rule

Do **not** perform broad dependent-app namespace cutover until both are true:

1. W3ID redirect registration is merged and live.
2. Ontology IRIs in this repo are rewritten to the canonical namespace above.

## Acceptance checklist

- [ ] W3ID request submitted with `.htaccess` payload
- [ ] W3ID redirect rules merged and resolvable
- [ ] Ontology files updated to canonical namespace
- [ ] Migration map (`docs/migrations/gcdfo-to-salmon-wave1.csv`) updated to canonical `new_iri` values
- [ ] README + conventions updated to the same canonical namespace
- [ ] One tagged release from `main` after namespace rewrite

## Notes on root TTL duplication concern

`/salmon-domain-ontology.ttl` at repo root is a compatibility wrapper and intentionally imports the modular source of truth at `ontology/salmon-domain-ontology.ttl`.
That is expected and can remain as-is.