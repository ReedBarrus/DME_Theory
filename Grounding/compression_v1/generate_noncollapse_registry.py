#!/usr/bin/env python3
"""Generate the first governed non-collapse authority registry.

This is a deterministic authority-compression layer over the v2.1
inventory plus the v2.1 promotion overlay. It compresses authority
structure, not doctrine text.
"""

from __future__ import annotations

import hashlib
import json
import re
from collections import defaultdict
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
SOURCE_SNAPSHOT = "theory-v2.1-grounded-canon"
OUTPUT_SNAPSHOT = "theory-v2.2-registry-canon"

INPUT_INVENTORY = REPO / "Grounding" / "v2_1" / "claim_inventory.jsonl"
INPUT_OVERLAY = REPO / "Grounding" / "v2_1_promotions" / "status_overlay_v2.json"

OUTPUT_DIR = REPO / "Grounding" / "compression_v1"
REGISTRY_PATH = REPO / "Core" / "README.DME.V2.NonCollapseRegistry.md"
ENVELOPE_PATH = OUTPUT_DIR / "compression_envelope.md"
MANIFEST_PATH = OUTPUT_DIR / "registry_generation_manifest.json"
OPERATING_REPORT_PATH = OUTPUT_DIR / "operating_point_report.md"


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


def canonical_key(text: str) -> str:
    return re.sub(r"\s+", " ", text.replace("\n", " ").strip().lower())


def status_with_overlay(entry: dict, overlay_updates: dict) -> str:
    update = overlay_updates.get(entry["claim_id"], {})
    return update.get("support_status", entry.get("support_status", "unknown"))


def occurrence_sort_key(entry: dict):
    return (
        entry["source_file"],
        entry["line_range"][0],
        entry["line_range"][1],
        entry["claim_id"],
    )


def choose_canonical_instance(instances: list[dict], overlay_updates: dict) -> dict:
    ordered = sorted(instances, key=occurrence_sort_key)
    fully_admitted = [
        entry for entry in ordered
        if status_with_overlay(entry, overlay_updates) == "fully_admitted"
    ]
    return fully_admitted[0] if fully_admitted else ordered[0]


def build_registry_rows(entries: list[dict], overlay_updates: dict):
    classes = defaultdict(list)
    for entry in entries:
        if entry["claim_type"] != "NC":
            continue
        if entry.get("basis", "doctrine_occurrence") != "doctrine_occurrence":
            continue
        classes[canonical_key(entry.get("verbatim_span", ""))].append(entry)

    rows = []
    for key, instances in classes.items():
        ordered_instances = sorted(instances, key=occurrence_sort_key)
        canonical_instance = choose_canonical_instance(ordered_instances, overlay_updates)
        rows.append(
            {
                "key": key,
                "canonical_text": ordered_instances[0]["verbatim_span"],
                "instances": len(ordered_instances),
                "scale_band": ordered_instances[0].get("scale_band", "sentence/doctrine_law").replace("/", " / "),
                "canonical_home": canonical_instance["source_file"],
                "canonical_claim_id": canonical_instance["claim_id"],
                "instance_refs": [entry["claim_id"] for entry in ordered_instances],
                "fully_admitted": status_with_overlay(canonical_instance, overlay_updates) == "fully_admitted",
                "first_occurrence": occurrence_sort_key(ordered_instances[0]),
            }
        )

    rows.sort(key=lambda row: (-row["instances"], row["first_occurrence"]))
    return rows


def render_registry(rows: list[dict]) -> str:
    lines = [
        "# DME V2 - Non-Collapse Registry",
        "",
        "```text",
        "status: derived canonical layer / governed compression registry / generated projection",
        f"source_snapshot: {SOURCE_SNAPSHOT}",
        f"output_snapshot: {OUTPUT_SNAPSHOT}",
        "input_inventory: Grounding/v2_1/claim_inventory.jsonl",
        "input_overlay: Grounding/v2_1_promotions/status_overlay_v2.json",
        "compression_envelope: Grounding/compression_v1/compression_envelope.md",
        "operation: operating point A - authority compression",
        "generation_rule: one entry per unique NC content, ordered by instance count descending then first occurrence",
        "canonicality_rule: first fully_admitted occurrence if present; otherwise first occurrence",
        "```",
        "",
        "This document is a derived canonical layer generated from the tagged inventory.",
        "It compresses authority structure, not text.",
        "In-document occurrences remain in place as projections.",
        "Regeneration requires a new anchor and chain migration.",
        "",
        "## Non-Collapse",
        "",
        "```text",
        "registry entry != doctrine replacement",
        "canonical home != only valid location",
        "authority compression != text deletion",
        "registry != constitution",
        "```",
        "",
        "## Registry Entries",
        "",
    ]

    for index, row in enumerate(rows, start=1):
        lines.extend(
            [
                f"### NCR-{index:04d}",
                "",
                "```text",
                f"canonical_text: {row['canonical_text']}",
                f"instances: {row['instances']}",
                f"scale_band: {row['scale_band']}",
                f"canonical_home: {row['canonical_home']}",
                f"instance_refs: {', '.join(row['instance_refs'])}",
                f"fully_admitted: {'yes' if row['fully_admitted'] else 'no'}",
                "registry_status: canonical entry; in-document occurrences",
                "  are declared projections of this entry",
                "```",
                "",
            ]
        )

    return "\n".join(lines)


def build_manifest(rows: list[dict]) -> dict:
    singleton_count = sum(1 for row in rows if row["instances"] == 1)
    duplicated = [row for row in rows if row["instances"] > 1]
    peer_instance_count_before = sum(row["instances"] for row in duplicated)
    return {
        "input_inventory_sha256": sha256_file(INPUT_INVENTORY),
        "input_overlay_sha256": sha256_file(INPUT_OVERLAY),
        "generator_script_sha256": sha256_file(Path(__file__)),
        "generated_registry_sha256": sha256_file(REGISTRY_PATH),
        "entry_count_total": len(rows),
        "singleton_count": singleton_count,
        "duplicated_content_count": len(duplicated),
        "peer_instance_count_before": peer_instance_count_before,
        "canonical_entry_count_after": len(duplicated),
        "source_snapshot": SOURCE_SNAPSHOT,
        "output_snapshot": OUTPUT_SNAPSHOT,
    }


def build_operating_report(manifest: dict) -> str:
    total_nc = manifest["singleton_count"] + manifest["peer_instance_count_before"]
    projected_reduction = (
        (manifest["peer_instance_count_before"] - manifest["canonical_entry_count_after"]) / total_nc
        if total_nc else 0.0
    )
    return "\n".join(
        [
            "# First Governed Compression - Operating Point Report",
            "",
            "```text",
            "projected (FCL-003 sizing): 45% statement reduction at D=0",
            "realized (this operation): 0% statement reduction;",
            f"  authority structure compressed from {manifest['peer_instance_count_before']:,} peer instances",
            f"  to {manifest['canonical_entry_count_after']:,} canonical entries + projections (duplicated",
            "  contents); singleton contents registered without",
            "  compression",
            "delta explanation: the declared envelope contains a",
            "  section-role invariant the sizing measurement did not",
            "  price. Operating point B (byte reduction) remains",
            "  available per-document under future envelope declarations.",
            "finding: declared envelopes reveal invariants naive sizing",
            "  misses - first realized lesson of the fidelity criterion.",
            "ODQ-8 note: the declared loss here is vector-valued and",
            "  qualitative (authority axis only) - concrete pressure",
            "  for the quantitative-measure question, recorded not resolved.",
            f"measured duplicate-instance compression ratio: {projected_reduction:.2%}",
            "```",
            "",
        ]
    )


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    entries = load_jsonl(INPUT_INVENTORY)
    overlay = load_json(INPUT_OVERLAY)
    overlay_updates = overlay.get("updates", {})

    rows = build_registry_rows(entries, overlay_updates)
    REGISTRY_PATH.write_text(render_registry(rows), encoding="utf-8")

    manifest = build_manifest(rows)
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    OPERATING_REPORT_PATH.write_text(build_operating_report(manifest), encoding="utf-8")

    print(json.dumps(manifest, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
