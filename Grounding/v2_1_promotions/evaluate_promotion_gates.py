#!/usr/bin/env python3
"""Promotion-gate evaluation layer over the v2.1 inventory.

This is an instrument-layer operation only.
It records epistemic divergence in an overlay without mutating
the committed v2.1 claim inventory.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import re
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
OUT_DIR = Path(__file__).resolve().parent
SOURCE_SNAPSHOT = "theory-v2.1-grounded-canon"
PROMOTION_LAYER_VERSION = "full-admission-gate-v0.2"

CLAIM_INVENTORY = REPO / "Grounding" / "v2_1" / "claim_inventory.jsonl"
RECURRENCE_MAP = REPO / "Grounding" / "v2_1" / "recurrence_map.json"
RUN_MANIFEST = REPO / "Grounding" / "v2_1" / "run_manifest.json"
V0_2_CROSSWALK = REPO / "Grounding" / "v0_2" / "id_crosswalk.json"
V2_1_CROSSWALK = REPO / "Grounding" / "v2_1" / "id_crosswalk.json"
BASE_SUITE = REPO / "Grounding" / "v2_1_measurements" / "suite_report.json"
PROVISIONAL_ORDERS = REPO / "Grounding" / "v2_1_measurements" / "provisional_orders.md"
DOCTRINE = REPO / "Core" / "README.DME.V2.IdentityEnvelopeComposition.md"
FCL = REPO / "Core" / "README.DME.V2.FormalCorrespondenceLedger.md"
DERIVE_MODULE_PATH = REPO / "Grounding" / "v2_1" / "derive_v2_1.py"
GALOIS_MODULE_PATH = REPO / "Grounding" / "v2_1_measurements" / "run_provisional_galois_measurements.py"
SIZING_REPORT = REPO / "Grounding" / "v2_1_promotions" / "full_admission_gate_sizing_report.json"

PROMOTION_LEDGER = OUT_DIR / "promotion_ledger_v2.jsonl"
STATUS_OVERLAY = OUT_DIR / "status_overlay_v2.json"
PROMOTION_REPORT = OUT_DIR / "promotion_report_v2.md"
GALOIS_RERUN_JSON = OUT_DIR / "galois_rerun_report_v2.json"
GALOIS_RERUN_MD = OUT_DIR / "galois_rerun_report_v2.md"

STRUCT_TO_PARTIAL_HEADING = (
    "Promotion from structurally supported candidate to partially admitted distinction requires:"
)
STRUCT_TO_PARTIAL_REQUIREMENTS = [
    "at least one deterministic axis fully evaluated",
    "source span identified with exact provenance",
    "distinction type classified",
    "RecurrenceMap entry created",
]
FULLY_TO_LEDGER_HEADING = (
    "Promotion from fully admitted distinction to ledger-supported invariant requires:"
)
FULLY_TO_LEDGER_REQUIREMENTS = [
    "recorded reconstruction path",
    "source-to-current representation trace",
    "ledgered provenance envelope",
    "declared loss / preservation status",
]
PARTIAL_TO_FULL_HEADING = (
    "Full Admission Gate (partially_admitted -> fully_admitted)"
)
PARTIAL_TO_FULL_REQUIREMENTS = [
    "multi-basis convergence across at least two distinct deterministic chart bases",
    "recurrence stability across at least two independent source locations",
    "no cross-basis contradiction inside the recurrence class",
    "deterministic completeness over axes evaluable for the claim type",
]
ODQ_7_TEXT = (
    "What are the declared conditions for promotion from partially_admitted "
    "to fully_admitted, and how do Proof-axis evaluation, feedback survival, "
    "recurrence stability, and reconstruction burden contribute to that "
    "promotion without collapsing support into authorization?"
)


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load module from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


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


def write_jsonl(path: Path, records: list[dict]):
    with path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_text(text: str) -> str:
    text = text.replace("\n", " ").strip().lower()
    text = re.sub(r"\s+", " ", text)
    return text


def now_iso() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def recurrence_entry_created(entry: dict, recurrence_map: dict) -> bool:
    terms = recurrence_map.get("terms", {})
    duplicate_nc = recurrence_map.get("duplicate_nc_laws", {})
    normalized_terms = entry.get("normalized_terms", [])
    if any(term in terms for term in normalized_terms):
        return True
    if entry["claim_type"] == "NC" and canonical_text(entry.get("verbatim_span", "")) in duplicate_nc:
        return True
    if entry.get("recurrence_refs"):
        return True
    return False


def exact_provenance_present(entry: dict) -> bool:
    return bool(
        entry.get("source_file")
        and isinstance(entry.get("line_range"), list)
        and len(entry["line_range"]) == 2
        and isinstance(entry.get("char_span"), list)
        and len(entry["char_span"]) == 2
        and entry.get("source_snapshot")
        and entry.get("verbatim_span")
    )


def deterministic_axis_evaluated(entry: dict) -> bool:
    return bool(entry.get("evaluated_axes"))


def distinction_type_classified(entry: dict) -> bool:
    return bool(entry.get("claim_type"))


def can_promote_struct_to_partial(entry: dict, recurrence_map: dict) -> tuple[bool, dict[str, bool]]:
    checks = {
        "at least one deterministic axis fully evaluated": deterministic_axis_evaluated(entry),
        "source span identified with exact provenance": exact_provenance_present(entry),
        "distinction type classified": distinction_type_classified(entry),
        "RecurrenceMap entry created": recurrence_entry_created(entry, recurrence_map),
    }
    return all(checks.values()), checks


def can_promote_fully_to_ledger(entry: dict) -> tuple[bool, dict[str, bool]]:
    text = (entry.get("verbatim_span") or "").lower()
    checks = {
        "recorded reconstruction path": bool(entry.get("section_context")) and "reconstruction" in text,
        "source-to-current representation trace": bool(entry.get("source_file")) and bool(entry.get("source_snapshot")),
        "ledgered provenance envelope": "Ledger" in entry.get("evaluated_axes", []),
        "declared loss / preservation status": ("loss" in text) or ("preserv" in text),
    }
    return all(checks.values()), checks


def build_def_subject_index(entries: list[dict]) -> dict[str, list[str]]:
    subjects = defaultdict(list)
    for entry in entries:
        if entry["claim_type"] != "DEF":
            continue
        terms = entry.get("normalized_terms", [])
        if terms:
            subjects[terms[0]].append(entry["claim_id"])
    return subjects


def build_nc_recurrence_classes(entries: list[dict]) -> dict[str, list[dict]]:
    classes = defaultdict(list)
    for entry in entries:
        if entry["claim_type"] == "NC":
            classes[canonical_text(entry.get("verbatim_span", ""))].append(entry)
    return classes


def deterministic_full_gate_coverage(entry: dict) -> bool:
    return {"Distinction", "Ledger"}.issubset(set(entry.get("evaluated_axes", [])))


def can_promote_partial_to_full(
    entry: dict,
    def_subjects: dict[str, list[str]],
    recurrence_classes: dict[str, list[dict]],
) -> tuple[bool, dict[str, bool], dict]:
    terms = entry.get("normalized_terms", [])
    class_entries = recurrence_classes.get(canonical_text(entry.get("verbatim_span", "")), [entry])
    basis_convergence = (
        len(terms) >= 2
        and terms[0] in def_subjects
        and terms[1] in def_subjects
    )
    recurrence_stability = len({item["source_file"] for item in class_entries}) >= 2
    contradiction_free = not any(bool(item.get("context_sensitive", False)) for item in class_entries)
    deterministic_complete = deterministic_full_gate_coverage(entry)

    checks = {
        "multi-basis convergence": basis_convergence,
        "recurrence stability": recurrence_stability,
        "no cross-basis contradiction": contradiction_free,
        "deterministic completeness": deterministic_complete,
    }
    detail = {
        "basis_type_pair": ["pattern_basis", "definitional_basis"],
        "recurrence_source_locations": sorted({item["source_file"] for item in class_entries}),
        "recurrence_class_size": len(class_entries),
        "context_sensitive_in_class": any(bool(item.get("context_sensitive", False)) for item in class_entries),
        "claim_type_coverage": "implementable" if entry["claim_type"] == "NC" else "check_not_implementable",
    }
    return all(checks.values()), checks, detail


def axis_profile_distribution(entries: list[dict]) -> dict[str, int]:
    counts = Counter(tuple(entry.get("evaluated_axes", [])) for entry in entries)
    return {
        " | ".join(profile) if profile else "(none)": count
        for profile, count in sorted(counts.items(), key=lambda item: (len(item[0]), item[0]))
    }


def support_distribution(entries: list[dict]) -> dict[str, int]:
    return dict(sorted(Counter(entry.get("support_status") for entry in entries).items()))


def merge_entry(entry: dict, updates: dict) -> dict:
    merged = dict(entry)
    merged.update({key: value for key, value in updates.items() if key in {"support_status", "evaluated_axes", "omitted_axes"}})
    return merged


def build_overlay_updates(
    entries: list[dict],
    recurrence_map: dict,
    resolved_live_map: dict[str, dict],
) -> tuple[dict, list[dict], dict]:
    overlay_updates: dict[str, dict] = {}
    events: list[dict] = []
    not_eligible_struct = []
    not_eligible_partial = []
    not_eligible_fully = []
    blocked_counts = Counter()
    blocked_examples = []
    check_not_implementable = Counter()
    def_subjects = build_def_subject_index(entries)
    recurrence_classes = build_nc_recurrence_classes(entries)

    timestamp = now_iso()

    for claim_id, info in resolved_live_map.items():
        entry = info["entry"]
        updated_axes = sorted(set(entry.get("evaluated_axes", [])) | {"Proof"})
        updated_omitted = [axis for axis in entry.get("omitted_axes", []) if axis != "Proof"]
        overlay = overlay_updates.setdefault(claim_id, {})
        overlay["evaluated_axes"] = updated_axes
        overlay["omitted_axes"] = updated_omitted
        overlay.setdefault("overlay_basis_refs", [])
        overlay["overlay_basis_refs"] = sorted(set(overlay["overlay_basis_refs"]) | set(info["basis_refs"]))
        overlay.setdefault("overlay_reasons", [])
        overlay["overlay_reasons"] = sorted(set(overlay["overlay_reasons"]) | {"Proof-axis recording from FCL perturbation survival"})

        events.append(
            {
                "event_type": "axis_evaluation",
                "claim_id": claim_id,
                "axis": "Proof",
                "from_axes": entry.get("evaluated_axes", []),
                "to_axes": updated_axes,
                "basis_refs": info["basis_refs"],
                "gate_evaluated": "Proof-axis recording from FCL perturbation survival",
                "authorization_change": "none",
                "blocked_uses_change": "none",
                "timestamp": timestamp,
            }
        )

    for entry in entries:
        current_status = entry.get("support_status")
        claim_id = entry["claim_id"]

        if current_status == "structurally_supported":
            eligible, checks = can_promote_struct_to_partial(entry, recurrence_map)
            if eligible:
                overlay = overlay_updates.setdefault(claim_id, {})
                overlay["support_status"] = "partially_admitted"
                overlay.setdefault("overlay_reasons", [])
                overlay["overlay_reasons"] = sorted(set(overlay["overlay_reasons"]) | {"Declared promotion gate evaluation"})
                events.append(
                    {
                        "event_type": "status_promotion",
                        "claim_id": claim_id,
                        "from_status": "structurally_supported",
                        "to_status": "partially_admitted",
                        "gate_heading": STRUCT_TO_PARTIAL_HEADING,
                        "gate_requirements": STRUCT_TO_PARTIAL_REQUIREMENTS,
                        "gate_checks": checks,
                        "authorization_change": "none",
                        "blocked_uses_change": "none",
                        "timestamp": timestamp,
                    }
                )
            else:
                not_eligible_struct.append(
                    {
                        "claim_id": claim_id,
                        "failed_requirements": [name for name, passed in checks.items() if not passed],
                        "use_mention_flag": entry.get("use_mention_flag", "unknown"),
                        "context_sensitive": bool(entry.get("context_sensitive", False)),
                    }
                )

        elif current_status == "partially_admitted":
            if entry["claim_type"] != "NC":
                key = f"{entry['claim_type']}:partially_admitted->fully_admitted"
                check_not_implementable[key] += 1
                if len(blocked_examples) < 25:
                    blocked_examples.append(claim_id)
                events.append(
                    {
                        "event_type": "blocked",
                        "claim_id": claim_id,
                        "from_status": "partially_admitted",
                        "target_status": "fully_admitted",
                        "reason": "check_not_implementable",
                        "gate_heading": PARTIAL_TO_FULL_HEADING,
                        "note": "Full Admission Gate coverage is not implemented for this claim type; no promotion inferred.",
                        "claim_type": entry["claim_type"],
                        "authorization_change": "none",
                        "blocked_uses_change": "none",
                        "timestamp": timestamp,
                    }
                )
                continue

            eligible, checks, detail = can_promote_partial_to_full(
                entry,
                def_subjects,
                recurrence_classes,
            )
            if eligible:
                overlay = overlay_updates.setdefault(claim_id, {})
                overlay["support_status"] = "fully_admitted"
                overlay.setdefault("overlay_reasons", [])
                overlay["overlay_reasons"] = sorted(
                    set(overlay["overlay_reasons"])
                    | {"Full Admission Gate evaluation"}
                )
                events.append(
                    {
                        "event_type": "status_promotion",
                        "claim_id": claim_id,
                        "from_status": "partially_admitted",
                        "to_status": "fully_admitted",
                        "gate_heading": PARTIAL_TO_FULL_HEADING,
                        "gate_requirements": PARTIAL_TO_FULL_REQUIREMENTS,
                        "gate_checks": checks,
                        "gate_detail": detail,
                        "authorization_change": "none",
                        "blocked_uses_change": "none",
                        "timestamp": timestamp,
                    }
                )
            else:
                not_eligible_partial.append(
                    {
                        "claim_id": claim_id,
                        "failed_requirements": [name for name, passed in checks.items() if not passed],
                        "gate_detail": detail,
                        "use_mention_flag": entry.get("use_mention_flag", "unknown"),
                        "context_sensitive": bool(entry.get("context_sensitive", False)),
                    }
                )

        elif current_status == "fully_admitted":
            eligible, checks = can_promote_fully_to_ledger(entry)
            if eligible:
                overlay = overlay_updates.setdefault(claim_id, {})
                overlay["support_status"] = "ledger_supported"
                overlay.setdefault("overlay_reasons", [])
                overlay["overlay_reasons"] = sorted(set(overlay["overlay_reasons"]) | {"Declared promotion gate evaluation"})
                events.append(
                    {
                        "event_type": "status_promotion",
                        "claim_id": claim_id,
                        "from_status": "fully_admitted",
                        "to_status": "ledger_supported",
                        "gate_heading": FULLY_TO_LEDGER_HEADING,
                        "gate_requirements": FULLY_TO_LEDGER_REQUIREMENTS,
                        "gate_checks": checks,
                        "authorization_change": "none",
                        "blocked_uses_change": "none",
                        "timestamp": timestamp,
                    }
                )
            else:
                not_eligible_fully.append(
                    {
                        "claim_id": claim_id,
                        "failed_requirements": [name for name, passed in checks.items() if not passed],
                    }
                )

    return overlay_updates, events, {
        "not_eligible_structurally_supported": not_eligible_struct,
        "not_eligible_partially_admitted": not_eligible_partial,
        "not_eligible_fully_admitted": not_eligible_fully,
        "blocked_counts": dict(blocked_counts),
        "blocked_examples": blocked_examples,
        "check_not_implementable": dict(check_not_implementable),
    }


def resolve_fcl_claims(entries: list[dict], derive_module) -> dict:
    live_by_id = {entry["claim_id"]: entry for entry in entries}
    live_ids = set(live_by_id)
    crosswalks = [load_json(V0_2_CROSSWALK), load_json(V2_1_CROSSWALK)]
    ref_map = derive_module.parse_fcl_claim_cluster_refs()

    resolved_records = []
    unresolved = []
    resolved_live_map = {}
    for fcl_entry, refs in ref_map.items():
        for cited_id in refs:
            resolution = derive_module.resolve_ref_chain(cited_id, live_ids, crosswalks)
            if not resolution["valid"]:
                unresolved.append(
                    {
                        "fcl_entry": fcl_entry,
                        "claim_id": cited_id,
                        **resolution,
                    }
                )
                continue
            final_id = resolution["final_id"]
            live_entry = live_by_id[final_id]
            resolved_records.append(
                {
                    "fcl_entry": fcl_entry,
                    "cited_id": cited_id,
                    "live_id": final_id,
                    "chain": resolution["chain"],
                    "resolution_reason": resolution["reason"],
                    "source_file": live_entry["source_file"],
                    "claim_type": live_entry["claim_type"],
                    "line_range": live_entry["line_range"],
                    "support_status": live_entry["support_status"],
                }
            )
            info = resolved_live_map.setdefault(
                final_id,
                {
                    "entry": live_entry,
                    "basis_refs": [],
                    "cited_ids": [],
                },
            )
            info["basis_refs"].append(fcl_entry)
            info["cited_ids"].append(cited_id)

    if unresolved:
        raise SystemExit(
            "FCL chain-resolution validation failed: "
            + json.dumps(unresolved, ensure_ascii=False)
        )

    for info in resolved_live_map.values():
        info["basis_refs"] = sorted(set(info["basis_refs"]))
        info["cited_ids"] = sorted(set(info["cited_ids"]))

    overlap_live = sorted(
        claim_id for claim_id, info in resolved_live_map.items() if len(info["basis_refs"]) > 1
    )
    return {
        "total_fcl_cited_refs": sum(len(refs) for refs in ref_map.values()),
        "live_resolved_refs": len(resolved_records),
        "unresolved_refs": [],
        "resolved_records": resolved_records,
        "resolved_live_map": resolved_live_map,
        "section_counts": {key: len(value) for key, value in ref_map.items()},
        "section_live_counts": {
            section: len({record["live_id"] for record in resolved_records if record["fcl_entry"] == section})
            for section in ref_map
        },
        "overlap_live_ids": overlap_live,
    }


def build_status_overlay(
    overlay_updates: dict,
    fcl_resolution: dict,
    base_hash: str,
) -> dict:
    return {
        "source_snapshot": SOURCE_SNAPSHOT,
        "promotion_layer_version": PROMOTION_LAYER_VERSION,
        "base_inventory_path": "Grounding/v2_1/claim_inventory.jsonl",
        "base_inventory_sha256": base_hash,
        "generated_at": now_iso(),
        "update_count": len(overlay_updates),
        "fcl_live_claim_count": len(fcl_resolution["resolved_live_map"]),
        "updates": {
            claim_id: {
                key: value
                for key, value in sorted(update.items())
            }
            for claim_id, update in sorted(overlay_updates.items())
        },
    }


def base_and_overlay_entries(entries: list[dict], overlay_updates: dict) -> tuple[list[dict], list[dict]]:
    overlay_entries = []
    for entry in entries:
        overlay_entry = merge_entry(entry, overlay_updates.get(entry["claim_id"], {}))
        overlay_entries.append(overlay_entry)
    return entries, overlay_entries


def run_measurement(entries: list[dict], galois_module) -> dict:
    recurrence = load_json(RECURRENCE_MAP)
    run_manifest = load_json(RUN_MANIFEST)
    base_suite = load_json(BASE_SUITE)

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
        missing = [
            field
            for field in required_fields
            if field not in entry or entry[field] in ("", None, [])
        ]
        if missing:
            abstract_totality_missing[entry["claim_id"]] = missing
            continue

        try:
            profile = galois_module.alpha(entry)
            alpha_profiles[entry["claim_id"]] = profile
        except Exception as exc:  # pragma: no cover - defensive
            alpha_failures.append({"claim_id": entry.get("claim_id"), "error": str(exc)})
            continue

        try:
            envelope = galois_module.gamma(profile)
        except Exception as exc:  # pragma: no cover - defensive
            gamma_failures.append({"claim_id": entry["claim_id"], "error": str(exc)})
            continue

        reconstructed = galois_module.profile_of(envelope)
        relation = galois_module.abstract_profile_compare(reconstructed, profile)
        inflations = galois_module.component_inflations(reconstructed, profile)
        if relation == "right_leq_left" or inflations:
            composite_violations.append(
                {
                    "claim_id": entry["claim_id"],
                    "relation": relation,
                    "inflated_components": inflations,
                }
            )

        observed = galois_module.observed_concrete_profile(entry)
        concrete_profiles[entry["claim_id"]] = observed
        okay, failed_components = galois_module.observed_satisfies_required(observed, envelope)
        if not okay:
            unit_violations.append(
                {
                    "claim_id": entry["claim_id"],
                    "failed_components": failed_components,
                    "support_status": entry["support_status"],
                }
            )

        if entry.get("blocked_uses") and entry["support_status"] != "partially_admitted":
            if not entry.get("context_sensitive") and entry.get("use_mention_flag") == "asserted":
                deontic_lowering_violations.append(
                    {
                        "claim_id": entry["claim_id"],
                        "support_status": entry["support_status"],
                    }
                )

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
    pair_stats = galois_module.build_pair_stats(combined)

    return {
        "baseline": {
            "strict_suite_source_snapshot": base_suite["manifest"]["source_snapshot"],
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
        },
        "unit_soundness_proxy": {
            "total_entries": len(entries),
            "support_inflation_against_own_requirements": unit_violations,
            "violation_count": len(unit_violations),
        },
        "deontic_separation_check": {
            "blocked_uses_affects_support_status_violations": deontic_lowering_violations,
            "blocked_entry_count": sum(1 for entry in entries if entry.get("blocked_uses")),
        },
        "hashes": {
            "alpha_profiles_hash": galois_module.canonical_hash(alpha_profiles),
            "concrete_profiles_hash": galois_module.canonical_hash(concrete_profiles),
            "pair_stats_hash": galois_module.canonical_hash(pair_stats),
            "composite_results_hash": galois_module.canonical_hash(composite_violations),
            "unit_results_hash": galois_module.canonical_hash(unit_violations),
        },
    }


def product_relation_for_profiles(left: dict, right: dict, galois_module) -> str:
    relations = [
        galois_module.ordered_compare(left["support_status"], right["support_status"], galois_module.SUPPORT_ORDER),
        galois_module.ordered_compare(left["opacity_status"], right["opacity_status"], galois_module.OPACITY_ORDER),
        galois_module.subset_compare(set(left["evaluated_axes"]), set(right["evaluated_axes"])),
        galois_module.reverse_subset_compare(set(left["omitted_axes"]), set(right["omitted_axes"])),
    ]
    return galois_module.product_partial_compare(relations)


def content_class_stats(entries: list[dict], galois_module, fcl_live_ids: set[str]) -> dict:
    classes = defaultdict(list)
    for entry in entries:
        key = (entry["claim_type"], canonical_text(entry.get("verbatim_span", "")))
        classes[key].append(entry)

    comparable = Counter()
    affected = Counter()
    samples = []
    class_count = 0
    pair_count = 0
    for group in classes.values():
        if len(group) < 2:
            continue
        class_count += 1
        contains_fcl = any(entry["claim_id"] in fcl_live_ids for entry in group)
        for index, left in enumerate(group):
            for right in group[index + 1 :]:
                pair_count += 1
                relation = product_relation_for_profiles(left, right, galois_module)
                comparable[relation] += 1
                if contains_fcl:
                    affected[relation] += 1
                    if relation in {"left_leq_right", "right_leq_left"} and len(samples) < 15:
                        samples.append(
                            {
                                "left_claim_id": left["claim_id"],
                                "right_claim_id": right["claim_id"],
                                "relation": relation,
                            }
                        )
    return {
        "class_key": ["claim_type", "verbatim_span (canonicalized)"],
        "class_count": class_count,
        "pair_count": pair_count,
        "relations": {
            "equal": comparable["equal"],
            "left_leq_right": comparable["left_leq_right"],
            "right_leq_left": comparable["right_leq_left"],
            "incomparable": comparable["incomparable"],
        },
        "fcl_affected_relations": {
            "equal": affected["equal"],
            "left_leq_right": affected["left_leq_right"],
            "right_leq_left": affected["right_leq_left"],
            "incomparable": affected["incomparable"],
        },
        "fcl_affected_non_equal_comparable_pairs": samples,
    }


def recurrence_class_quotient_stats(entries: list[dict], galois_module) -> dict:
    classes = defaultdict(list)
    for entry in entries:
        key = (
            entry["claim_type"],
            canonical_text(entry.get("verbatim_span", "")),
            entry.get("opacity_status"),
            tuple(sorted(entry.get("evaluated_axes", []))),
            tuple(sorted(entry.get("omitted_axes", []))),
        )
        classes[key].append(entry)

    relations = Counter()
    class_count = 0
    pair_count = 0
    for group in classes.values():
        if len(group) < 2:
            continue
        class_count += 1
        for index, left in enumerate(group):
            for right in group[index + 1 :]:
                pair_count += 1
                relation = product_relation_for_profiles(left, right, galois_module)
                relations[relation] += 1
    return {
        "class_key": [
            "claim_type",
            "verbatim_span (canonicalized)",
            "opacity_status",
            "evaluated_axes",
            "omitted_axes",
        ],
        "class_count": class_count,
        "pair_count": pair_count,
        "relations": {
            "equal": relations["equal"],
            "left_leq_right": relations["left_leq_right"],
            "right_leq_left": relations["right_leq_left"],
            "incomparable": relations["incomparable"],
        },
    }


def build_galois_rerun_report(
    base_entries: list[dict],
    overlay_entries: list[dict],
    overlay_data: dict,
    fcl_resolution: dict,
    galois_module,
) -> dict:
    base_run = run_measurement(base_entries, galois_module)
    overlay_run_a = run_measurement(overlay_entries, galois_module)
    overlay_run_b = run_measurement(overlay_entries, galois_module)

    idempotence_confirmation = {
        "hash_equality": overlay_run_a["hashes"] == overlay_run_b["hashes"],
        "field_deltas": [] if overlay_run_a["abstract_order_totality_proxy"] == overlay_run_b["abstract_order_totality_proxy"] else ["abstract_order_totality_proxy"],
        "profile_deltas": [] if overlay_run_a["hashes"]["alpha_profiles_hash"] == overlay_run_b["hashes"]["alpha_profiles_hash"] else ["alpha_profiles_hash"],
        "order_comparison_deltas": [] if overlay_run_a["hashes"]["pair_stats_hash"] == overlay_run_b["hashes"]["pair_stats_hash"] else ["pair_stats_hash"],
        "run_a_hashes": overlay_run_a["hashes"],
        "run_b_hashes": overlay_run_b["hashes"],
    }
    overlay_run_a["idempotence_confirmation"] = idempotence_confirmation

    fcl_live_ids = set(fcl_resolution["resolved_live_map"])
    base_within = content_class_stats(base_entries, galois_module, fcl_live_ids)
    overlay_within = content_class_stats(overlay_entries, galois_module, fcl_live_ids)
    base_quotient = recurrence_class_quotient_stats(base_entries, galois_module)
    overlay_quotient = recurrence_class_quotient_stats(overlay_entries, galois_module)

    delta = {
        "non_inflation_violation_delta": (
            len(overlay_run_a["idempotence_noninflation_composite"]["violations"])
            - len(base_run["idempotence_noninflation_composite"]["violations"])
        ),
        "unit_soundness_violation_delta": (
            overlay_run_a["unit_soundness_proxy"]["violation_count"]
            - base_run["unit_soundness_proxy"]["violation_count"]
        ),
        "within_class_non_equal_comparable_delta": (
            overlay_within["relations"]["left_leq_right"]
            + overlay_within["relations"]["right_leq_left"]
            - base_within["relations"]["left_leq_right"]
            - base_within["relations"]["right_leq_left"]
        ),
        "quotient_non_equal_comparable_delta": (
            overlay_quotient["relations"]["left_leq_right"]
            + overlay_quotient["relations"]["right_leq_left"]
            - base_quotient["relations"]["left_leq_right"]
            - base_quotient["relations"]["right_leq_left"]
        ),
    }

    return {
        "manifest": {
            "source_snapshot": SOURCE_SNAPSHOT,
            "promotion_layer_version": PROMOTION_LAYER_VERSION,
            "base_inventory_sha256": sha256_file(CLAIM_INVENTORY),
            "status_overlay_sha256": sha256_file(STATUS_OVERLAY),
            "base_suite_sha256": sha256_file(BASE_SUITE),
            "sizing_report_sha256": sha256_file(SIZING_REPORT),
        },
        "overlay_summary": {
            "overlay_update_count": overlay_data["update_count"],
            "fcl_live_claim_count": overlay_data["fcl_live_claim_count"],
        },
        "base": {
            "idempotence_noninflation_composite": {
                "violation_count": len(base_run["idempotence_noninflation_composite"]["violations"]),
            },
            "unit_soundness_proxy": base_run["unit_soundness_proxy"],
            "within_class_comparability": base_within,
            "recurrence_class_quotient": base_quotient,
        },
        "overlay": {
            "idempotence_noninflation_composite": {
                "violation_count": len(overlay_run_a["idempotence_noninflation_composite"]["violations"]),
            },
            "unit_soundness_proxy": overlay_run_a["unit_soundness_proxy"],
            "idempotence_confirmation": overlay_run_a["idempotence_confirmation"],
            "within_class_comparability": overlay_within,
            "recurrence_class_quotient": overlay_quotient,
        },
        "delta": delta,
    }


def markdown_galois_rerun(report: dict) -> str:
    return "\n".join(
        [
            "# Galois Measurement Rerun Under Promotion Overlay",
            "",
            "```json",
            json.dumps(report["manifest"], indent=2, ensure_ascii=False),
            "```",
            "",
            "## 1. Base vs Overlay",
            "",
            "```json",
            json.dumps(
                {
                    "base": report["base"],
                    "overlay": report["overlay"],
                    "delta": report["delta"],
                },
                indent=2,
                ensure_ascii=False,
            ),
            "```",
            "",
        ]
    )


def choose_verdict(galois_rerun_report: dict, gate_summary: dict) -> str:
    overlay = galois_rerun_report["overlay"]
    if (
        overlay["idempotence_noninflation_composite"]["violation_count"] > 0
        or overlay["unit_soundness_proxy"]["violation_count"] > 0
        or not overlay["idempotence_confirmation"]["hash_equality"]
    ):
        return "instability found; report and halt"
    informative_pairs = (
        overlay["within_class_comparability"]["relations"]["left_leq_right"]
        + overlay["within_class_comparability"]["relations"]["right_leq_left"]
    )
    if informative_pairs > 0:
        return "divergence stable, FCL-002 verification advanced; FCL-003 can open"
    return "divergence stable but non-discriminating; hold FCL-003"


def markdown_promotion_report(
    base_entries: list[dict],
    overlay_entries: list[dict],
    base_hash: str,
    overlay_hash: str,
    fcl_resolution: dict,
    gate_summary: dict,
    overlay_updates: dict,
    galois_rerun_report: dict,
    sizing_report: dict,
) -> str:
    axis_before = axis_profile_distribution(base_entries)
    axis_after = axis_profile_distribution(overlay_entries)
    support_before = support_distribution(base_entries)
    support_after = support_distribution(overlay_entries)
    proof_count = len(fcl_resolution["resolved_live_map"])
    verdict = choose_verdict(galois_rerun_report, gate_summary)

    resolved_lines = [
        (
            f"{record['fcl_entry']}: {record['cited_id']} -> {record['live_id']} "
            f"({record['source_file']}:{record['line_range'][0]}-{record['line_range'][1]})"
        )
        for record in fcl_resolution["resolved_records"]
    ]

    return "\n".join(
        [
            "# Full Admission Gate Promotion Evaluation",
            "",
            "## 1. Source Anchor",
            "",
            "```text",
            f"source_snapshot: {SOURCE_SNAPSHOT}",
            f"v2_1_inventory_sha256: {base_hash}",
            f"status_overlay_sha256: {overlay_hash}",
            "```",
            "",
            "## 2. FCL Chain Resolution",
            "",
            "```text",
            f"total FCL-cited refs: {fcl_resolution['total_fcl_cited_refs']}",
            f"live resolved refs: {fcl_resolution['live_resolved_refs']}",
            f"unresolved refs: {len(fcl_resolution['unresolved_refs'])}",
            f"section counts: {fcl_resolution['section_counts']}",
            f"section live counts: {fcl_resolution['section_live_counts']}",
            f"overlap live ids: {fcl_resolution['overlap_live_ids']}",
            "```",
            "",
            "Resolved claims:",
            "",
            "```text",
            *resolved_lines,
            "```",
            "",
            "## 3. Divergence Summary",
            "",
            "```text",
            f"axis profile distribution before overlay: {axis_before}",
            f"axis profile distribution after overlay:  {axis_after}",
            f"support/status distribution before overlay: {support_before}",
            f"support/status distribution after overlay:  {support_after}",
            f"overlay update count: {len(overlay_updates)}",
            "```",
            "",
            "## 4. FCL Proof-Axis Evaluation Summary",
            "",
            "```text",
            f"number of unique live FCL claims evaluated on Proof axis: {proof_count}",
            f"historical cited refs chain-resolved: {fcl_resolution['live_resolved_refs']}",
            f"FCL-001 unique live count: {fcl_resolution['section_live_counts'].get('FCL-001', 0)}",
            f"FCL-002 unique live count: {fcl_resolution['section_live_counts'].get('FCL-002', 0)}",
            f"overlap: {len(fcl_resolution['overlap_live_ids'])}",
            "```",
            "",
            "## 5. Gate Evaluation Summary",
            "",
            "```text",
            f"structurally_supported -> partially_admitted promotions: {sum(1 for update in overlay_updates.values() if update.get('support_status') == 'partially_admitted')}",
            f"partially_admitted -> fully_admitted promotions: {sum(1 for update in overlay_updates.values() if update.get('support_status') == 'fully_admitted')}",
            f"structurally_supported -> partially_admitted not eligible: {len(gate_summary['not_eligible_structurally_supported'])}",
            f"partially_admitted -> fully_admitted not eligible: {len(gate_summary['not_eligible_partially_admitted'])}",
            f"fully_admitted -> ledger_supported not eligible: {len(gate_summary['not_eligible_fully_admitted'])}",
            f"check_not_implementable counts: {gate_summary['check_not_implementable']}",
            "```",
            "",
            "Not eligible examples:",
            "",
            "```json",
            json.dumps(
                {
                    "structurally_supported": gate_summary["not_eligible_structurally_supported"][:15],
                    "partially_admitted": gate_summary["not_eligible_partially_admitted"][:15],
                    "fully_admitted": gate_summary["not_eligible_fully_admitted"][:10],
                },
                indent=2,
                ensure_ascii=False,
            ),
            "```",
            "",
            "## 6. Full Admission Gate Sizing Anchor",
            "",
            "```text",
            f"definitional-basis convergence: {sizing_report['nc_gate_components']['definitional_basis_convergence']['count']} ({sizing_report['nc_gate_components']['definitional_basis_convergence']['share_of_nc']:.2%})",
            f"recurrence stability: {sizing_report['nc_gate_components']['recurrence_stability']['count']} ({sizing_report['nc_gate_components']['recurrence_stability']['share_of_nc']:.2%})",
            f"context-sensitive inversion flags: {sizing_report['nc_gate_components']['context_sensitive_inversion_flags']['count']}",
            f"full gate eligible: {sizing_report['nc_gate_components']['full_gate_eligible']['count']} ({sizing_report['nc_gate_components']['full_gate_eligible']['share_of_nc']:.2%})",
            f"check_not_implementable examples: {gate_summary['blocked_examples']}",
            "```",
            "",
            "## 7. Galois Rerun Summary",
            "",
            "```text",
            f"non-inflation violation delta: {galois_rerun_report['delta']['non_inflation_violation_delta']}",
            f"unit-soundness violation delta: {galois_rerun_report['delta']['unit_soundness_violation_delta']}",
            f"idempotence stable: {str(galois_rerun_report['overlay']['idempotence_confirmation']['hash_equality']).lower()}",
            f"within-class non-equal comparable delta: {galois_rerun_report['delta']['within_class_non_equal_comparable_delta']}",
            f"within-class non-equal comparable total: {galois_rerun_report['overlay']['within_class_comparability']['relations']['left_leq_right'] + galois_rerun_report['overlay']['within_class_comparability']['relations']['right_leq_left']}",
            f"quotient non-equal comparable delta: {galois_rerun_report['delta']['quotient_non_equal_comparable_delta']}",
            f"quotient non-equal comparable total: {galois_rerun_report['overlay']['recurrence_class_quotient']['relations']['left_leq_right'] + galois_rerun_report['overlay']['recurrence_class_quotient']['relations']['right_leq_left']}",
            f"FCL-affected non-equal comparable pairs: {galois_rerun_report['overlay']['within_class_comparability']['fcl_affected_non_equal_comparable_pairs']}",
            "```",
            "",
            "## 8. Verdict",
            "",
            "```text",
            verdict,
            "```",
            "",
        ]
    )


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    derive_module = load_module(DERIVE_MODULE_PATH, "dme_promotion_derive")
    galois_module = load_module(GALOIS_MODULE_PATH, "dme_promotion_galois")
    sizing_report = load_json(SIZING_REPORT)

    base_entries = load_jsonl(CLAIM_INVENTORY)
    recurrence_map = load_json(RECURRENCE_MAP)
    base_hash = sha256_file(CLAIM_INVENTORY)

    fcl_resolution = resolve_fcl_claims(base_entries, derive_module)
    overlay_updates, events, gate_summary = build_overlay_updates(
        base_entries,
        recurrence_map,
        fcl_resolution["resolved_live_map"],
    )

    overlay_data = build_status_overlay(overlay_updates, fcl_resolution, base_hash)
    STATUS_OVERLAY.write_text(
        json.dumps(overlay_data, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    overlay_hash = sha256_file(STATUS_OVERLAY)

    write_jsonl(PROMOTION_LEDGER, events)

    base_entries_for_compare, overlay_entries = base_and_overlay_entries(base_entries, overlay_updates)
    galois_rerun_report = build_galois_rerun_report(
        base_entries_for_compare,
        overlay_entries,
        overlay_data,
        fcl_resolution,
        galois_module,
    )
    GALOIS_RERUN_JSON.write_text(
        json.dumps(galois_rerun_report, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    GALOIS_RERUN_MD.write_text(
        markdown_galois_rerun(galois_rerun_report),
        encoding="utf-8",
    )

    PROMOTION_REPORT.write_text(
        markdown_promotion_report(
            base_entries_for_compare,
            overlay_entries,
            base_hash,
            overlay_hash,
            fcl_resolution,
            gate_summary,
            overlay_updates,
            galois_rerun_report,
            sizing_report,
        ),
        encoding="utf-8",
    )

    print(
        json.dumps(
            {
                "source_snapshot": SOURCE_SNAPSHOT,
                "promotion_layer_version": PROMOTION_LAYER_VERSION,
                "overlay_update_count": overlay_data["update_count"],
                "event_count": len(events),
                "fcl_live_claim_count": len(fcl_resolution["resolved_live_map"]),
                "fully_admitted_promotion_count": sum(
                    1 for update in overlay_updates.values() if update.get("support_status") == "fully_admitted"
                ),
                "check_not_implementable_count": sum(gate_summary["check_not_implementable"].values()),
                "verdict": choose_verdict(galois_rerun_report, gate_summary),
            },
            indent=2,
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
