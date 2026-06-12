#!/usr/bin/env python3
"""Run the extractor v0.2 idempotence + round-trip measurement suite.

This suite measures the current canonized snapshot
`theory-v2.1-grounded-canon` against the committed `Grounding/v2_1`
artifacts. It does not patch doctrine.
"""

from __future__ import annotations

import contextlib
import hashlib
import importlib.util
import io
import json
import shutil
import tempfile
from collections import Counter
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
SUITE_DIR = Path(__file__).resolve().parent
PRIOR_DIR = REPO / "Grounding" / "v0_2"
COMMITTED_DIR = REPO / "Grounding" / "v2_1"
EXTRACTOR_PATH = REPO / "Grounding" / "v0" / "extract_v0.py"
DERIVE_PATH = REPO / "Grounding" / "v2_1" / "derive_v2_1.py"
CURRENT_SNAPSHOT = "theory-v2.1-grounded-canon"

OUTPUT_FILES = [
    "claim_inventory.jsonl",
    "recurrence_map.json",
    "run_manifest.json",
    "id_crosswalk.json",
    "ClaimInventory.POPULATED.v2_1.md",
    "extract_v0_2.py",
]

SUPPORT_RANK = {
    "structurally_supported": 0,
    "partially_admitted": 1,
    "ledger_supported": 2,
    "feedback_tested": 3,
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


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


def canonical_json_hash(obj) -> str:
    payload = json.dumps(obj, sort_keys=True, ensure_ascii=False).encode("utf-8")
    return sha256_bytes(payload)


def entry_projection(entry: dict) -> dict:
    return {
        "claim_id": entry["claim_id"],
        "claim_type": entry["claim_type"],
        "source_file": entry["source_file"],
        "line_range": entry["line_range"],
        "verbatim_span": entry["verbatim_span"],
        "support_status": entry.get("support_status"),
        "opacity_status": entry.get("opacity_status"),
        "blocked_uses": sorted(entry.get("blocked_uses", [])),
        "use_mention_flag": entry.get("use_mention_flag"),
        "context_sensitive": bool(entry.get("context_sensitive", False)),
        "context_prefix": entry.get("context_prefix"),
        "evaluated_axes": entry.get("evaluated_axes", []),
        "omitted_axes": entry.get("omitted_axes", []),
        "extraction_method": entry.get("extraction_method"),
    }


def snapshot_output_dir(path: Path) -> dict:
    missing = [name for name in OUTPUT_FILES if not (path / name).exists()]
    if missing:
        raise FileNotFoundError(f"Missing expected outputs in {path}: {missing}")

    entries = load_jsonl(path / "claim_inventory.jsonl")
    manifest = load_json(path / "run_manifest.json")
    crosswalk = load_json(path / "id_crosswalk.json")
    recurrence = load_json(path / "recurrence_map.json")

    projections = [entry_projection(entry) for entry in entries]
    projections.sort(key=lambda item: item["claim_id"])

    support_counts = Counter(entry["support_status"] for entry in entries)
    opacity_counts = Counter(entry["opacity_status"] for entry in entries)
    use_counts = Counter(entry.get("use_mention_flag", "unknown") for entry in entries)
    blocked_entries = sorted(
        entry["claim_id"] for entry in entries if entry.get("blocked_uses")
    )
    context_sensitive_entries = sorted(
        entry["claim_id"] for entry in entries if entry.get("context_sensitive")
    )

    return {
        "path": path.as_posix(),
        "file_hashes": {name: sha256_file(path / name) for name in OUTPUT_FILES},
        "manifest": manifest,
        "manifest_hash": canonical_json_hash(manifest),
        "crosswalk_hash": canonical_json_hash(crosswalk),
        "recurrence_hash": canonical_json_hash(recurrence),
        "entry_projection_hash": canonical_json_hash(projections),
        "entries_by_id": {entry["claim_id"]: entry_projection(entry) for entry in entries},
        "counts_by_type": dict(sorted(Counter(entry["claim_type"] for entry in entries).items())),
        "support_counts": dict(sorted(support_counts.items())),
        "opacity_counts": dict(sorted(opacity_counts.items())),
        "use_mention_counts": dict(sorted(use_counts.items())),
        "blocked_entry_ids": blocked_entries,
        "context_sensitive_ids": context_sensitive_entries,
        "total_entries": len(entries),
    }


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load module from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_extractor_module():
    return load_module(EXTRACTOR_PATH, "dme_v2_1_measure_extractor")


def load_derive_module():
    return load_module(DERIVE_PATH, "dme_v2_1_measure_derive")


def build_chain_validate(derive_module):
    def chain_validate(entries_new, crosswalk_new):
        live_ids = {entry["claim_id"] for entry in entries_new}
        crosswalks = [
            load_json(PRIOR_DIR / "id_crosswalk.json"),
            crosswalk_new,
        ]
        ref_map = derive_module.parse_fcl_claim_cluster_refs()
        results = {}
        dangling = {}
        for fcl_id, refs in ref_map.items():
            for ref in refs:
                resolution = derive_module.resolve_ref_chain(ref, live_ids, crosswalks)
                results[ref] = resolution
                if not resolution["valid"]:
                    dangling.setdefault(fcl_id, []).append({"claim_id": ref, **resolution})
        return {
            "passed": not dangling,
            "dangling_fcl_refs": dangling,
            "results": results,
            "ref_sections": {key: len(value) for key, value in ref_map.items()},
        }

    return chain_validate


def run_extractor_to(output_dir: Path, *, strict: bool) -> dict:
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    derive_module = load_derive_module()
    derive_module.OUTPUT_DIR = output_dir
    derive_module.PRIOR_DIR = PRIOR_DIR
    derive_module.SOURCE_SNAPSHOT = CURRENT_SNAPSHOT

    with contextlib.redirect_stdout(io.StringIO()):
        derive_module.main()

    return snapshot_output_dir(output_dir)


def attempt_strict_run(output_dir: Path) -> dict:
    try:
        snapshot = run_extractor_to(output_dir, strict=True)
        return {"status": "passed", "snapshot": snapshot, "error": None}
    except SystemExit as exc:
        return {"status": "blocked", "snapshot": None, "error": str(exc)}


def compare_snapshots(left: dict, right: dict) -> dict:
    left_ids = set(left["entries_by_id"])
    right_ids = set(right["entries_by_id"])

    support_inflations = []
    support_demotions = []
    field_deltas = []
    for claim_id in sorted(left_ids & right_ids):
        left_entry = left["entries_by_id"][claim_id]
        right_entry = right["entries_by_id"][claim_id]
        left_rank = SUPPORT_RANK.get(left_entry["support_status"], -999)
        right_rank = SUPPORT_RANK.get(right_entry["support_status"], -999)
        if right_rank > left_rank:
            support_inflations.append(claim_id)
        elif right_rank < left_rank:
            support_demotions.append(claim_id)
        if left_entry != right_entry:
            changed_fields = sorted(
                key for key in left_entry.keys() if left_entry.get(key) != right_entry.get(key)
            )
            field_deltas.append({"claim_id": claim_id, "fields": changed_fields})

    return {
        "all_output_hashes_equal": left["file_hashes"] == right["file_hashes"],
        "file_hashes_equal": {
            name: left["file_hashes"][name] == right["file_hashes"][name]
            for name in OUTPUT_FILES
        },
        "entry_projection_hash_equal": left["entry_projection_hash"] == right["entry_projection_hash"],
        "manifest_hash_equal": left["manifest_hash"] == right["manifest_hash"],
        "crosswalk_hash_equal": left["crosswalk_hash"] == right["crosswalk_hash"],
        "recurrence_hash_equal": left["recurrence_hash"] == right["recurrence_hash"],
        "claim_id_sets_equal": left_ids == right_ids,
        "missing_in_right": sorted(left_ids - right_ids),
        "new_in_right": sorted(right_ids - left_ids),
        "support_inflations": support_inflations,
        "support_demotions": support_demotions,
        "field_delta_count": len(field_deltas),
        "field_delta_examples": field_deltas[:10],
        "blocked_entry_ids_equal": left["blocked_entry_ids"] == right["blocked_entry_ids"],
        "context_sensitive_ids_equal": left["context_sensitive_ids"] == right["context_sensitive_ids"],
        "counts_by_type_equal": left["counts_by_type"] == right["counts_by_type"],
        "support_counts_equal": left["support_counts"] == right["support_counts"],
        "use_mention_counts_equal": left["use_mention_counts"] == right["use_mention_counts"],
    }


def classify_odqs(committed: dict, committed_vs_a: dict, a_vs_b: dict) -> dict:
    odq4 = {
        "classification": "partially_measurable",
        "measurable_surfaces": [
            "The abstract-side carrier is observable in the inventory: support_status, opacity_status, blocked_uses, and evaluated/omitted axes are serialized fields.",
            f"Current v2.1 support-status distribution is measurable: {committed['support_counts']}.",
            f"Blocked-use divergence is measurable: {len(committed['blocked_entry_ids'])} entries carry blocked uses while remaining epistemically supported.",
        ],
        "blocked_surfaces": [
            "The doctrine still does not declare an order on admitted topology objects themselves.",
            "The doctrine still does not declare an order on hypothetical descriptions themselves beyond status ladders on statuses.",
            "Without declared concrete and abstract orders, monotonicity cannot be promoted from proxy observation to formal test.",
        ],
        "rationale": "ODQ-4 is partially measurable because the inventory exposes candidate carriers for the two domains, but canon still does not declare the domain orders themselves.",
    }

    odq5 = {
        "classification": "partially_measurable",
        "measurable_surfaces": [
            "Same-version idempotence is directly measurable as a fixed-point test over a fresh rerun pair.",
            "Status non-inflation is measurable as a counit-like proxy by comparing support_status across fresh reruns.",
            "Demotion preservation is measurable for context-sensitive and blocked-use entries because those annotations are serialized and comparable by claim_id.",
        ],
        "blocked_surfaces": [
            "Alpha and gamma are not declared as total monotone maps in doctrine.",
            "Unit (no-loss concretization round-trip) cannot be formally tested without a declared order on admitted topology.",
            "Counit can only be tested as a proxy fixed-point / non-inflation surface, not as an admitted adjunction law.",
        ],
        "rationale": "ODQ-5 is partially measurable because strict rerun idempotence and deflationary proxy behavior are testable now, while full unit/counit admission remains blocked by undeclared maps and orders.",
        "proxy_results": {
            "committed_vs_rerun_a_field_delta_count": committed_vs_a["field_delta_count"],
            "rerun_a_vs_rerun_b_field_delta_count": a_vs_b["field_delta_count"],
            "rerun_a_vs_rerun_b_support_inflations": len(a_vs_b["support_inflations"]),
        },
    }
    return {"ODQ-4": odq4, "ODQ-5": odq5}


def build_suite_report(committed: dict, strict_attempt: dict, rerun_a: dict, rerun_b: dict) -> dict:
    committed_vs_a = compare_snapshots(committed, rerun_a)
    a_vs_b = compare_snapshots(rerun_a, rerun_b)

    idempotence = {
        "classification": "measurable" if strict_attempt["status"] == "passed" else "blocked",
        "strict_current_corpus_rerun": {
            "classification": "measurable" if strict_attempt["status"] == "passed" else "blocked",
            "passed": strict_attempt["status"] == "passed",
            "error": strict_attempt["error"],
        },
        "committed_vs_rerun_a": committed_vs_a,
        "rerun_a_vs_rerun_b": a_vs_b,
        "passed": (
            strict_attempt["status"] == "passed"
            and committed_vs_a["all_output_hashes_equal"]
            and a_vs_b["all_output_hashes_equal"]
            and not committed_vs_a["support_inflations"]
            and not a_vs_b["support_inflations"]
        ),
    }

    round_trip_proxies = {
        "status_fixed_point": {
            "classification": "measurable",
            "passed": a_vs_b["entry_projection_hash_equal"] and committed_vs_a["entry_projection_hash_equal"],
            "evidence": {
                "committed_vs_rerun_a_field_delta_count": committed_vs_a["field_delta_count"],
                "rerun_a_vs_rerun_b_field_delta_count": a_vs_b["field_delta_count"],
            },
        },
        "counit_like_non_inflation": {
            "classification": "partially_measurable",
            "passed": not committed_vs_a["support_inflations"] and not a_vs_b["support_inflations"],
            "evidence": {
                "committed_vs_rerun_a_support_inflations": committed_vs_a["support_inflations"],
                "rerun_a_vs_rerun_b_support_inflations": a_vs_b["support_inflations"],
                "demoted_entry_count": len(committed["blocked_entry_ids"]),
                "context_sensitive_entry_count": len(committed["context_sensitive_ids"]),
            },
        },
        "unit_like_no_loss_of_admitted_structure": {
            "classification": "blocked",
            "passed": None,
            "reason": "No doctrine-declared gamma map or concrete order on admitted topology exists yet, so no-loss concretization cannot be formalized as a measurement.",
        },
    }

    return {
        "suite": {
            "name": "v0.2 idempotence + round-trip measurement suite",
            "source_snapshot": CURRENT_SNAPSHOT,
            "extractor_version": committed["manifest"]["extractor_version"],
            "committed_baseline": "Grounding/v2_1",
            "output_files_compared": OUTPUT_FILES,
        },
        "baseline": {
            "total_entries": committed["total_entries"],
            "counts_by_type": committed["counts_by_type"],
            "support_counts": committed["support_counts"],
            "opacity_counts": committed["opacity_counts"],
            "use_mention_counts": committed["use_mention_counts"],
            "blocked_entry_count": len(committed["blocked_entry_ids"]),
            "context_sensitive_entry_count": len(committed["context_sensitive_ids"]),
        },
        "idempotence": idempotence,
        "round_trip_proxies": round_trip_proxies,
        "odq_measurability": classify_odqs(committed, committed_vs_a, a_vs_b),
    }


def markdown_report(report: dict) -> str:
    lines = [
        "# v0.2 Idempotence + Round-Trip Measurement Suite",
        "",
        "```text",
        f"source_snapshot: {report['suite']['source_snapshot']}",
        f"extractor_version: {report['suite']['extractor_version']}",
        f"committed_baseline: {report['suite']['committed_baseline']}",
        "```",
        "",
        "## 1. Baseline",
        "",
        "```text",
        f"total_entries: {report['baseline']['total_entries']}",
        f"counts_by_type: {report['baseline']['counts_by_type']}",
        f"support_counts: {report['baseline']['support_counts']}",
        f"use_mention_counts: {report['baseline']['use_mention_counts']}",
        f"blocked_entry_count: {report['baseline']['blocked_entry_count']}",
        f"context_sensitive_entry_count: {report['baseline']['context_sensitive_entry_count']}",
        "```",
        "",
        "## 2. Idempotence",
        "",
        "```text",
        f"classification: {report['idempotence']['classification']}",
        f"passed: {str(report['idempotence']['passed']).lower()}",
        f"strict_current_corpus_rerun: {report['idempotence']['strict_current_corpus_rerun']['classification']}",
        f"strict_current_corpus_error: {report['idempotence']['strict_current_corpus_rerun']['error']}",
        f"committed_vs_rerun_a hashes equal: {str(report['idempotence']['committed_vs_rerun_a']['all_output_hashes_equal']).lower()}",
        f"rerun_a_vs_rerun_b hashes equal: {str(report['idempotence']['rerun_a_vs_rerun_b']['all_output_hashes_equal']).lower()}",
        f"committed_vs_rerun_a field deltas: {report['idempotence']['committed_vs_rerun_a']['field_delta_count']}",
        f"rerun_a_vs_rerun_b field deltas: {report['idempotence']['rerun_a_vs_rerun_b']['field_delta_count']}",
        "```",
        "",
        "## 3. Round-Trip Proxies",
        "",
    ]

    for name, result in report["round_trip_proxies"].items():
        lines.extend(
            [
                f"### {name}",
                "",
                "```text",
                f"classification: {result['classification']}",
                f"passed: {str(result['passed']).lower() if result['passed'] is not None else 'n/a'}",
            ]
        )
        if "reason" in result:
            lines.append(f"reason: {result['reason']}")
        if "evidence" in result:
            lines.append(f"evidence: {result['evidence']}")
        lines.extend(["```", ""])

    lines.extend(["## 4. ODQ Measurability", ""])
    for name, result in report["odq_measurability"].items():
        lines.extend(
            [
                f"### {name}",
                "",
                "```text",
                f"classification: {result['classification']}",
                f"rationale: {result['rationale']}",
                "measurable_surfaces:",
                *[f"  - {item}" for item in result["measurable_surfaces"]],
                "blocked_surfaces:",
                *[f"  - {item}" for item in result["blocked_surfaces"]],
            ]
        )
        if "proxy_results" in result:
            lines.append(f"proxy_results: {result['proxy_results']}")
        lines.extend(["```", ""])

    lines.extend(
        [
            "## 5. Verdict",
            "",
            "```text",
            f"ODQ-4: {report['odq_measurability']['ODQ-4']['classification']}",
            f"ODQ-5: {report['odq_measurability']['ODQ-5']['classification']}",
            "No doctrine patched in this suite.",
            "```",
            "",
        ]
    )
    return "\n".join(lines)


def main():
    SUITE_DIR.mkdir(parents=True, exist_ok=True)

    committed = snapshot_output_dir(COMMITTED_DIR)

    with tempfile.TemporaryDirectory(prefix="dme_v2_1_test_a_") as tmp_a, tempfile.TemporaryDirectory(
        prefix="dme_v2_1_test_b_"
    ) as tmp_b, tempfile.TemporaryDirectory(prefix="dme_v2_1_test_strict_") as tmp_strict:
        strict_attempt = attempt_strict_run(Path(tmp_strict) / "v2_1")
        rerun_a = run_extractor_to(Path(tmp_a) / "v2_1", strict=False)
        rerun_b = run_extractor_to(Path(tmp_b) / "v2_1", strict=False)

    report = build_suite_report(committed, strict_attempt, rerun_a, rerun_b)

    (SUITE_DIR / "suite_report.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    (SUITE_DIR / "suite_report.md").write_text(
        markdown_report(report),
        encoding="utf-8",
    )

    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
