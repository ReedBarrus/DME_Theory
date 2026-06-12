#!/usr/bin/env python3
"""Run the strict derivation suite for theory-v2.2-registry-canon."""

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
COMMITTED_DIR = REPO / "Grounding" / "v2_2"
DERIVE_PATH = REPO / "Grounding" / "v2_2" / "derive_v2_2.py"
CURRENT_SNAPSHOT = "theory-v2.2-registry-canon"

OUTPUT_FILES = [
    "claim_inventory.jsonl",
    "recurrence_map.json",
    "run_manifest.json",
    "id_crosswalk.json",
    "ClaimInventory.POPULATED.v2_2.md",
    "extract_v0_2.py",
]


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
        "evaluated_axes": entry.get("evaluated_axes", []),
        "omitted_axes": entry.get("omitted_axes", []),
    }


def snapshot_output_dir(path: Path) -> dict:
    missing = [name for name in OUTPUT_FILES if not (path / name).exists()]
    if missing:
        raise FileNotFoundError(f"Missing expected outputs in {path}: {missing}")

    entries = load_jsonl(path / "claim_inventory.jsonl")
    manifest = load_json(path / "run_manifest.json")
    projections = [entry_projection(entry) for entry in entries]
    projections.sort(key=lambda item: item["claim_id"])
    return {
        "path": path.as_posix(),
        "file_hashes": {name: sha256_file(path / name) for name in OUTPUT_FILES},
        "manifest_hash": canonical_json_hash(manifest),
        "projection_hash": canonical_json_hash(projections),
        "total_entries": len(entries),
        "counts_by_type": dict(sorted(Counter(entry["claim_type"] for entry in entries).items())),
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

    derive_module = load_module(DERIVE_PATH, "dme_v2_2_measure_derive")
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
        "projection_hash_equal": left["projection_hash"] == right["projection_hash"],
        "total_entries_equal": left["total_entries"] == right["total_entries"],
        "counts_by_type_equal": left["counts_by_type"] == right["counts_by_type"],
    }


def markdown_report(report: dict) -> str:
    return "\n".join(
        [
            "# v2.2 Strict Suite",
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
        ]
    )


def main():
    committed = snapshot_output_dir(COMMITTED_DIR)
    with tempfile.TemporaryDirectory(prefix="dme_v2_2_strict_") as tmp_strict, tempfile.TemporaryDirectory(
        prefix="dme_v2_2_rerun_a_"
    ) as tmp_a, tempfile.TemporaryDirectory(prefix="dme_v2_2_rerun_b_") as tmp_b:
        strict_attempt = attempt_strict_run(Path(tmp_strict) / "v2_2")
        rerun_a = run_derive_to(Path(tmp_a) / "v2_2")
        rerun_b = run_derive_to(Path(tmp_b) / "v2_2")

    report = {
        "manifest": {
            "source_snapshot": CURRENT_SNAPSHOT,
            "committed_baseline": "Grounding/v2_2",
        },
        "strict_suite": strict_attempt,
        "committed_manifest": committed["manifest"],
        "committed_vs_rerun": compare_snapshots(committed, rerun_a),
        "rerun_a_vs_b": compare_snapshots(rerun_a, rerun_b),
    }

    SUITE_DIR.mkdir(parents=True, exist_ok=True)
    (SUITE_DIR / "suite_report.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    (SUITE_DIR / "suite_report.md").write_text(markdown_report(report), encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
