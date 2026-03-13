# Namespace stabilization release draft

Status: **completed; retained as the release-note draft for `0.0.0`**

## Recorded tag

`0.0.0`

## Suggested release title

`0.0.0 — smn namespace stabilization (pre-alpha)`

## Why this tag

- It is the first tag cut from the live `https://w3id.org/smn` namespace state.
- It marks the namespace/cutover stabilization checkpoint without implying a feature-complete public publication surface.
- `0.0.0` is the right maturity signal for this repo state: real namespace stabilization, still pre-alpha publication posture.

## Scope for this release slice

- Canonical shared namespace locked to `https://w3id.org/smn` (`smn:`).
- Ontology, module, research, and case-study build IRIs rewritten to the live namespace.
- Migration map and cutover docs aligned to the canonical `smn` story.
- Contributor issue templates added for low-friction term/model maintenance.
- Live W3ID redirect verification recorded for the conservative Turtle-first surface.
- Phase-2 closeout package aligned to the DFO provider-verification contract plus SPSR downstream smoke evidence.

## Explicitly not included in this release

- Published HTML docs.
- Published RDF/XML serialization.
- Published JSON-LD serialization.
- Versioned release snapshot directories served from a stable public host.
- Rich DFO-style content-negotiated publication targets.

## Release notes draft

```markdown
## Summary

This release establishes `https://w3id.org/smn` as the canonical shared namespace for the Salmon Domain Ontology and records the first stable live-namespace baseline.

## Included

- rewrites ontology/module/profile IRIs to the canonical `smn` base
- aligns migration artifacts and cutover docs to `smn:`
- records the DFO no-runtime provider-verification contract in place of the fictional DFO live-smoke gate
- documents the live W3ID redirect behavior for the current Turtle-first publication surface
- adds issue templates for new terms, missing superclasses, definition updates, and obsoletions

## Current publication posture

The W3ID path is live, but publication remains intentionally conservative for now:

- root, `/latest`, representative term/module/build/profile paths resolve to current Turtle artifacts
- HTML docs, RDF/XML, JSON-LD, and W3ID-backed version snapshot redirects are not published yet

## Validation

- ontology Turtle parse check passed for all files under `ontology/`
- live W3ID redirect verification recorded in `docs/publishing/evidence/2026-03-13-w3id-live-redirect-check.md`
- phase-2 closeout package aligned to SPSR smoke evidence plus the DFO provider-verification note

## Follow-up

- publish richer HTML/RDF/XML/JSON-LD targets
- add W3ID-backed versioned release snapshot redirects
- cut the next real release only after the richer publication surface exists
```
