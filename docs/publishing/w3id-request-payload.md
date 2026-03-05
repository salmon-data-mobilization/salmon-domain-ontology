# W3ID request payload (ready to submit)

Status: draft-ready
Target registry: <https://github.com/perma-id/w3id.org>
Requested path: `salmon-domain-ontology`

## 1) Proposed PR contents in `perma-id/w3id.org`

Create folder:

- `salmon-domain-ontology/`

Create file:

- `salmon-domain-ontology/.htaccess`

Use this content:

```apache
Options +FollowSymLinks
RewriteEngine On

# Main ontology build
RewriteRule ^$ https://raw.githubusercontent.com/salmon-data-mobilization/salmon-domain-ontology/main/ontology/salmon-domain-ontology.ttl [R=302,L]
RewriteRule ^ontology/?$ https://raw.githubusercontent.com/salmon-data-mobilization/salmon-domain-ontology/main/ontology/salmon-domain-ontology.ttl [R=302,L]

# Optional build entrypoints
RewriteRule ^research/?$ https://raw.githubusercontent.com/salmon-data-mobilization/salmon-domain-ontology/main/ontology/salmon-domain-ontology-research.ttl [R=302,L]
RewriteRule ^rda-case-study/?$ https://raw.githubusercontent.com/salmon-data-mobilization/salmon-domain-ontology/main/ontology/salmon-domain-ontology-rda-case-study.ttl [R=302,L]

# Module IRIs
RewriteRule ^modules/([A-Za-z0-9._-]+)/?$ https://raw.githubusercontent.com/salmon-data-mobilization/salmon-domain-ontology/main/ontology/modules/$1.ttl [R=302,L]

# Profile bridge namespace roots
RewriteRule ^profile/hakai/?$ https://raw.githubusercontent.com/salmon-data-mobilization/salmon-domain-ontology/main/ontology/modules/08-rda-case-study-profile-bridges.ttl [R=302,L]
RewriteRule ^profile/neville/?$ https://raw.githubusercontent.com/salmon-data-mobilization/salmon-domain-ontology/main/ontology/modules/09-rda-neville-decomposition-profile-bridges.ttl [R=302,L]
RewriteRule ^profile/rda-case-study/?$ https://raw.githubusercontent.com/salmon-data-mobilization/salmon-domain-ontology/main/ontology/salmon-domain-ontology-rda-case-study.ttl [R=302,L]

# Any term IRI (e.g., /Stock) resolves to canonical ontology graph
RewriteRule ^[A-Za-z0-9._-]+/?$ https://raw.githubusercontent.com/salmon-data-mobilization/salmon-domain-ontology/main/ontology/salmon-domain-ontology.ttl [R=302,L]
```

## 2) Suggested PR title

`Add w3id redirects for salmon-domain-ontology`

## 3) Suggested PR body

```markdown
This PR registers persistent identifiers for the Salmon Domain Ontology.

Requested base:
- https://w3id.org/salmon-domain-ontology

Maintainer repository:
- https://github.com/salmon-data-mobilization/salmon-domain-ontology

Why:
- We need a persistent namespace under maintainers' control for ontology terms and module IRIs.
- Existing `w3id.org/salmon` path is controlled by a different project.

Redirect behavior:
- Base and `/ontology` resolve to the modular primary build.
- `/research` and `/rda-case-study` resolve to optional builds.
- `/modules/<name>` resolves to each module artifact.
- `/profile/*` paths resolve to profile bridge artifacts.
- term paths like `/Stock` resolve to the canonical ontology graph.

Initial redirects use `302` while finalization is underway.
```

## 4) Post-merge verification commands

```bash
curl -I https://w3id.org/salmon-domain-ontology
curl -I https://w3id.org/salmon-domain-ontology/Stock
curl -I https://w3id.org/salmon-domain-ontology/modules/01-entity-systematics
curl -I https://w3id.org/salmon-domain-ontology/research
curl -I https://w3id.org/salmon-domain-ontology/rda-case-study
```

Expected: redirect responses to the corresponding raw GitHub URLs.

## 5) Follow-up after registration

- Rewrite in-repo IRIs to canonical namespace (see `namespace-decision.md`).
- Update migration maps and downstream namespace compat tables.
- Cut one namespace-stabilization release from `main`.
