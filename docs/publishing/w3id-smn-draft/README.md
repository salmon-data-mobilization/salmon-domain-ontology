# /smn/

Salmon Domain Ontology shared namespace (`smn:`).

## Canonical IRIs

- Latest ontology IRI: `https://w3id.org/smn`
- Term namespace: `https://w3id.org/smn/`
- Module namespace: `https://w3id.org/smn/modules/<module-name>`
- Research build: `https://w3id.org/smn/research`
- Case-study build: `https://w3id.org/smn/rda-case-study`
- Profile roots:
  - `https://w3id.org/smn/profile/hakai/`
  - `https://w3id.org/smn/profile/neville/`
  - `https://w3id.org/smn/profile/rda-case-study/`

## Maintainer repository

- <https://github.com/salmon-data-mobilization/salmon-domain-ontology>

## Maintainer contact

- Brett Johnson — GitHub: `Br-Johnson`

## Local reference status

This folder records the conservative Turtle-first W3ID registration materials now live for `smn`.
Keep it as the local reference copy for future redirect revisions.

Current publication gaps:

1. No GitHub Pages site (or equivalent public HTML doc surface) is live for this repo.
2. No published RDF/XML serialization exists.
3. No published JSON-LD serialization exists.
4. No W3ID-backed SemVer release snapshot redirects are live yet. The repo tag `0.0.0` exists, but version-path redirects are still future work.

Because of those gaps, the live `.htaccess` rules currently use a safe latest-Turtle fallback and keep the full DFO-style content-negotiation pattern documented for later activation.

## Verification commands

### Conservative Turtle-first checks

```bash
curl -I https://w3id.org/smn
curl -I https://w3id.org/smn/latest
curl -I https://w3id.org/smn/Stock
curl -I https://w3id.org/smn/modules/01-entity-systematics
curl -I https://w3id.org/smn/research
curl -I https://w3id.org/smn/rda-case-study
curl -I https://w3id.org/smn/profile/hakai
curl -I -H 'Accept: text/turtle' https://w3id.org/smn
```

Expected: root returns `301` to the trailing-slash form, then `303` redirects resolve to the matching raw GitHub Turtle artifact.

### Future DFO-style checks

Run these only after stable public assets exist:

```bash
curl -I -H 'Accept: text/turtle' https://w3id.org/smn
curl -I -H 'Accept: application/rdf+xml' https://w3id.org/smn
curl -I -H 'Accept: application/ld+json' https://w3id.org/smn
curl -I https://w3id.org/smn/0.0.0
```

Expected: `303` redirects to latest HTML/Turtle/RDFXML/JSON-LD assets plus SemVer release snapshots.

## Upgrade step

Before switching the W3ID rules to the richer publication pattern, publish or stage a stable public target surface for:

- latest HTML docs,
- latest Turtle,
- latest RDF/XML,
- latest JSON-LD,
- versioned release snapshots.

Then replace the conservative fallback section in `.htaccess` with the DFO-style latest/version redirect rules.
