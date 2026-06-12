#!/usr/bin/env python3
"""Provisional ODQ-4/5 measurement layer over the v2.1 inventory.

This is an instrument-layer measurement only.
It does not modify doctrine and does not admit the candidate
orders or maps as canon.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
OUT_DIR = Path(__file__).resolve().parent
SOURCE_SNAPSHOT = "theory-v2.1-grounded-canon"
MEASUREMENT_LAYER_VERSION = "provisional-galois-v0.1"

CLAIM_INVENTORY = REPO / "Grounding" / "v2_1" / "claim_inventory.jsonl"
RECURRENCE_MAP = REPO / "Grounding" / "v2_1" / "recurrence_map.json"
RUN_MANIFEST = REPO / "Grounding" / "v2_1" / "run_manifest.json"
ID_CROSSWALK = REPO / "Grounding" / "v2_1" / "id_crosswalk.json"
STRICT_SUITE = REPO / "Grounding" / "v0_2_tests" / "suite_report.json"
FCL_LEDGER = REPO / "Core" / "README.DME.V2.FormalCorrespondenceLedger.md"

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

LIVE_RESOLUTION_ORDER = {
    "unresolved": 0,
    "resolved_via_chain": 1,
    "live_direct": 2,
}

INPUT_PATHS = {
    "claim_inventory": CLAIM_INVENTORY,
    "recurrence_map": RECURRENCE_MAP,
    "run_manifest": RUN_MANIFEST,
    "id_crosswalk": ID_CROSSWALK,
    "strict_suite_report": STRICT_SUITE,
    "formal_correspondence_ledger": FCL_LEDGER,
}


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


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


def canonical_hash(obj) -> str:
    obj = to_jsonable(obj)
    return hashlib.sha256(
        json.dumps(obj, sort_keys=True, ensure_ascii=False).encode("utf-8")
    ).hexdigest()


def to_jsonable(obj):
    if isinstance(obj, dict):
        return {key: to_jsonable(value) for key, value in obj.items()}
    if isinstance(obj, list):
        return [to_jsonable(value) for value in obj]
    if isinstance(obj, set):
        return sorted(to_jsonable(value) for value in obj)
    return obj


def ordered_compare(left, right, mapping: dict) -> str:
    if left not in mapping or right not in mapping:
        return "incomparable"
    if mapping[left] == mapping[right]:
        return "equal"
    if mapping[left] < mapping[right]:
        return "left_leq_right"
    return "right_leq_left"


def subset_compare(left: set, right: set) -> str:
    if left == right:
        return "equal"
    if left.issubset(right):
        return "left_leq_right"
    if right.issubset(left):
        return "right_leq_left"
    return "incomparable"


def reverse_subset_compare(left: set, right: set) -> str:
    return subset_compare(right, left)


def span_specificity_compare(left: dict, right: dict) -> str:
    if left["source_file"] != right["source_file"]:
        return "incomparable"

    left_line = tuple(left["line_range"])
    right_line = tuple(right["line_range"])
    left_char = tuple(left["char_span"])
    right_char = tuple(right["char_span"])

    if left_line == right_line and left_char == right_char:
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
    if left_contains_right and not right_contains_left:
        return "left_leq_right"
    if right_contains_left and not left_contains_right:
        return "right_leq_left"
    return "incomparable"


def loss_compare(left: str, right: str) -> str:
    order = {"absent": 0, "declared": 1}
    return ordered_compare(left, right, order)


def product_partial_compare(component_relations: list[str]) -> str:
    if "incomparable" in component_relations:
        return "incomparable"
    strict_left = any(rel == "left_leq_right" for rel in component_relations)
    strict_right = any(rel == "right_leq_left" for rel in component_relations)
    if strict_left and strict_right:
        return "incomparable"
    if strict_left:
        return "left_leq_right"
    if strict_right:
        return "right_leq_left"
    return "equal"


def provenance_fields(entry: dict) -> set[str]:
    fields = set()
    if entry.get("source_file"):
        fields.add("source_file")
    line_range = entry.get("line_range")
    if isinstance(line_range, list) and len(line_range) == 2:
        fields.add("line_range")
    char_span = entry.get("char_span")
    if isinstance(char_span, list) and len(char_span) == 2:
        fields.add("char_span")
    if entry.get("source_snapshot"):
        fields.add("source_snapshot")
    if entry.get("verbatim_span"):
        fields.add("verbatim_span")
    if entry.get("section_context"):
        fields.add("section_context")
    return fields


def source_span_fields(entry: dict) -> set[str]:
    fields = set()
    if isinstance(entry.get("line_range"), list) and len(entry["line_range"]) == 2:
        fields.add("line_range")
    if isinstance(entry.get("char_span"), list) and len(entry["char_span"]) == 2:
        fields.add("char_span")
    if entry.get("verbatim_span"):
        fields.add("verbatim_span")
    return fields


def source_lineage(entry: dict) -> set[str]:
    lineage = set()
    if entry.get("source_snapshot"):
        lineage.add(f"snapshot:{entry['source_snapshot']}")
    if entry.get("source_file"):
        lineage.add(f"file:{entry['source_file']}")
    return lineage


def loss_decl_status(entry: dict) -> str:
    text = (entry.get("verbatim_span") or "").lower()
    if "loss" in text or "preserv" in text:
        return "declared"
    return "absent"


def live_resolution_status(entry: dict) -> str:
    return "live_direct"


def alpha(entry: dict) -> dict:
    return {
        "claim_id": entry["claim_id"],
        "claim_type": entry["claim_type"],
        "support_status": entry.get("support_status"),
        "opacity_status": entry.get("opacity_status"),
        "evaluated_axes": sorted(entry.get("evaluated_axes", [])),
        "omitted_axes": sorted(entry.get("omitted_axes", [])),
        "provenance_fields": sorted(provenance_fields(entry)),
        "source_span_fields": sorted(source_span_fields(entry)),
        "context_sensitive": bool(entry.get("context_sensitive", False)),
        "use_mention_flag": entry.get("use_mention_flag", "unknown"),
        "deontic_profile": {
            "blocked_uses": sorted(entry.get("blocked_uses", [])),
        },
    }


def gamma(profile: dict) -> dict:
    envelope = {
        "required_evaluated_axes": sorted(profile["evaluated_axes"]),
        "required_omitted_axes_upper_bound": sorted(profile["omitted_axes"]),
        "required_provenance_fields": sorted(profile["provenance_fields"]),
        "required_source_span_fields": sorted(profile["source_span_fields"]),
        "required_source_lineage": ["snapshot:" + SOURCE_SNAPSHOT],
        "required_loss_preservation_status": "absent",
        "required_context_sensitive_flag": profile["context_sensitive"],
        "required_use_mention_flag": profile["use_mention_flag"],
        "required_deontic_separation": bool(profile["deontic_profile"]["blocked_uses"]),
        "deontic_profile": {
            "blocked_uses": sorted(profile["deontic_profile"]["blocked_uses"]),
        },
        "required_support_status_ceiling": profile["support_status"],
        "required_opacity_status_ceiling": profile["opacity_status"],
    }
    return envelope


def profile_of(envelope: dict) -> dict:
    evaluated_axes = set(envelope["required_evaluated_axes"])
    omitted_axes = set(envelope["required_omitted_axes_upper_bound"])
    provenance = set(envelope["required_provenance_fields"])
    source_span = set(envelope["required_source_span_fields"])
    context_sensitive = bool(envelope["required_context_sensitive_flag"])
    use_mention_flag = envelope["required_use_mention_flag"]

    if context_sensitive or use_mention_flag != "asserted":
        support_status = "structurally_supported"
    elif {"Distinction", "Ledger"}.issubset(evaluated_axes) and {
        "source_file",
        "line_range",
        "char_span",
        "source_snapshot",
        "verbatim_span",
    }.issubset(provenance):
        support_status = "partially_admitted"
    else:
        support_status = "inferred_candidate"

    if {"Distinction", "Ledger"}.issubset(evaluated_axes) and provenance:
        opacity_status = "partially_supported"
    elif evaluated_axes:
        opacity_status = "candidate"
    else:
        opacity_status = "conjectural"

    return {
        "support_status": support_status,
        "opacity_status": opacity_status,
        "evaluated_axes": sorted(evaluated_axes),
        "omitted_axes": sorted(omitted_axes),
        "provenance_fields": sorted(provenance),
        "source_span_fields": sorted(source_span),
        "context_sensitive": context_sensitive,
        "use_mention_flag": use_mention_flag,
        "deontic_profile": {
            "blocked_uses": sorted(envelope["deontic_profile"]["blocked_uses"]),
        },
    }


def observed_concrete_profile(entry: dict) -> dict:
    return {
        "claim_id": entry["claim_id"],
        "claim_type": entry["claim_type"],
        "evaluated_axes": set(entry.get("evaluated_axes", [])),
        "omitted_axes": set(entry.get("omitted_axes", [])),
        "provenance_fields": provenance_fields(entry),
        "source_span_fields": source_span_fields(entry),
        "source_lineage": source_lineage(entry),
        "line_range": list(entry.get("line_range", [])),
        "char_span": list(entry.get("char_span", [])),
        "source_file": entry.get("source_file"),
        "loss_decl_status": loss_decl_status(entry),
        "live_resolution": live_resolution_status(entry),
        "blocked_uses": set(entry.get("blocked_uses", [])),
        "support_status": entry.get("support_status"),
        "opacity_status": entry.get("opacity_status"),
        "context_sensitive": bool(entry.get("context_sensitive", False)),
        "use_mention_flag": entry.get("use_mention_flag", "unknown"),
    }


def abstract_profile_compare(left: dict, right: dict) -> str:
    relations = [
        ordered_compare(left["support_status"], right["support_status"], SUPPORT_ORDER),
        ordered_compare(left["opacity_status"], right["opacity_status"], OPACITY_ORDER),
        subset_compare(set(left["evaluated_axes"]), set(right["evaluated_axes"])),
        subset_compare(set(left["provenance_fields"]) | set(left["source_span_fields"]),
                       set(right["provenance_fields"]) | set(right["source_span_fields"])),
        reverse_subset_compare(set(left["omitted_axes"]), set(right["omitted_axes"])),
    ]
    return product_partial_compare(relations)


def concrete_profile_compare(left: dict, right: dict) -> str:
    relations = [
        product_partial_compare([
            subset_compare(left["evaluated_axes"], right["evaluated_axes"]),
            reverse_subset_compare(left["omitted_axes"], right["omitted_axes"]),
        ]),
        subset_compare(left["provenance_fields"] | left["source_lineage"], right["provenance_fields"] | right["source_lineage"]),
        span_specificity_compare(left, right),
        loss_compare(left["loss_decl_status"], right["loss_decl_status"]),
        ordered_compare(left["live_resolution"], right["live_resolution"], LIVE_RESOLUTION_ORDER),
    ]
    return product_partial_compare(relations)


def observed_satisfies_required(observed: dict, required: dict) -> tuple[bool, list[str]]:
    failed = []
    if not set(required["required_evaluated_axes"]).issubset(observed["evaluated_axes"]):
        failed.append("required_evaluated_axes")
    if not set(required["required_provenance_fields"]).issubset(observed["provenance_fields"]):
        failed.append("required_provenance_fields")
    if not set(required["required_source_span_fields"]).issubset(observed["source_span_fields"]):
        failed.append("required_source_span_fields")
    if not set(required["required_source_lineage"]).issubset(observed["source_lineage"]):
        failed.append("required_source_lineage")
    if required["required_loss_preservation_status"] == "declared" and observed["loss_decl_status"] != "declared":
        failed.append("required_loss_preservation_status")
    if required["required_context_sensitive_flag"] and not observed["context_sensitive"]:
        failed.append("required_context_sensitive_flag")
    if required["required_use_mention_flag"] != observed["use_mention_flag"]:
        failed.append("required_use_mention_flag")
    if required["required_deontic_separation"] and not observed["blocked_uses"]:
        failed.append("required_deontic_separation")
    return (not failed, failed)


def component_inflations(reconstructed: dict, original: dict) -> list[str]:
    inflations = []
    if abstract_profile_compare(reconstructed, original) == "right_leq_left":
        if SUPPORT_ORDER[reconstructed["support_status"]] > SUPPORT_ORDER[original["support_status"]]:
            inflations.append("support_status")
        if OPACITY_ORDER[reconstructed["opacity_status"]] > OPACITY_ORDER[original["opacity_status"]]:
            inflations.append("opacity_status")
        if set(reconstructed["evaluated_axes"]) > set(original["evaluated_axes"]):
            inflations.append("evaluated_axes")
        if (set(reconstructed["provenance_fields"]) | set(reconstructed["source_span_fields"])) > (
            set(original["provenance_fields"]) | set(original["source_span_fields"])
        ):
            inflations.append("provenance/source_span")
        if set(reconstructed["omitted_axes"]) < set(original["omitted_axes"]):
            inflations.append("omitted_axes")
    return inflations


def build_pair_stats(entries: list[dict]) -> dict:
    stats = {
        "within_type": {"total_pairs": 0, "equal": 0, "left_leq_right": 0, "right_leq_left": 0, "incomparable": 0},
        "across_type": {"total_pairs": 0, "equal": 0, "left_leq_right": 0, "right_leq_left": 0, "incomparable": 0},
        "within_type_by_claim_type": defaultdict(lambda: {"total_pairs": 0, "equal": 0, "left_leq_right": 0, "right_leq_left": 0, "incomparable": 0}),
        "across_type_matrix": defaultdict(lambda: {"total_pairs": 0, "equal": 0, "left_leq_right": 0, "right_leq_left": 0, "incomparable": 0}),
    }
    n = len(entries)
    for i in range(n):
        left = entries[i]
        for j in range(i + 1, n):
            right = entries[j]
            relation = concrete_profile_compare(left["concrete"], right["concrete"])
            if left["claim_type"] == right["claim_type"]:
                bucket = stats["within_type"]
                per_type = stats["within_type_by_claim_type"][left["claim_type"]]
                bucket["total_pairs"] += 1
                bucket[relation] += 1
                per_type["total_pairs"] += 1
                per_type[relation] += 1
            else:
                key = f"{min(left['claim_type'], right['claim_type'])}-{max(left['claim_type'], right['claim_type'])}"
                bucket = stats["across_type"]
                per_pair = stats["across_type_matrix"][key]
                bucket["total_pairs"] += 1
                bucket[relation] += 1
                per_pair["total_pairs"] += 1
                per_pair[relation] += 1
    stats["within_type_by_claim_type"] = dict(stats["within_type_by_claim_type"])
    stats["across_type_matrix"] = dict(stats["across_type_matrix"])
    return stats


def manifest_block() -> dict:
    return {
        "source_snapshot": SOURCE_SNAPSHOT,
        "measurement_layer_version": MEASUREMENT_LAYER_VERSION,
        "inputs": {
            "claim_inventory_sha256": sha256_file(CLAIM_INVENTORY),
            "id_crosswalk_sha256": sha256_file(ID_CROSSWALK),
            "run_manifest_sha256": sha256_file(RUN_MANIFEST),
        },
    }


def run_once() -> dict:
    entries = load_jsonl(CLAIM_INVENTORY)
    recurrence = load_json(RECURRENCE_MAP)
    run_manifest = load_json(RUN_MANIFEST)
    strict_suite = load_json(STRICT_SUITE)

    alpha_profiles = {}
    concrete_profiles = {}
    abstract_totality_missing = defaultdict(list)
    alpha_failures = []
    gamma_failures = []
    composite_violations = []
    unit_violations = []
    deontic_lowering_violations = []

    for entry in entries:
        required_fields = [
            "claim_id",
            "claim_type",
            "support_status",
            "opacity_status",
            "evaluated_axes",
            "omitted_axes",
            "source_file",
            "line_range",
            "char_span",
            "source_snapshot",
            "verbatim_span",
        ]
        missing = [field for field in required_fields if field not in entry or entry[field] in ("", None, [])]
        if missing:
            abstract_totality_missing[entry["claim_id"]] = missing
            continue

        try:
            profile = alpha(entry)
            alpha_profiles[entry["claim_id"]] = profile
        except Exception as exc:  # pragma: no cover - defensive
            alpha_failures.append({"claim_id": entry.get("claim_id"), "error": str(exc)})
            continue

        try:
            envelope = gamma(profile)
        except Exception as exc:  # pragma: no cover - defensive
            gamma_failures.append({"claim_id": entry["claim_id"], "error": str(exc)})
            continue

        reconstructed = profile_of(envelope)
        rel = abstract_profile_compare(reconstructed, profile)
        inflations = component_inflations(reconstructed, profile)
        if rel == "right_leq_left" or inflations:
            composite_violations.append({
                "claim_id": entry["claim_id"],
                "relation": rel,
                "inflated_components": inflations,
                "original_profile": profile,
                "reconstructed_profile": reconstructed,
            })

        observed = observed_concrete_profile(entry)
        concrete_profiles[entry["claim_id"]] = observed
        okay, failed_components = observed_satisfies_required(observed, envelope)
        if not okay:
            unit_violations.append({
                "claim_id": entry["claim_id"],
                "failed_components": failed_components,
                "support_status": entry["support_status"],
            })

        if entry.get("blocked_uses") and entry["support_status"] != "partially_admitted":
            if not entry.get("context_sensitive") and entry.get("use_mention_flag") == "asserted":
                deontic_lowering_violations.append({
                    "claim_id": entry["claim_id"],
                    "support_status": entry["support_status"],
                    "blocked_uses": sorted(entry.get("blocked_uses", [])),
                })

    combined = [
        {
            "claim_id": entry["claim_id"],
            "claim_type": entry["claim_type"],
            "abstract": alpha_profiles[entry["claim_id"]],
            "concrete": concrete_profiles[entry["claim_id"]],
        }
        for entry in entries
        if entry["claim_id"] in alpha_profiles and entry["claim_id"] in concrete_profiles
    ]
    pair_stats = build_pair_stats(combined)

    entries_with_high_support_and_blocked_uses = [
        entry["claim_id"]
        for entry in entries
        if entry.get("blocked_uses") and entry.get("support_status") == "partially_admitted"
    ]
    deontic_constraints_only = [
        {
            "claim_id": entry["claim_id"],
            "support_status": entry["support_status"],
            "use_mention_flag": entry.get("use_mention_flag"),
            "context_sensitive": bool(entry.get("context_sensitive", False)),
        }
        for entry in entries
        if entry.get("blocked_uses")
    ]

    output = {
        "manifest": manifest_block(),
        "baseline": {
            "strict_suite_source_snapshot": strict_suite["suite"]["source_snapshot"],
            "inventory_total_entries": len(entries),
            "counts_by_type": run_manifest["counts_by_type"],
            "recurrence_term_count": len(recurrence.get("terms", {})),
            "duplicate_nc_law_count": len(recurrence.get("duplicate_nc_laws", {})),
        },
        "abstract_order_totality_proxy": {
            "total_entries": len(entries),
            "profile_assignment_successes": len(alpha_profiles),
            "missing_fields_count": len(abstract_totality_missing),
            "missing_fields": dict(abstract_totality_missing),
            "unclassifiable_entries": alpha_failures,
        },
        "concrete_order_partiality_proxy": {
            "within_type": pair_stats["within_type"],
            "across_type": pair_stats["across_type"],
            "within_type_by_claim_type": pair_stats["within_type_by_claim_type"],
            "across_type_matrix": pair_stats["across_type_matrix"],
        },
        "alpha_totality_proxy": {
            "total_entries": len(entries),
            "successes": len(alpha_profiles),
            "failures": alpha_failures,
        },
        "gamma_totality_proxy": {
            "total_profiles": len(alpha_profiles),
            "successes": len(alpha_profiles) - len(gamma_failures),
            "failures": gamma_failures,
        },
        "idempotence_noninflation_composite": {
            "total_profiles": len(alpha_profiles),
            "violations": composite_violations,
            "support_inflations": [v["claim_id"] for v in composite_violations if "support_status" in v["inflated_components"]],
            "opacity_inflations": [v["claim_id"] for v in composite_violations if "opacity_status" in v["inflated_components"]],
            "evaluated_axis_inflations": [v["claim_id"] for v in composite_violations if "evaluated_axes" in v["inflated_components"]],
            "provenance_inflations": [v["claim_id"] for v in composite_violations if "provenance/source_span" in v["inflated_components"]],
        },
        "unit_soundness_proxy": {
            "total_entries": len(entries),
            "support_inflation_against_own_requirements": unit_violations,
            "violation_count": len(unit_violations),
        },
        "deontic_separation_check": {
            "entries_with_high_support_and_blocked_uses": entries_with_high_support_and_blocked_uses,
            "entries_where_blocked_uses_remain_deontic_constraints_only": deontic_constraints_only[:50],
            "blocked_uses_affects_support_status_violations": deontic_lowering_violations,
            "blocked_entry_count": len(deontic_constraints_only),
        },
    }

    output["hashes"] = {
        "alpha_profiles_hash": canonical_hash(alpha_profiles),
        "concrete_profiles_hash": canonical_hash(concrete_profiles),
        "pair_stats_hash": canonical_hash(pair_stats),
        "composite_results_hash": canonical_hash(output["idempotence_noninflation_composite"]),
        "unit_results_hash": canonical_hash(output["unit_soundness_proxy"]),
    }
    return output


def classify_odqs(run_a: dict, run_b: dict) -> dict:
    within = run_a["concrete_order_partiality_proxy"]["within_type"]
    across = run_a["concrete_order_partiality_proxy"]["across_type"]
    total_within = max(within["total_pairs"], 1)
    total_across = max(across["total_pairs"], 1)
    within_incomparability_rate = within["incomparable"] / total_within
    across_incomparability_rate = across["incomparable"] / total_across

    odq4 = {
        "classification": "partially_measurable",
        "evidence": {
            "order_surfaces_measured": [
                "support_status chain",
                "opacity_status chain",
                "evaluated-axis coverage",
                "provenance/source-span completeness",
                "omitted-axis penalty",
                "axis-evaluation dominance",
                "provenance inclusion",
                "source-span specificity",
                "declared loss/preservation completeness",
                "live claim resolution through v2.1 inventory",
            ],
            "within_type_comparability_statistics": within,
            "across_type_comparability_statistics": across,
            "within_type_incomparability_rate": within_incomparability_rate,
            "across_type_incomparability_rate": across_incomparability_rate,
            "pointwise_order_behavior": {
                "within_type": {
                    "equal": within["equal"],
                    "left_leq_right": within["left_leq_right"],
                    "right_leq_left": within["right_leq_left"],
                    "incomparable": within["incomparable"],
                },
                "across_type": {
                    "equal": across["equal"],
                    "left_leq_right": across["left_leq_right"],
                    "right_leq_left": across["right_leq_left"],
                    "incomparable": across["incomparable"],
                },
            },
        },
        "blocked_surfaces": [
            "The abstract and concrete domain orders remain hypothetical topology only; they are not admitted doctrine.",
            "No canon-declared order on admitted topology objects exists yet.",
            "No canon-declared order on hypothetical descriptions themselves exists beyond status ladders over statuses.",
        ],
    }

    composite = run_a["idempotence_noninflation_composite"]
    unit_proxy = run_a["unit_soundness_proxy"]
    confirmation = run_a["idempotence_confirmation"]
    odq5 = {
        "classification": "partially_measurable",
        "evidence": {
            "idempotence_noninflation_composite_results": {
                "violation_count": len(composite["violations"]),
                "support_inflations": composite["support_inflations"],
                "opacity_inflations": composite["opacity_inflations"],
                "evaluated_axis_inflations": composite["evaluated_axis_inflations"],
                "provenance_inflations": composite["provenance_inflations"],
            },
            "unit_soundness_proxy_results": unit_proxy,
            "idempotence_confirmation_results": confirmation,
            "support_inflation_against_own_requirements": unit_proxy["support_inflation_against_own_requirements"],
        },
        "blocked_surfaces": [
            "alpha, gamma, and profile_of remain provisional measurement functions only.",
            "The counit proper is still undeclared in doctrine; this layer measures a provisional alpha-gamma-alpha composite only.",
            "The unit proper is still undeclared in doctrine; this layer measures a requirement-subset proxy only.",
        ],
    }
    return {"ODQ-4": odq4, "ODQ-5": odq5}


def build_provisional_orders_md(run_result: dict) -> str:
    return "\n".join([
        "# Provisional Orders and Maps",
        "",
        "```text",
        f"source_snapshot: {SOURCE_SNAPSHOT}",
        f"measurement_layer_version: {MEASUREMENT_LAYER_VERSION}",
        "status: hypothetical topology for measurement only",
        "doctrine_status: not admitted",
        "```",
        "",
        "## 1. Boundary",
        "",
        "This document defines candidate orders and maps for measuring ODQ-4 and ODQ-5 over the lawfully re-derived v2.1 inventory.",
        "",
        "These are hypothetical topology only.",
        "",
        "They do not declare doctrine.",
        "",
        "They do not admit a Galois connection.",
        "",
        "## 2. Order Convention",
        "",
        "Both candidate orders are pointwise product partial orders.",
        "",
        "```text",
        "Profile A <= Profile B iff A <= B on every component.",
        "higher = stronger epistemic grounding",
        "omitted axes count negatively",
        "scalar scoring, weighted sums, and rank aggregation are forbidden",
        "incomparability is a reported result, not a failure",
        "```",
        "",
        "## 3. Abstract-Side Candidate Order",
        "",
        "Components:",
        "",
        "```text",
        "support_status order",
        "opacity_status order",
        "evaluated-axis coverage order",
        "provenance/source-span completeness order",
        "omitted-axis penalty order",
        "```",
        "",
        "Component realizations in this layer:",
        "",
        "```text",
        "support_status: inferred_candidate < structurally_supported < partially_admitted < fully_admitted < ledger_supported < feedback_tested",
        "opacity_status: opaque < conjectural < candidate < partially_supported < fully_supported",
        "evaluated-axis coverage: stronger = superset",
        "provenance/source-span completeness: stronger = superset of present provenance/source-span fields",
        "omitted-axis penalty: stronger = subset of omitted axes",
        "```",
        "",
        "## 4. Concrete-Side Candidate Order",
        "",
        "Components:",
        "",
        "```text",
        "axis-evaluation dominance",
        "provenance inclusion",
        "source-span specificity",
        "declared loss / preservation completeness",
        "live claim resolution through the v2.1 inventory",
        "```",
        "",
        "Component realizations in this layer:",
        "",
        "```text",
        "axis-evaluation dominance: stronger = more evaluated axes and fewer omitted axes",
        "provenance inclusion: stronger = superset of provenance + source-lineage fields",
        "source-span specificity: stronger = narrower span within the same source file",
        "loss/preservation completeness: absent < declared",
        "live claim resolution: unresolved < resolved_via_chain < live_direct",
        "```",
        "",
        "## 5. Deontic Separation",
        "",
        "Blocked uses remain outside the epistemic orders.",
        "",
        "```text",
        "blocked_uses does not lower support_status",
        "blocked_uses is tracked as a separate deontic/use-authorization profile",
        "support and authorization are measured separately and never folded",
        "```",
        "",
        "## 6. Provisional Maps",
        "",
        "### alpha(entry)",
        "",
        "Maps a live v2.1 claim entry to an abstract admission profile containing:",
        "",
        "```text",
        "claim_id",
        "claim_type",
        "support_status",
        "opacity_status",
        "evaluated_axes",
        "omitted_axes",
        "provenance/source-span completeness",
        "context_sensitive flag",
        "use_mention flag",
        "deontic profile: blocked_uses only as authorization constraints",
        "```",
        "",
        "### gamma(profile)",
        "",
        "Maps an abstract admission profile to a required concrete evidence envelope containing:",
        "",
        "```text",
        "required evaluated axes",
        "required provenance/source-span fields",
        "required source lineage",
        "required loss/preservation declaration status",
        "required opacity/context annotations",
        "required blocked-use separation, if blocked uses exist",
        "```",
        "",
        "### profile_of(envelope)",
        "",
        "```text",
        "the strongest admission profile warranted by exactly that evidence envelope.",
        "```",
        "",
        "In this provisional layer, `profile_of` is treated as a candidate component of any future declared gamma structure.",
        "",
        "## 7. Current Measured Posture",
        "",
        "```text",
        f"total_entries: {run_result['baseline']['inventory_total_entries']}",
        f"blocked_entry_count: {run_result['deontic_separation_check']['blocked_entry_count']}",
        f"within_type_total_pairs: {run_result['concrete_order_partiality_proxy']['within_type']['total_pairs']}",
        f"across_type_total_pairs: {run_result['concrete_order_partiality_proxy']['across_type']['total_pairs']}",
        "```",
        "",
    ])


def build_suite_report_json() -> dict:
    run_a = run_once()
    run_b = run_once()

    confirmation = {
        "hash_equality": run_a["hashes"] == run_b["hashes"],
        "field_deltas": [] if run_a["abstract_order_totality_proxy"] == run_b["abstract_order_totality_proxy"] else ["abstract_order_totality_proxy"],
        "profile_deltas": [] if run_a["hashes"]["alpha_profiles_hash"] == run_b["hashes"]["alpha_profiles_hash"] else ["alpha_profiles_hash"],
        "order_comparison_deltas": [] if run_a["hashes"]["pair_stats_hash"] == run_b["hashes"]["pair_stats_hash"] else ["pair_stats_hash"],
        "run_a_hashes": run_a["hashes"],
        "run_b_hashes": run_b["hashes"],
    }
    run_a["idempotence_confirmation"] = confirmation
    odqs = classify_odqs(run_a, run_b)

    verdict = "ODQ-4/5 require more instrument work"

    ordered = {
        "manifest": run_a["manifest"],
        "baseline": run_a["baseline"],
        "abstract_order_totality_proxy": run_a["abstract_order_totality_proxy"],
        "concrete_order_partiality_proxy": run_a["concrete_order_partiality_proxy"],
        "alpha_totality_proxy": run_a["alpha_totality_proxy"],
        "gamma_totality_proxy": run_a["gamma_totality_proxy"],
        "idempotence_noninflation_composite": run_a["idempotence_noninflation_composite"],
        "unit_soundness_proxy": run_a["unit_soundness_proxy"],
        "idempotence_confirmation": run_a["idempotence_confirmation"],
        "deontic_separation_check": run_a["deontic_separation_check"],
        "odq_status_report": odqs,
        "summary_verdict": verdict,
    }
    return ordered


def build_suite_report_md(report: dict) -> str:
    manifest = report["manifest"]
    lines = [
        "# Provisional ODQ-4/5 Measurement Suite",
        "",
        "```json",
        json.dumps(manifest, indent=2),
        "```",
        "",
        "## 1. Baseline",
        "",
        "```text",
        f"strict_suite_source_snapshot: {report['baseline']['strict_suite_source_snapshot']}",
        f"inventory_total_entries: {report['baseline']['inventory_total_entries']}",
        f"counts_by_type: {report['baseline']['counts_by_type']}",
        f"recurrence_term_count: {report['baseline']['recurrence_term_count']}",
        f"duplicate_nc_law_count: {report['baseline']['duplicate_nc_law_count']}",
        "```",
        "",
        "## 2. Tests",
        "",
    ]

    for key in [
        "abstract_order_totality_proxy",
        "concrete_order_partiality_proxy",
        "alpha_totality_proxy",
        "gamma_totality_proxy",
        "idempotence_noninflation_composite",
        "unit_soundness_proxy",
        "idempotence_confirmation",
        "deontic_separation_check",
    ]:
        lines.extend([
            f"### {key}",
            "",
            "```json",
            json.dumps(report[key], indent=2, ensure_ascii=False),
            "```",
            "",
        ])

    lines.extend(["## 3. ODQ Status Report", ""])
    for odq in ["ODQ-4", "ODQ-5"]:
        lines.extend([
            f"### {odq}",
            "",
            "```json",
            json.dumps(report["odq_status_report"][odq], indent=2, ensure_ascii=False),
            "```",
            "",
        ])

    lines.extend([
        "## 4. Summary Verdict",
        "",
        "```text",
        report["summary_verdict"],
        "```",
        "",
    ])
    return "\n".join(lines)


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    report = build_suite_report_json()

    (OUT_DIR / "suite_report.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    (OUT_DIR / "suite_report.md").write_text(
        build_suite_report_md(report),
        encoding="utf-8",
    )
    (OUT_DIR / "provisional_orders.md").write_text(
        build_provisional_orders_md(report),
        encoding="utf-8",
    )

    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
