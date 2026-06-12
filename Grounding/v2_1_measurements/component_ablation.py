#!/usr/bin/env python3
"""Component ablation and quotient diagnostic for ODQ-4/5.

This is an instrument-layer diagnostic only.
It measures whether identity coordinates annihilate comparability
and whether quotienting by recurrence classes restores order
behavior once span/provenance are removed from the epistemic order.
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
DIAGNOSTIC_VERSION = "component-ablation-v0.1"

CLAIM_INVENTORY = REPO / "Grounding" / "v2_1" / "claim_inventory.jsonl"
RUN_MANIFEST = REPO / "Grounding" / "v2_1" / "run_manifest.json"
PROVISIONAL_SUITE = OUT_DIR / "suite_report.json"

SUPPORT_ORDER = {
    "inferred_candidate": 0,
    "structurally_supported": 1,
    "partially_admitted": 2,
    "fully_admitted": 3,
    "ledger_supported": 4,
    "feedback_tested": 5,
}

OPACITY_ORDER = {
    "opaque": 0,
    "conjectural": 1,
    "candidate": 2,
    "partially_supported": 3,
    "fully_supported": 4,
}


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path):
    entries = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                entries.append(json.loads(line))
    return entries


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_text(text: str) -> str:
    text = text.replace("\n", " ").strip().lower()
    text = re.sub(r"\s+", " ", text)
    return text


def ordered_relation(left: str, right: str, order: dict[str, int]) -> str:
    if order[left] == order[right]:
        return "equal"
    if order[left] < order[right]:
        return "left_leq_right"
    return "right_leq_left"


def subset_relation(left: list[str], right: list[str]) -> str:
    left_set = set(left)
    right_set = set(right)
    if left_set == right_set:
        return "equal"
    if left_set.issubset(right_set):
        return "left_leq_right"
    if right_set.issubset(left_set):
        return "right_leq_left"
    return "incomparable"


def reverse_subset_relation(left: list[str], right: list[str]) -> str:
    return subset_relation(right, left)


def span_provenance_relation(left: dict, right: dict) -> str:
    if left["source_file"] != right["source_file"]:
        return "incomparable"
    if left["source_snapshot"] != right["source_snapshot"]:
        return "incomparable"

    left_line = tuple(left["line_range"])
    right_line = tuple(right["line_range"])
    left_char = tuple(left["char_span"])
    right_char = tuple(right["char_span"])

    if (
        left_line == right_line
        and left_char == right_char
        and left.get("verbatim_span") == right.get("verbatim_span")
    ):
        return "equal"

    left_contains_right = (
        left_line[0] <= right_line[0]
        and left_line[1] >= right_line[1]
        and left_char[0] <= right_char[0]
        and left_char[1] >= right_char[1]
    )
    right_contains_left = (
        right_line[0] <= left_line[0]
        and right_line[1] >= left_line[1]
        and right_char[0] <= left_char[0]
        and right_char[1] >= left_char[1]
    )
    if left_contains_right:
        return "left_leq_right"
    if right_contains_left:
        return "right_leq_left"
    return "incomparable"


def product_relation(relations: list[str]) -> str:
    if "incomparable" in relations:
        return "incomparable"
    strict_left = any(rel == "left_leq_right" for rel in relations)
    strict_right = any(rel == "right_leq_left" for rel in relations)
    if strict_left and strict_right:
        return "incomparable"
    if strict_left:
        return "left_leq_right"
    if strict_right:
        return "right_leq_left"
    return "equal"


def summarize_relations(counter: Counter[str]) -> dict[str, object]:
    total_pairs = sum(counter.values())
    comparable_pairs = total_pairs - counter["incomparable"]
    return {
        "total_pairs": total_pairs,
        "equal": counter["equal"],
        "left_leq_right": counter["left_leq_right"],
        "right_leq_left": counter["right_leq_left"],
        "incomparable": counter["incomparable"],
        "comparability_rate": (
            comparable_pairs / total_pairs if total_pairs else None
        ),
    }


def all_within_type_pairs(entries: list[dict]):
    grouped = defaultdict(list)
    for entry in entries:
        grouped[entry["claim_type"]].append(entry)
    for group in grouped.values():
        for index, left in enumerate(group):
            for right in group[index + 1 :]:
                yield left, right


def recurrence_class_key(entry: dict):
    return (
        entry["claim_type"],
        canonical_text(entry.get("verbatim_span", "")),
        entry.get("opacity_status"),
        tuple(sorted(entry.get("evaluated_axes", []))),
        tuple(sorted(entry.get("omitted_axes", []))),
    )


def quotient_relation(left: dict, right: dict) -> str:
    relations = [
        ordered_relation(left["support_status"], right["support_status"], SUPPORT_ORDER),
        ordered_relation(left["opacity_status"], right["opacity_status"], OPACITY_ORDER),
        subset_relation(left.get("evaluated_axes", []), right.get("evaluated_axes", [])),
        reverse_subset_relation(left.get("omitted_axes", []), right.get("omitted_axes", [])),
    ]
    return product_relation(relations)


def build_report() -> dict[str, object]:
    entries = load_jsonl(CLAIM_INVENTORY)
    run_manifest = load_json(RUN_MANIFEST)
    provisional_suite = load_json(PROVISIONAL_SUITE)

    support_counter = Counter()
    opacity_counter = Counter()
    axes_counter = Counter()
    span_provenance_counter = Counter()

    for left, right in all_within_type_pairs(entries):
        support_counter[ordered_relation(left["support_status"], right["support_status"], SUPPORT_ORDER)] += 1
        opacity_counter[ordered_relation(left["opacity_status"], right["opacity_status"], OPACITY_ORDER)] += 1
        axes_counter[subset_relation(left.get("evaluated_axes", []), right.get("evaluated_axes", []))] += 1
        span_provenance_counter[span_provenance_relation(left, right)] += 1

    recurrence_classes = defaultdict(list)
    for entry in entries:
        recurrence_classes[recurrence_class_key(entry)].append(entry)

    retained_classes = {
        key: group for key, group in recurrence_classes.items() if len(group) >= 2
    }
    quotient_counter = Counter()
    for group in retained_classes.values():
        for index, left in enumerate(group):
            for right in group[index + 1 :]:
                quotient_counter[quotient_relation(left, right)] += 1

    support_summary = summarize_relations(support_counter)
    opacity_summary = summarize_relations(opacity_counter)
    axes_summary = summarize_relations(axes_counter)
    span_provenance_summary = summarize_relations(span_provenance_counter)
    quotient_summary = summarize_relations(quotient_counter)

    homogeneity_caveat = (
        "Support, opacity, and evaluated-axis signatures are highly homogeneous in the "
        "current inventory. The ablation cleanly isolates identity-coordinate annihilation, "
        "but it does not by itself verify discriminating order behavior under future status divergence."
    )

    return {
        "manifest": {
            "source_snapshot": SOURCE_SNAPSHOT,
            "diagnostic_version": DIAGNOSTIC_VERSION,
            "inputs": {
                "claim_inventory_sha256": sha256_file(CLAIM_INVENTORY),
                "run_manifest_sha256": sha256_file(RUN_MANIFEST),
                "provisional_suite_sha256": sha256_file(PROVISIONAL_SUITE),
            },
        },
        "baseline": {
            "inventory_total_entries": len(entries),
            "counts_by_type": run_manifest["counts_by_type"],
            "provisional_summary_verdict": provisional_suite["summary_verdict"],
        },
        "component_ablation": {
            "support_status_only": support_summary,
            "opacity_status_only": opacity_summary,
            "evaluated_axes_only": axes_summary,
            "span_provenance_only": span_provenance_summary,
        },
        "recurrence_class_quotient": {
            "class_key": [
                "claim_type",
                "verbatim_span (canonicalized)",
                "opacity_status",
                "evaluated_axes",
                "omitted_axes",
            ],
            "class_count": len(retained_classes),
            "within_class_pair_count": quotient_summary["total_pairs"],
            "pointwise_order_components": [
                "support_status",
                "opacity_status",
                "evaluated_axes",
                "omitted_axes (negative)",
            ],
            "summary": quotient_summary,
        },
        "confirmation": {
            "identity_coordinate_annihilation_confirmed": (
                span_provenance_summary["comparability_rate"] == 0.0
            ),
            "recurrence_class_quotient_restoration_confirmed": (
                quotient_summary["comparability_rate"] == 1.0
            ),
            "conservative_resolution_gate": (
                span_provenance_summary["comparability_rate"] == 0.0
                and quotient_summary["comparability_rate"] == 1.0
            ),
            "homogeneity_caveat": homogeneity_caveat,
        },
    }


def build_markdown(report: dict[str, object]) -> str:
    return "\n".join(
        [
            "# Component Ablation Diagnostic",
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
            "## 2. Component Ablation",
            "",
            "```json",
            json.dumps(report["component_ablation"], indent=2, ensure_ascii=False),
            "```",
            "",
            "## 3. Recurrence-Class Quotient",
            "",
            "```json",
            json.dumps(report["recurrence_class_quotient"], indent=2, ensure_ascii=False),
            "```",
            "",
            "## 4. Confirmation",
            "",
            "```json",
            json.dumps(report["confirmation"], indent=2, ensure_ascii=False),
            "```",
            "",
            "## 5. Readout",
            "",
            "```text",
            (
                "span/provenance-only comparability: "
                f"{report['component_ablation']['span_provenance_only']['comparability_rate']:.6f}"
            ),
            (
                "quotient within-class comparability: "
                f"{report['recurrence_class_quotient']['summary']['comparability_rate']:.4f} "
                f"over {report['recurrence_class_quotient']['within_class_pair_count']} pairs "
                f"in {report['recurrence_class_quotient']['class_count']} classes"
            ),
            report["confirmation"]["homogeneity_caveat"],
            "```",
            "",
        ]
    )


def main():
    report = build_report()
    (OUT_DIR / "ablation_report.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    (OUT_DIR / "ablation_report.md").write_text(
        build_markdown(report),
        encoding="utf-8",
    )
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
