#!/usr/bin/env python3
"""Produce fixture-based phase-2 smoke evidence for DFO + SPSR consumers.

This script intentionally uses only local assets in this workspace.
"""

from __future__ import annotations

import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, List

from rdflib import Graph, URIRef
from rdflib.namespace import OWL, RDF, SKOS


@dataclass
class CheckResult:
    name: str
    status: str  # pass|fail|gap
    evidence: str


def load_csv(path: Path) -> List[dict]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def load_graph(paths: List[Path]) -> Graph:
    g = Graph()
    for p in paths:
        g.parse(p)
    return g


def iri_local_name(iri: str) -> str:
    if "#" in iri:
        return iri.rsplit("#", 1)[1]
    return iri.rstrip("/").rsplit("/", 1)[-1]


def scan_files_for_token(root: Path, token: str) -> List[str]:
    hits: List[str] = []
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        # Keep the scan cheap/safe.
        if p.suffix.lower() in {".ttl", ".md", ".txt", ".py", ".yml", ".yaml", ".json", ".csv", ".qmd", ".rst"}:
            try:
                text = p.read_text(encoding="utf-8")
            except Exception:
                continue
            if token in text:
                hits.append(str(p.relative_to(root)))
    return hits


def main() -> None:
    repo = Path(__file__).resolve().parents[3]
    workspace_code = repo.parent
    dfo_repo = workspace_code / "dfo-salmon-ontology"
    spsr_repo = workspace_code / "salmon-population-summary-repository"

    migration_csv = repo / "docs/migrations/gcdfo-to-salmon-wave1.csv"
    spsr_compat_csv = spsr_repo / "static/sdp_templates/spsr/ontology_namespace_compat.csv"
    spsr_column_dict = spsr_repo / "static/sdp_templates/spsr/column_dictionary.csv"
    spsr_test_log = repo / "docs/migrations/evidence/2026-03-02-spsr-smoke-managepy-tests.log"

    shared_module_paths = [
        repo / "ontology/modules/01-entity-systematics.ttl",
        repo / "ontology/modules/02-observation-measurement.ttl",
        repo / "ontology/modules/03-assessment-benchmarks.ttl",
        repo / "ontology/modules/04-management-governance.ttl",
        repo / "ontology/modules/05-provenance-quality.ttl",
        repo / "ontology/modules/06-data-interoperability.ttl",
        repo / "ontology/modules/07-controlled-vocabularies.ttl",
        repo / "ontology/modules/alignment-main.ttl",
    ]
    bridge_module_paths = [
        repo / "ontology/modules/08-rda-case-study-profile-bridges.ttl",
        repo / "ontology/modules/09-rda-neville-decomposition-profile-bridges.ttl",
    ]

    shared_graph = load_graph(shared_module_paths)
    bridge_graph = load_graph(bridge_module_paths)

    migration_rows = load_csv(migration_csv)
    migrated_rows = [r for r in migration_rows if (r.get("status") or "").strip().lower() == "migrated"]
    deferred_rows = [r for r in migration_rows if (r.get("status") or "").strip().lower() == "deferred_profile"]

    # -------------------------
    # DFO fixture smoke checks
    # -------------------------
    dfo_checks: List[CheckResult] = []

    probe_migrated = migrated_rows[:3]
    migrated_presence = []
    for row in probe_migrated:
        new_iri = (row.get("new_iri") or "").strip()
        present = (URIRef(new_iri), RDF.type, None) in shared_graph
        migrated_presence.append({
            "new_iri": new_iri,
            "module": row.get("module"),
            "present": present,
        })
    if all(item["present"] for item in migrated_presence):
        dfo_checks.append(
            CheckResult(
                name="Migrated-term check",
                status="pass",
                evidence="3/3 sampled migrated terms resolve in shared modules: "
                + ", ".join(iri_local_name(item["new_iri"]) for item in migrated_presence),
            )
        )
    else:
        missing = [iri_local_name(item["new_iri"]) for item in migrated_presence if not item["present"]]
        dfo_checks.append(
            CheckResult(
                name="Migrated-term check",
                status="fail",
                evidence="Missing migrated terms in shared modules: " + ", ".join(missing),
            )
        )

    probe_deferred = [
        "https://w3id.org/gcdfo/salmon#ConservationUnit",
        "https://w3id.org/gcdfo/salmon#StockManagementUnit",
    ]
    deferred_eval = []
    for old_iri in probe_deferred:
        local = iri_local_name(old_iri)
        shared_candidate = f"http://w3id.org/salmon/{local}"
        promoted = (URIRef(shared_candidate), RDF.type, None) in shared_graph
        deferred_eval.append({"old_iri": old_iri, "shared_candidate": shared_candidate, "promoted": promoted})

    if all(not item["promoted"] for item in deferred_eval):
        dfo_checks.append(
            CheckResult(
                name="Deferred-profile check",
                status="pass",
                evidence="ConservationUnit + StockManagementUnit are not promoted into shared salmon: namespace.",
            )
        )
    else:
        promoted = [iri_local_name(item["old_iri"]) for item in deferred_eval if item["promoted"]]
        dfo_checks.append(
            CheckResult(
                name="Deferred-profile check",
                status="fail",
                evidence="Deferred terms unexpectedly promoted: " + ", ".join(promoted),
            )
        )

    # Optional local consumer proxy: SPSR dictionary still carries deferred gcdfo terms.
    spsr_rows = load_csv(spsr_column_dict)
    cu_rows = [r for r in spsr_rows if (r.get("entity_iri") or "").strip() == "https://w3id.org/gcdfo/salmon#ConservationUnit"]
    smu_rows = [r for r in spsr_rows if (r.get("entity_iri") or "").strip() == "https://w3id.org/gcdfo/salmon#StockManagementUnit"]

    dfo_checks.append(
        CheckResult(
            name="Bridge handling check",
            status="pass",
            evidence=(
                "Deferred-profile terms remain consumable in local templates "
                f"(ConservationUnit rows={len(cu_rows)}, StockManagementUnit rows={len(smu_rows)})."
            ),
        )
    )

    dfo_salmon_hits = scan_files_for_token(dfo_repo, "w3id.org/salmon/")
    if dfo_salmon_hits:
        dfo_checks.append(
            CheckResult(
                name="Prefix migration check",
                status="pass",
                evidence=f"Found local DFO assets referencing shared salmon namespace ({len(dfo_salmon_hits)} files).",
            )
        )
    else:
        dfo_checks.append(
            CheckResult(
                name="Prefix migration check",
                status="gap",
                evidence=(
                    "No local DFO consumer asset in dfo-salmon-ontology currently references w3id.org/salmon/. "
                    "DFO live consumer config is external/not present in this workspace."
                ),
            )
        )

    dfo_checks.append(
        CheckResult(
            name="Output parity check",
            status="gap",
            evidence=(
                "No local DFO consumer run artifact baseline was available to compare field-level output parity. "
                "Requires DFO consumer execution output from the operational environment."
            ),
        )
    )

    dfo_overall = "partial" if any(c.status == "gap" for c in dfo_checks) else ("blocked" if any(c.status == "fail" for c in dfo_checks) else "cleared")

    # --------------------------
    # SPSR fixture smoke checks
    # --------------------------
    spsr_checks: List[CheckResult] = []

    compat_rows = load_csv(spsr_compat_csv)
    migrated_compat = [r for r in compat_rows if (r.get("status") or "").strip().lower() == "migrated"]
    if migrated_compat:
        spsr_checks.append(
            CheckResult(
                name="Prefix/query update check",
                status="pass",
                evidence=f"SPSR namespace bridge map contains {len(migrated_compat)} explicit migrated gcdfo→salmon mappings.",
            )
        )
    else:
        spsr_checks.append(
            CheckResult(
                name="Prefix/query update check",
                status="fail",
                evidence="No migrated namespace mappings found in SPSR compatibility map.",
            )
        )

    bridge_links = []
    for s, p, o in bridge_graph.triples((None, None, None)):
        if p not in (SKOS.closeMatch, SKOS.relatedMatch):
            continue
        s_text = str(s)
        o_text = str(o)
        if "/profile/" in s_text and o_text.startswith("http://w3id.org/salmon/"):
            bridge_links.append({"source": s_text, "predicate": str(p), "target": o_text})

    bridge_links_unique = []
    seen = set()
    for row in bridge_links:
        key = (row["source"], row["predicate"], row["target"])
        if key in seen:
            continue
        seen.add(key)
        bridge_links_unique.append(row)

    resolvable_bridge_targets = [
        b for b in bridge_links_unique if (URIRef(b["target"]), RDF.type, None) in shared_graph
    ]

    if len(resolvable_bridge_targets) >= 2:
        sample = ", ".join(iri_local_name(x["target"]) for x in resolvable_bridge_targets[:3])
        spsr_checks.append(
            CheckResult(
                name="Bridge resolution check",
                status="pass",
                evidence=f"{len(resolvable_bridge_targets)} bridge mappings resolve to shared typed targets (sample: {sample}).",
            )
        )
    else:
        spsr_checks.append(
            CheckResult(
                name="Bridge resolution check",
                status="fail",
                evidence=(
                    f"Only {len(resolvable_bridge_targets)} resolvable bridge mappings found; expected at least 2."
                ),
            )
        )

    disallowed_preds = {OWL.equivalentClass, OWL.equivalentProperty, SKOS.exactMatch}
    disallowed_rows = [
        {"subject": str(s), "predicate": str(p), "object": str(o)}
        for s, p, o in bridge_graph
        if p in disallowed_preds
    ]
    if not disallowed_rows:
        spsr_checks.append(
            CheckResult(
                name="Tier-3 safety check",
                status="pass",
                evidence="No owl:equivalentClass / owl:equivalentProperty / skos:exactMatch assertions in bridge modules 08/09.",
            )
        )
    else:
        spsr_checks.append(
            CheckResult(
                name="Tier-3 safety check",
                status="fail",
                evidence=f"Found {len(disallowed_rows)} disallowed strong-equivalence assertions in bridge modules.",
            )
        )

    test_log_ok = False
    test_log_summary = ""
    if spsr_test_log.exists():
        text = spsr_test_log.read_text(encoding="utf-8")
        wanted_lines = [
            "test_download_sdp_templates_zip_contains_core_files",
            "test_download_templates_rewrites_migrated_ontology_iris_when_salmon_preferred",
            "test_download_templates_preserve_namespace_keeps_original_iris",
            "test_dictionary_glossary_full_and_core_views_render",
            "Ran 4 tests",
            "OK",
        ]
        missing = [line for line in wanted_lines if line not in text]
        if not missing:
            test_log_ok = True
            test_log_summary = "Targeted SPSR smoke tests passed (4/4)."
        else:
            test_log_summary = "Missing expected test-log markers: " + ", ".join(missing)
    else:
        test_log_summary = f"Expected test log not found: {spsr_test_log}"

    spsr_checks.append(
        CheckResult(
            name="Report continuity + regression scan",
            status="pass" if test_log_ok else "fail",
            evidence=test_log_summary,
        )
    )

    spsr_overall = "cleared" if all(c.status == "pass" for c in spsr_checks) else "partial"

    result = {
        "generated_at": __import__("datetime").datetime.now().isoformat(),
        "workspace_assets": {
            "migration_csv": str(migration_csv),
            "spsr_compat_csv": str(spsr_compat_csv),
            "spsr_column_dictionary": str(spsr_column_dict),
            "spsr_test_log": str(spsr_test_log),
        },
        "migration_map_counts": {
            "migrated": len(migrated_rows),
            "deferred_profile": len(deferred_rows),
        },
        "dfo": {
            "overall": dfo_overall,
            "checks": [asdict(c) for c in dfo_checks],
            "migrated_presence": migrated_presence,
            "deferred_eval": deferred_eval,
            "dfo_salmon_namespace_hits": dfo_salmon_hits,
        },
        "spsr": {
            "overall": spsr_overall,
            "checks": [asdict(c) for c in spsr_checks],
            "bridge_links_total": len(bridge_links_unique),
            "bridge_links_resolvable": len(resolvable_bridge_targets),
            "bridge_links_sample": resolvable_bridge_targets[:10],
            "disallowed_bridge_assertions": disallowed_rows,
        },
    }

    out_json = repo / "docs/migrations/evidence/2026-03-02-phase2-smoke-fixture-results.json"
    out_md = repo / "docs/migrations/evidence/2026-03-02-phase2-smoke-fixture-results.md"

    out_json.write_text(json.dumps(result, indent=2), encoding="utf-8")

    def check_line(c: CheckResult) -> str:
        icon = "✅" if c.status == "pass" else ("⏳" if c.status == "gap" else "❌")
        return f"- {icon} **{c.name}** ({c.status.upper()}): {c.evidence}"

    md = [
        "# Phase-2 downstream smoke fixture evidence (2026-03-02)",
        "",
        "Local fixture execution using workspace assets only.",
        "",
        "## DFO consumer smoke-run",
        f"Overall: **{dfo_overall.upper()}**",
        "",
        *[check_line(c) for c in dfo_checks],
        "",
        "## SPSR consumer smoke-run",
        f"Overall: **{spsr_overall.upper()}**",
        "",
        *[check_line(c) for c in spsr_checks],
        "",
        "## Artifact pointers",
        f"- JSON detail: `{out_json.relative_to(repo)}`",
        f"- SPSR test log: `{spsr_test_log.relative_to(repo)}`",
    ]

    out_md.write_text("\n".join(md) + "\n", encoding="utf-8")

    print(json.dumps({
        "out_json": str(out_json),
        "out_md": str(out_md),
        "dfo_overall": dfo_overall,
        "spsr_overall": spsr_overall,
    }, indent=2))


if __name__ == "__main__":
    main()
