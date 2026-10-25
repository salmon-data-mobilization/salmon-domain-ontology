#!/usr/bin/env python3
"""Post-process WIDOCO output for project-specific publication defaults.

Current policy for this repo:
- normalize the displayed ontology title to "Salmon Domain Ontology"
- remove "Draft" wording from the default WIDOCO subtitle
- normalize generated schema.org run timestamps to committed ontology metadata
- stabilize WIDOCO changelog list ordering across regenerations
- keep WIDOCO's raw bracketed predicate IRIs visible in HTML changelog items
- restore stable `#/Term` anchors for `smn:` terms
- inject the version IRI into the rendered metadata block
- strip trailing whitespace from generated publication artifacts
"""

from __future__ import annotations

import re
from html import escape as html_escape
from html.parser import HTMLParser
from pathlib import Path

from rdflib import Graph
from rdflib.namespace import DCTERMS, OWL, RDF


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "ontology" / "salmon-domain-ontology.ttl"
SMN_ENTITY_PATTERN = re.compile(
    r'(?P<indent>\s*)<div class="entity" id="https://w3id\.org/smn/(?P<term>[A-Za-z0-9._-]+)">'
)
SMN_LINK_PATTERN = re.compile(r'href="#https://w3id\.org/smn/([A-Za-z0-9._-]+)"')
# WIDOCO writes deleted predicate IRIs as raw `<http://...>` in changelog
# items. Browsers treat those as tags and hide the predicate from readers.
CHANGE_IRI_PATTERN = re.compile(r"<(https?://[^<>\s]+)>")


GENERATED_ARTIFACTS = (
    "docs/index.html",
    "docs/index-en.html",
    "docs/smn.owl",
)


def _load_ontology_metadata() -> tuple[str | None, str | None]:
    graph = Graph()
    graph.parse(SOURCE, format="turtle")
    ontology = next(graph.subjects(RDF.type, OWL.Ontology), None)
    if ontology is None:
        return None, None
    version_iri = graph.value(ontology, OWL.versionIRI)
    modified = graph.value(ontology, DCTERMS.modified)
    return (
        str(version_iri) if version_iri is not None else None,
        str(modified) if modified is not None else None,
    )


def _canonicalize_change_lists(content: str) -> str:
    # Match innermost lists only. WIDOCO nests per-term change lists inside
    # class/property lists, so a broad ``.*?`` pattern can consume across a
    # nested ``<ul>`` and leave the actual change items nondeterministic.
    ul_pattern = re.compile(r"<ul>(?:(?!<ul>|</ul>).)*</ul>", flags=re.S)

    def _normalize_ul(match: re.Match[str]) -> str:
        block = match.group(0)
        items = re.findall(r"<li>.*?</li>", block, flags=re.S)
        if not items:
            return block

        # Escape only the raw IRI tokens inside change items. Ordinary HTML
        # links and markup elsewhere in the generated page stay untouched.
        items = [
            CHANGE_IRI_PATTERN.sub(
                lambda iri: f"&lt;{html_escape(iri.group(1), quote=False)}&gt;",
                item,
            )
            for item in items
        ]
        normalized = [re.sub(r"\s+", " ", item).strip() for item in items]
        if not all(
            item.startswith("<li>Added:") or item.startswith("<li>Deleted:")
            for item in normalized
        ):
            return block

        ordered = [raw for _, raw in sorted(zip(normalized, items), key=lambda t: t[0])]
        indent_match = re.search(r"\n(\s*)<li>", block)
        indent = indent_match.group(1) if indent_match else ""
        return "<ul>\n" + "\n".join(f"{indent}{item.strip()}" for item in ordered) + "\n</ul>"

    return ul_pattern.sub(_normalize_ul, content)


def _self_test_changelog_predicate_visibility() -> None:
    """A WIDOCO `<IRI>` in a change item must remain visible HTML text."""
    class TextCollector(HTMLParser):
        def __init__(self) -> None:
            super().__init__()
            self.text: list[str] = []

        def handle_data(self, data: str) -> None:
            self.text.append(data)

    iri = "http://www.w3.org/2004/02/skos/core#closeMatch"
    example = f"<ul><li>Deleted: <{iri}> https://example.org/Thing</li></ul>"
    collector = TextCollector()
    collector.feed(_canonicalize_change_lists(example))
    if f"<{iri}>" not in "".join(collector.text):
        raise AssertionError("WIDOCO change predicate IRI is hidden as an HTML tag")


def _restore_smn_term_anchors(content: str) -> str:
    content = SMN_LINK_PATTERN.sub(lambda match: f'href="#/{match.group(1)}"', content)

    def _inject_anchor(match: re.Match[str]) -> str:
        indent = match.group("indent")
        term = match.group("term")
        return f'{indent}<a id="/{term}"></a>\n{indent}<div class="entity" id="https://w3id.org/smn/{term}">'

    return SMN_ENTITY_PATTERN.sub(_inject_anchor, content)


def _inject_version_iri(content: str, version_iri: str | None) -> str:
    if not version_iri or version_iri in content or "<dt>Previous version:</dt>" not in content:
        return content

    injection = (
        f'<dt>Version IRI:</dt>\n<dd><a href="{version_iri}">{version_iri}</a></dd>\n<dt>Previous version:</dt>'
    )
    return content.replace("<dt>Previous version:</dt>", injection, 1)


def _normalize_schema_org_dates(content: str, modified: str | None) -> str:
    if not modified:
        return content
    return re.sub(r'"dateReleased":"[^"]+"', f'"dateReleased":"{modified}"', content, count=1)


def _strip_trailing_whitespace(path: Path) -> None:
    content = path.read_text(encoding="utf-8")
    stripped = "\n".join(line.rstrip() for line in content.splitlines()).rstrip("\n") + "\n"
    if stripped != content:
        path.write_text(stripped, encoding="utf-8")
        print(f"Stripped trailing whitespace from {path}")


def patch_html(path: Path) -> None:
    content = path.read_text(encoding="utf-8")
    original = content
    version_iri, modified = _load_ontology_metadata()

    content = content.replace("Salmon Domain Ontology (modular build)", "Salmon Domain Ontology")
    content = content.replace("Ontology Specification Draft", "Ontology Specification")
    content = _normalize_schema_org_dates(content, modified)
    content = _canonicalize_change_lists(content)
    content = _restore_smn_term_anchors(content)
    content = _inject_version_iri(content, version_iri)

    if content != original:
        path.write_text(content, encoding="utf-8")
        print(f"Patched {path}")
    else:
        print(f"No changes for {path}")


def main() -> None:
    _self_test_changelog_predicate_visibility()
    for rel in ["docs/index.html", "docs/index-en.html"]:
        path = ROOT / rel
        if path.exists():
            patch_html(path)
    for rel in GENERATED_ARTIFACTS:
        path = ROOT / rel
        if path.exists():
            _strip_trailing_whitespace(path)


if __name__ == "__main__":
    main()
