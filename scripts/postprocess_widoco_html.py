#!/usr/bin/env python3
"""Post-process WIDOCO HTML output for project-specific UX defaults.

Current policy for this repo:
- normalize the displayed ontology title to "Salmon Domain Ontology"
- remove "Draft" wording from the default WIDOCO subtitle
- stabilize WIDOCO changelog list ordering across regenerations
"""

from __future__ import annotations

import re
from pathlib import Path


def _canonicalize_change_lists(content: str) -> str:
    ul_pattern = re.compile(r"<ul>\s*(?:<li>.*?</li>\s*)+</ul>", flags=re.S)

    def _normalize_ul(match: re.Match[str]) -> str:
        block = match.group(0)
        items = re.findall(r"<li>.*?</li>", block, flags=re.S)
        if not items:
            return block

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


def patch_html(path: Path) -> None:
    content = path.read_text(encoding="utf-8")
    original = content

    content = content.replace("Salmon Domain Ontology (modular build)", "Salmon Domain Ontology")
    content = content.replace("Ontology Specification Draft", "Ontology Specification")
    content = _canonicalize_change_lists(content)

    if content != original:
        path.write_text(content, encoding="utf-8")
        print(f"Patched {path}")
    else:
        print(f"No changes for {path}")


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    for rel in ["docs/index.html", "docs/index-en.html"]:
        path = root / rel
        if path.exists():
            patch_html(path)


if __name__ == "__main__":
    main()
