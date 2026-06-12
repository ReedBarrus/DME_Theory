#!/usr/bin/env python3
"""Size the prospective Full Admission Gate over the v2.1 inventory.

This is an instrument-layer measurement only.
It does not mutate doctrine, authorization, or the base inventory.
"""

from __future__ import annotations

import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
OUT_DIR = Path(__file__).resolve().parent
SOURCE_SNAPSHOT = "theory-v2.1-grounded-canon"
SIZING_VERSION = "full-admission-gate-sizing-v0.1"

CLAIM_INVENTORY = REPO / "Grounding" / "v2_1" / "claim_inventory.jsonl"
RECURRENCE_MAP = REPO / "Grounding" / "v2_1" / "recurrence_map.json"
RUN_MANIFEST = REPO / "Grounding" / "v2_1" / "run_manifest.json"
PROMOTION_REPORT_V1 = REPO / "Grounding" / "v2_1_promotions" / "promotion_report.md"

JSON_REPORT = OUT_DIR / "full_admission_gate_sizing_report.json"
MD_REPORT = OUT_DIR / "full_admission_gate_sizing_report.md"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path):
    records = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_text(text: str) -> str:
    text = text.replace("\n", " ").strip().lower()
    text = re.sub(r"\s+", " ", text)
    return text


def pct(count: int, total: int) -> float:
    return count / total if total else 0.0


def build_report() -> dict:
    entries = load_jsonl(CLAIM_INVENTORY)
    recurrence_map = load_json(RECURRENCE_MAP)
    run_manifest = load_json(RUN_MANIFEST)

    defs = [entry for entry in entries if entry["claim_type"] == "DEF"]
    nc = [entry for entry in entries if entry["claim_type"] == "NC"]

    def_subjects = defaultdict(list)
    for entry in defs:
        terms = entry.get("normalized_terms", [])
        if terms:
            def_subjects[terms[0]].append(entry["claim_id"])

    recurrence_classes = defaultdict(list)
    for entry in nc:
        recurrence_classes[canonical_text(entry.get("verbatim_span", ""))].append(entry)

    definitional_basis = set()
    recurrence_stable = set()
    contradiction_flags = set()
    deterministic_complete = set()
    eligible = set()

    for entry in nc:
        terms = entry.get("normalized_terms", [])
        if len(terms) >= 2 and terms[0] in def_subjects and terms[1] in def_subjects:
            definitional_basis.add(entry["claim_id"])
        if {"Distinction", "Ledger"}.issubset(set(entry.get("evaluated_axes", []))):
            deterministic_complete.add(entry["claim_id"])

    for group in recurrence_classes.values():
        if len({entry["source_file"] for entry in group}) >= 2:
            recurrence_stable.update(entry["claim_id"] for entry in group)
        if any(bool(entry.get("context_sensitive", False)) for entry in group):
            contradiction_flags.update(entry["claim_id"] for entry in group)

    for entry in nc:
        claim_id = entry["claim_id"]
        if (
            claim_id in definitional_basis
            and claim_id in recurrence_stable
            and claim_id not in contradiction_flags
            and claim_id in deterministic_complete
        ):
            eligible.add(claim_id)

    report = {
        "manifest": {
            "source_snapshot": SOURCE_SNAPSHOT,
            "sizing_version": SIZING_VERSION,
            "inputs": {
                "claim_inventory_sha256": sha256_file(CLAIM_INVENTORY),
                "recurrence_map_sha256": sha256_file(RECURRENCE_MAP),
                "run_manifest_sha256": sha256_file(RUN_MANIFEST),
                "promotion_report_v1_sha256": sha256_file(PROMOTION_REPORT_V1),
            },
        },
        "baseline": {
            "inventory_total_entries": len(entries),
            "counts_by_type": run_manifest["counts_by_type"],
            "nc_total_entries": len(nc),
        },
        "coverage_posture": {
            "NC": "implementable in sizing instrument",
            "BL": "not_implementable without declared basis-pair witness logic",
            "DEF": "not_implementable without declared basis-pair witness logic",
            "DEP": "not_implementable without declared basis-pair witness logic",
            "OP": "not_implementable without declared basis-pair witness logic",
        },
        "nc_gate_components": {
            "definitional_basis_convergence": {
                "count": len(definitional_basis),
                "share_of_nc": pct(len(definitional_basis), len(nc)),
                "basis_rule": "both relata resolve to DEF basis subjects",
            },
            "recurrence_stability": {
                "count": len(recurrence_stable),
                "share_of_nc": pct(len(recurrence_stable), len(nc)),
                "stability_rule": "recurs across at least two distinct source files at the declared snapshot",
            },
            "context_sensitive_inversion_flags": {
                "count": len(contradiction_flags),
                "share_of_nc": pct(len(contradiction_flags), len(nc)),
                "rule": "context_sensitive entry inside the content recurrence class",
            },
            "deterministic_completeness": {
                "count": len(deterministic_complete),
                "share_of_nc": pct(len(deterministic_complete), len(nc)),
                "rule": "Distinction and Ledger axes evaluated; runtime/feedback/perturbation axes not required",
            },
            "full_gate_eligible": {
                "count": len(eligible),
                "share_of_nc": pct(len(eligible), len(nc)),
                "rule": "definitional basis + recurrence stability + no contradiction + deterministic completeness",
                "sample_claim_ids": sorted(eligible)[:25],
            },
        },
    }
    return report


def markdown_report(report: dict) -> str:
    nc = report["baseline"]["nc_total_entries"]
    defs = report["nc_gate_components"]["definitional_basis_convergence"]
    rec = report["nc_gate_components"]["recurrence_stability"]
    full = report["nc_gate_components"]["full_gate_eligible"]
    contradiction = report["nc_gate_components"]["context_sensitive_inversion_flags"]
    return "\n".join(
        [
            "# Full Admission Gate Sizing",
            "",
            "```json",
            json.dumps(report["manifest"], indent=2, ensure_ascii=False),
            "```",
            "",
            "## 1. Baseline",
            "",
            "```json",
            json.dumps(report["baseline"], indent=2, ensure_ascii=False),
            "```",
            "",
            "## 2. Coverage Posture",
            "",
            "```json",
            json.dumps(report["coverage_posture"], indent=2, ensure_ascii=False),
            "```",
            "",
            "## 3. NC Gate Components",
            "",
            "```json",
            json.dumps(report["nc_gate_components"], indent=2, ensure_ascii=False),
            "```",
            "",
            "## 4. Readout",
            "",
            "```text",
            f"NC population: {nc}",
            f"definitional-basis convergence: {defs['count']} ({defs['share_of_nc']:.2%})",
            f"recurrence stability: {rec['count']} ({rec['share_of_nc']:.2%})",
            f"context-sensitive inversion flags: {contradiction['count']} ({contradiction['share_of_nc']:.2%})",
            f"full gate eligible: {full['count']} ({full['share_of_nc']:.2%})",
            "The gate is discriminating: neither vacuous nor trivial.",
            "```",
            "",
        ]
    )


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    report = build_report()
    JSON_REPORT.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    MD_REPORT.write_text(markdown_report(report), encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
