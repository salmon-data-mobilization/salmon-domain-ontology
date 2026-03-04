#!/usr/bin/env python3
"""Compare DFO smoke output artifact against a baseline artifact.

Supports CSV and JSON artifacts.

PASS rule:
- candidate contains all baseline fields/keys required for structural parity
- file formats match

Extras in candidate are reported as warnings but do not fail parity by default.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple


def detect_format(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix == ".csv":
        return "csv"
    if suffix == ".json":
        return "json"
    return "unknown"


def read_csv_schema(path: Path) -> Tuple[List[str], int]:
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames or []
        row_count = sum(1 for _ in reader)
    return headers, row_count


def read_json_structure(path: Path) -> Tuple[str, Set[str], int]:
    data = json.loads(path.read_text(encoding="utf-8"))

    if isinstance(data, list):
        keys: Set[str] = set()
        for row in data:
            if isinstance(row, dict):
                keys.update(row.keys())
        return "list", keys, len(data)

    if isinstance(data, dict):
        return "object", set(data.keys()), len(data)

    return type(data).__name__, set(), 1


def to_sorted_list(items: Set[str]) -> List[str]:
    return sorted(items)


def main() -> int:
    parser = argparse.ArgumentParser(description="Check structural output parity for DFO smoke artifacts.")
    parser.add_argument("--candidate", required=True, help="Path to candidate output artifact (new run)")
    parser.add_argument("--baseline", required=True, help="Path to baseline output artifact (last known-good)")
    parser.add_argument("--out-json", required=True, help="Path to write parity result JSON")
    parser.add_argument("--out-md", required=True, help="Path to write parity result Markdown")
    args = parser.parse_args()

    candidate_path = Path(args.candidate).resolve()
    baseline_path = Path(args.baseline).resolve()
    out_json_path = Path(args.out_json).resolve()
    out_md_path = Path(args.out_md).resolve()
    out_json_path.parent.mkdir(parents=True, exist_ok=True)
    out_md_path.parent.mkdir(parents=True, exist_ok=True)

    if not candidate_path.exists() or not baseline_path.exists():
        missing = []
        if not candidate_path.exists():
            missing.append(str(candidate_path))
        if not baseline_path.exists():
            missing.append(str(baseline_path))
        result = {
            "status": "fail",
            "reason": "missing_input_files",
            "missing": missing,
            "candidate": str(candidate_path),
            "baseline": str(baseline_path),
        }
        out_json_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        out_md_path.write_text(
            "# DFO output parity check\n\n"
            "Status: **FAIL**\n\n"
            "Missing input files:\n"
            + "\n".join(f"- `{m}`" for m in missing)
            + "\n",
            encoding="utf-8",
        )
        print("PARITY FAIL: missing input files")
        return 1

    candidate_format = detect_format(candidate_path)
    baseline_format = detect_format(baseline_path)

    result: Dict[str, Any] = {
        "candidate": str(candidate_path),
        "baseline": str(baseline_path),
        "candidate_format": candidate_format,
        "baseline_format": baseline_format,
    }

    if candidate_format == "unknown" or baseline_format == "unknown" or candidate_format != baseline_format:
        result.update(
            {
                "status": "fail",
                "reason": "format_mismatch_or_unsupported",
            }
        )
        out_json_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        out_md_path.write_text(
            "# DFO output parity check\n\n"
            "Status: **FAIL**\n\n"
            f"- Candidate format: `{candidate_format}`\n"
            f"- Baseline format: `{baseline_format}`\n"
            "- Reason: format mismatch or unsupported type\n",
            encoding="utf-8",
        )
        print("PARITY FAIL: format mismatch or unsupported")
        return 1

    if candidate_format == "csv":
        candidate_headers, candidate_rows = read_csv_schema(candidate_path)
        baseline_headers, baseline_rows = read_csv_schema(baseline_path)

        candidate_set = set(candidate_headers)
        baseline_set = set(baseline_headers)

        missing_required = baseline_set - candidate_set
        extras = candidate_set - baseline_set

        status = "pass" if not missing_required else "fail"

        result.update(
            {
                "status": status,
                "type": "csv",
                "candidate_headers": candidate_headers,
                "baseline_headers": baseline_headers,
                "missing_required_headers": to_sorted_list(missing_required),
                "extra_candidate_headers": to_sorted_list(extras),
                "candidate_row_count": candidate_rows,
                "baseline_row_count": baseline_rows,
                "row_count_delta": candidate_rows - baseline_rows,
            }
        )

        md_lines = [
            "# DFO output parity check",
            "",
            f"Status: **{status.upper()}**",
            "",
            "## Artifact summary",
            f"- Candidate: `{candidate_path}`",
            f"- Baseline: `{baseline_path}`",
            f"- Format: `{candidate_format}`",
            "",
            "## Header parity",
            f"- Missing required headers in candidate: {len(missing_required)}",
            f"- Extra candidate headers: {len(extras)}",
            "",
            "## Row counts",
            f"- Candidate rows: {candidate_rows}",
            f"- Baseline rows: {baseline_rows}",
            f"- Delta: {candidate_rows - baseline_rows}",
        ]

        if missing_required:
            md_lines.extend(["", "### Missing required headers", *[f"- `{h}`" for h in sorted(missing_required)]])
        if extras:
            md_lines.extend(["", "### Extra candidate headers (warning)", *[f"- `{h}`" for h in sorted(extras)]])

        out_json_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        out_md_path.write_text("\n".join(md_lines) + "\n", encoding="utf-8")

        if status == "pass":
            print("PARITY PASS")
            return 0
        print("PARITY FAIL")
        return 1

    # JSON
    candidate_shape, candidate_keys, candidate_count = read_json_structure(candidate_path)
    baseline_shape, baseline_keys, baseline_count = read_json_structure(baseline_path)

    missing_required = baseline_keys - candidate_keys
    extras = candidate_keys - baseline_keys

    shape_mismatch = candidate_shape != baseline_shape
    status = "pass" if (not missing_required and not shape_mismatch) else "fail"

    result.update(
        {
            "status": status,
            "type": "json",
            "candidate_shape": candidate_shape,
            "baseline_shape": baseline_shape,
            "missing_required_keys": to_sorted_list(missing_required),
            "extra_candidate_keys": to_sorted_list(extras),
            "candidate_record_count": candidate_count,
            "baseline_record_count": baseline_count,
            "record_count_delta": candidate_count - baseline_count,
            "shape_mismatch": shape_mismatch,
        }
    )

    md_lines = [
        "# DFO output parity check",
        "",
        f"Status: **{status.upper()}**",
        "",
        "## Artifact summary",
        f"- Candidate: `{candidate_path}`",
        f"- Baseline: `{baseline_path}`",
        "- Format: `json`",
        f"- Candidate shape: `{candidate_shape}`",
        f"- Baseline shape: `{baseline_shape}`",
        "",
        "## Key parity",
        f"- Missing required keys in candidate: {len(missing_required)}",
        f"- Extra candidate keys: {len(extras)}",
        "",
        "## Record counts",
        f"- Candidate record count: {candidate_count}",
        f"- Baseline record count: {baseline_count}",
        f"- Delta: {candidate_count - baseline_count}",
    ]

    if shape_mismatch:
        md_lines.extend(["", "### Shape mismatch", "- Candidate and baseline JSON top-level shapes differ."])
    if missing_required:
        md_lines.extend(["", "### Missing required keys", *[f"- `{k}`" for k in sorted(missing_required)]])
    if extras:
        md_lines.extend(["", "### Extra candidate keys (warning)", *[f"- `{k}`" for k in sorted(extras)]])

    out_json_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    out_md_path.write_text("\n".join(md_lines) + "\n", encoding="utf-8")

    if status == "pass":
        print("PARITY PASS")
        return 0
    print("PARITY FAIL")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
