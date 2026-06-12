#!/usr/bin/env python3
"""Run the strict derivation suite for theory-v2.2-registry-canon under extractor v0.3."""

from __future__ import annotations

import contextlib
import hashlib
import importlib.util
import io
import json
import shutil
import tempfile
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
SUITE_DIR = Path(__file__).resolve().parent
COMMITTED_DIR = REPO / "Grounding" / "v2_2_1"
DERIVE_PATH = REPO / "Grounding" / "v2_2_1" / "derive_v2_2_1.py"
CURRENT_SNAPSHOT = "theory-v2.2-registry-canon"
REGISTRY_SURFACE = "Core/README.DME.V2.NonCollapseRegistry.md"

OUTPUT_FILES = [
    "claim_inventory.jsonl",
    "recurrence_map.json",
    "run_manifest.json",
    "id_crosswalk.json",
    "new_entry_registry.json",
    "ClaimInventory.POPULATED.v2_2_1.md",
    "extract_v0_3.py",
]


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def canonical_json_hash(obj) -> str:
    payload = json.dumps(obj, sort_keys=True, ensure_ascii=False).encode("utf-8")
    return sha256_bytes(payload)


def snapshot_output_dir(path: Path) -> dict:
    missing = [name for name in OUTPUT_FILES if not (path / name).exists()]
    if missing:
        raise FileNotFoundError(f"Missing expected outputs in {path}: {missing}")
    manifest = load_json(path / "run_manifest.json")
    return {
        "path": path.as_posix(),
        "file_hashes": {name: sha256_file(path / name) for name in OUTPUT_FILES},
        "manifest_hash": canonical_json_hash(manifest),
        "manifest": manifest,
    }


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load module from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_derive_to(output_dir: Path) -> dict:
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    derive_module = load_module(DERIVE_PATH, "dme_v2_2_1_measure_derive")
    derive_module.OUTPUT_DIR = output_dir
    derive_module.SOURCE_SNAPSHOT = CURRENT_SNAPSHOT

    with contextlib.redirect_stdout(io.StringIO()):
        derive_module.main()

    return snapshot_output_dir(output_dir)


def attempt_strict_run(output_dir: Path) -> dict:
    try:
        snapshot = run_derive_to(output_dir)
        return {"status": "passed", "snapshot": snapshot, "error": None}
    except SystemExit as exc:
        return {"status": "blocked", "snapshot": None, "error": str(exc)}


def compare_snapshots(left: dict, right: dict) -> dict:
    return {
        "all_output_hashes_equal": left["file_hashes"] == right["file_hashes"],
        "file_hashes_equal": {
            name: left["file_hashes"][name] == right["file_hashes"][name]
            for name in OUTPUT_FILES
        },
        "manifest_hash_equal": left["manifest_hash"] == right["manifest_hash"],
    }


def build_derivation_sanity(manifest: dict) -> dict:
    attr = manifest["new_content_attribution_by_basis"]
    review_flags = []
    doctrine_warning_candidates = []
    for basis, info in attr.items():
        for file_info in info.get("files", []):
            if file_info.get("flag_review"):
                review_flags.append({"basis": basis, **file_info})
            if file_info.get("warning_candidate"):
                doctrine_warning_candidates.append({"basis": basis, **file_info})
    registry_expected = [
        item for item in review_flags
        if item["basis"] == "registry_canonical" and item["source_file"] == REGISTRY_SURFACE
    ]
    return {
        "threshold": 0.10,
        "review_flags": review_flags,
        "registry_expected_flags": registry_expected,
        "doctrine_warning_candidates": doctrine_warning_candidates,
        "status": "flagged" if review_flags else "clear",
    }


def markdown_suite(report: dict) -> str:
    return "\n".join(
        [
            "# v2.2.1 Strict Suite",
            "",
            "```text",
            f"source_snapshot: {report['manifest']['source_snapshot']}",
            f"committed_baseline: {report['manifest']['committed_baseline']}",
            f"strict_status: {report['strict_suite']['status']}",
            f"strict_error: {report['strict_suite']['error']}",
            f"chain_validation: {report['committed_manifest']['fcl_chain_validation']['status']}",
            f"crosswalk_chain: {report['committed_manifest']['fcl_chain_validation']['crosswalk_chain']}",
            "```",
            "",
            "## 1. Committed vs Rerun",
            "",
            "```json",
            json.dumps(report["committed_vs_rerun"], indent=2, ensure_ascii=False),
            "```",
            "",
            "## 2. Idempotence",
            "",
            "```json",
            json.dumps(report["rerun_a_vs_b"], indent=2, ensure_ascii=False),
            "```",
            "",
            "## 3. Derivation Sanity",
            "",
            "```json",
            json.dumps(report["derivation_sanity"], indent=2, ensure_ascii=False),
            "```",
            "",
        ]
    )


def markdown_sanity(report: dict) -> str:
    return "\n".join(
        [
            "# v2.2.1 Derivation Sanity",
            "",
            "```text",
            f"threshold: {report['threshold']:.0%} of new unique contents per basis",
            f"status: {report['status']}",
            f"registry_expected_flag_count: {len(report['registry_expected_flags'])}",
            f"doctrine_warning_candidate_count: {len(report['doctrine_warning_candidates'])}",
            "```",
            "",
            "```json",
            json.dumps(report, indent=2, ensure_ascii=False),
            "```",
            "",
        ]
    )


def main():
    committed = snapshot_output_dir(COMMITTED_DIR)
    with tempfile.TemporaryDirectory(prefix="dme_v2_2_1_strict_") as tmp_strict, tempfile.TemporaryDirectory(
        prefix="dme_v2_2_1_rerun_a_"
    ) as tmp_a, tempfile.TemporaryDirectory(prefix="dme_v2_2_1_rerun_b_") as tmp_b:
        strict_attempt = attempt_strict_run(Path(tmp_strict) / "v2_2_1")
        rerun_a = run_derive_to(Path(tmp_a) / "v2_2_1")
        rerun_b = run_derive_to(Path(tmp_b) / "v2_2_1")

    derivation_sanity = build_derivation_sanity(committed["manifest"])
    report = {
        "manifest": {
            "source_snapshot": CURRENT_SNAPSHOT,
            "committed_baseline": "Grounding/v2_2_1",
        },
        "strict_suite": strict_attempt,
        "committed_manifest": committed["manifest"],
        "committed_vs_rerun": compare_snapshots(committed, rerun_a),
        "rerun_a_vs_b": compare_snapshots(rerun_a, rerun_b),
        "derivation_sanity": derivation_sanity,
    }

    SUITE_DIR.mkdir(parents=True, exist_ok=True)
    (SUITE_DIR / "suite_report.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    (SUITE_DIR / "suite_report.md").write_text(markdown_suite(report), encoding="utf-8")
    (SUITE_DIR / "derivation_sanity_report.json").write_text(
        json.dumps(derivation_sanity, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    (SUITE_DIR / "derivation_sanity_report.md").write_text(
        markdown_sanity(derivation_sanity),
        encoding="utf-8",
    )
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
