#!/usr/bin/env python3
"""Lawfully re-derive the claim inventory at theory-v2.2-registry-canon.

This wrapper reuses the v0.2 deterministic extractor logic without
changing its extraction semantics. It changes only the derivation
anchor, prior-inventory base, and validation chain needed for the
v2_1 -> v2_2 migration.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import re
import shutil
from collections import Counter, defaultdict
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
SOURCE_SNAPSHOT = "theory-v2.2-registry-canon"
PRIOR_DIR = REPO / "Grounding" / "v2_1"
OUTPUT_DIR = REPO / "Grounding" / "v2_2"
EXTRACTOR_PATH = REPO / "Grounding" / "v0" / "extract_v0.py"

ENTRY_ATTRIBUTION = {
    "noncollapse_registry": {
        "source_file": "Core/README.DME.V2.NonCollapseRegistry.md",
        "section_fragment": None,
    },
    "fcl003_operating_point_a": {
        "source_file": "Core/README.DME.V2.FormalCorrespondenceLedger.md",
        "section_fragment": "FCL-003 - Compression Admissibility",
    },
    "memory_index_registry_routes": {
        "source_file": "MEMORY_INDEX.md",
        "section_fragment": None,
    },
}


def load_extractor_module():
    spec = importlib.util.spec_from_file_location("dme_v2_2_extract_wrapper", EXTRACTOR_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load extractor from {EXTRACTOR_PATH}")
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


def write_jsonl(path: Path, records):
    with path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")


def parse_fcl_claim_cluster_refs():
    text = (REPO / "Core" / "README.DME.V2.FormalCorrespondenceLedger.md").read_text(
        encoding="utf-8", errors="replace"
    )
    headings = list(re.finditer(r"^### (FCL-\d+)\b.*$", text, flags=re.M))
    refs = defaultdict(list)
    for index, match in enumerate(headings):
        entry_name = match.group(1)
        start = match.start()
        end = headings[index + 1].start() if index + 1 < len(headings) else text.find("## 5. Queued Correspondences", start + 1)
        if end == -1:
            end = None
        segment = text[start:end]
        refs[entry_name] = sorted(set(re.findall(r"CLAIM-[A-Z]+-\d{4}", segment)))
    return refs


def resolve_target_id(info: dict) -> str | None:
    for key in ("v0_2_id", "v2_1_id", "v2_2_id"):
        if info.get(key):
            return info[key]
    for key, value in info.items():
        if key.endswith("_id") and value:
            return value
    return None


def resolve_ref_chain(claim_id: str, live_ids: set[str], crosswalks: list[dict]) -> dict:
    current = claim_id
    chain = [claim_id]
    if current in live_ids:
        return {"valid": True, "final_id": current, "chain": chain, "reason": "live_direct"}

    for crosswalk in crosswalks:
        info = crosswalk.get(current)
        if not info:
            return {
                "valid": False,
                "final_id": None,
                "chain": chain,
                "reason": f"missing_crosswalk_entry:{current}",
            }
        status = info.get("status")
        target = resolve_target_id(info)
        if status == "superseded_no_successor":
            return {
                "valid": False,
                "final_id": None,
                "chain": chain,
                "reason": "superseded_no_successor",
            }
        if target:
            current = target
            chain.append(current)
        if current in live_ids:
            return {"valid": True, "final_id": current, "chain": chain, "reason": status}

    if current in live_ids:
        return {"valid": True, "final_id": current, "chain": chain, "reason": "live_after_chain"}
    return {"valid": False, "final_id": None, "chain": chain, "reason": f"unresolved:{current}"}


def validate_fcl_chain(entries_v2_2: list[dict], crosswalk_v2_2: dict) -> dict:
    live_ids = {entry["claim_id"] for entry in entries_v2_2}
    crosswalks = [
        load_json(REPO / "Grounding" / "v0_2" / "id_crosswalk.json"),
        load_json(PRIOR_DIR / "id_crosswalk.json"),
        crosswalk_v2_2,
    ]
    ref_map = parse_fcl_claim_cluster_refs()
    results = {}
    dangling = {}
    for fcl_id, refs in ref_map.items():
        for ref in refs:
            resolution = resolve_ref_chain(ref, live_ids, crosswalks)
            results[ref] = resolution
            if not resolution["valid"]:
                dangling.setdefault(fcl_id, []).append({"claim_id": ref, **resolution})
    return {
        "passed": not dangling,
        "dangling": dangling,
        "results": results,
        "ref_sections": {key: len(value) for key, value in ref_map.items()},
        "crosswalk_chain": [
            "Grounding/v0_2/id_crosswalk.json",
            "Grounding/v2_1/id_crosswalk.json",
            "Grounding/v2_2/id_crosswalk.json",
        ],
    }


def assign_stable_ids_relaxed(module, entries_new: list[dict], entries_old: list[dict]):
    old_by_key = defaultdict(list)
    old_ceiling = defaultdict(int)
    for old in entries_old:
        key = (old["source_file"], old["claim_type"])
        old_by_key[key].append(old)
        claim_type, serial = module.parse_claim_id(old["claim_id"])
        old_ceiling[claim_type] = max(old_ceiling[claim_type], serial)

    next_serial = defaultdict(int, old_ceiling)
    for old_list in old_by_key.values():
        old_list.sort(key=lambda entry: entry["claim_id"])

    crosswalk = {
        old["claim_id"]: {
            "status": "superseded_no_successor",
            "v2_2_id": None,
            "reason": "No deterministic v2.2 successor matched on source_file, claim_type, overlap, or fallback verbatim/term similarity.",
        }
        for old in entries_old
    }
    consumed_old = set()

    indexed_entries = list(enumerate(entries_new))
    indexed_entries.sort(
        key=lambda item: (
            item[1]["claim_type"],
            item[1]["source_file"],
            -(item[1]["line_range"][1] - item[1]["line_range"][0]),
            item[1]["line_range"][0],
            item[1]["line_range"][1],
            item[0],
        )
    )

    def eligible(entry: dict, old: dict) -> bool:
        score = module.score_match(entry, old)
        overlap, verbatim_equal, shared_terms, _, _ = score
        return overlap > 0 or verbatim_equal > 0 or shared_terms > 0

    for _, entry in indexed_entries:
        key = (entry["source_file"], entry["claim_type"])
        candidates = []
        for old in old_by_key.get(key, []):
            if old["claim_id"] in consumed_old:
                continue
            if eligible(entry, old):
                candidates.append((module.score_match(entry, old), old))
        candidates.sort(key=lambda item: item[0], reverse=True)

        if candidates:
            top_score = candidates[0][0]
            matched_old = [
                candidate[1]
                for candidate in candidates
                if candidate[0] == top_score
                or (
                    candidate[0][1] == top_score[1]
                    and candidate[0][2] == top_score[2]
                    and (candidate[0][1] > 0 or candidate[0][2] > 0)
                )
            ]
            keeper = min(matched_old, key=lambda old: module.parse_claim_id(old["claim_id"])[1])
            entry["claim_id"] = keeper["claim_id"]
            consumed_old.add(keeper["claim_id"])
            crosswalk[keeper["claim_id"]] = {
                "status": "preserved",
                "v2_2_id": keeper["claim_id"],
                "reason": "Deterministic v2.2 match preserved via source_file, claim_type, and overlap/verbatim/term similarity.",
            }
            absorbed = []
            for old in matched_old:
                if old["claim_id"] == keeper["claim_id"]:
                    continue
                consumed_old.add(old["claim_id"])
                absorbed.append(old["claim_id"])
                crosswalk[old["claim_id"]] = {
                    "status": "merged_into",
                    "v2_2_id": keeper["claim_id"],
                    "reason": f"Merged into {keeper['claim_id']} after deterministic overlap/verbatim/term match.",
                }
            if absorbed:
                entry["supersedes"] = absorbed
        else:
            claim_type = entry["claim_type"]
            next_serial[claim_type] += 1
            entry["claim_id"] = f"CLAIM-{claim_type}-{next_serial[claim_type]:04d}"
            crosswalk[entry["claim_id"]] = {
                "status": "new_in_v2_2",
                "v2_2_id": entry["claim_id"],
                "reason": "No prior v2.1 entry matched deterministically; allocated above the v2.1 type ceiling.",
            }

    return entries_new, crosswalk


def new_entry_attribution(entries_v2_2: list[dict], crosswalk: dict) -> dict:
    new_ids = {
        claim_id
        for claim_id, info in crosswalk.items()
        if info.get("status") == "new_in_v2_2"
    }
    attribution = {key: 0 for key in ENTRY_ATTRIBUTION}
    unattributed = []
    for entry in entries_v2_2:
        if entry["claim_id"] not in new_ids:
            continue
        matched = False
        for key, rule in ENTRY_ATTRIBUTION.items():
            if entry["source_file"] != rule["source_file"]:
                continue
            fragment = rule["section_fragment"]
            if fragment and fragment not in entry.get("section_context", ""):
                continue
            attribution[key] += 1
            matched = True
            break
        if not matched:
            unattributed.append(entry["claim_id"])
    attribution["unattributed_new_entries"] = len(unattributed)
    attribution["unattributed_claim_ids"] = unattributed[:50]
    return attribution


def populated_summary(manifest: dict, prior_manifest: dict) -> str:
    counts = manifest["counts_by_type"]
    prior_counts = prior_manifest.get("counts_by_type", {})
    total_delta = manifest["total_entries"] - prior_manifest.get("total_entries", 0)
    lines = [
        "# DME V2 - Claim Inventory (POPULATED, v2.2)",
        "",
        "```text",
        "status: grounding instrument / POPULATED",
        f"source_snapshot: {SOURCE_SNAPSHOT}",
        "extraction_method: extractor v0.2, deterministic pattern grammar",
        "population_status: populated - derived record, append-only",
        "ledger_file: claim_inventory.jsonl (canonical; this doc is a projection of it)",
        "```",
        "",
        "## 1. Run Summary",
        "",
        "```text",
        "prior_inventory: Grounding/v2_1/claim_inventory.jsonl",
        f"total_entries: {manifest['total_entries']}",
        f"counts_by_type: {counts}",
        f"new_in_v2_2: {manifest['id_counts']['new_in_v2_2']}",
        f"preserved: {manifest['id_counts']['preserved']}",
        f"merged_into: {manifest['id_counts']['merged_into']}",
        f"superseded_no_successor: {manifest['id_counts']['superseded_no_successor']}",
        f"strict_fcl_chain_validation: {manifest['fcl_chain_validation']['status']}",
        "```",
        "",
        "## 2. Comparison Against v2.1",
        "",
        "```text",
        f"total entries delta: {total_delta:+d}  ({prior_manifest.get('total_entries', 0)} -> {manifest['total_entries']})",
        f"BL delta:  {counts.get('BL', 0) - prior_counts.get('BL', 0):+d}",
        f"DEF delta: {counts.get('DEF', 0) - prior_counts.get('DEF', 0):+d}",
        f"DEP delta: {counts.get('DEP', 0) - prior_counts.get('DEP', 0):+d}",
        f"NC delta:  {counts.get('NC', 0) - prior_counts.get('NC', 0):+d}",
        f"OP delta:  {counts.get('OP', 0) - prior_counts.get('OP', 0):+d}",
        "```",
        "",
        "## 3. New Entry Attribution",
        "",
        "```text",
        *[
            f"{key}: {value}"
            for key, value in manifest["new_entry_attribution"].items()
            if key != "unattributed_claim_ids"
        ],
        "```",
        "",
        "## 4. Chain Validation",
        "",
        "```text",
        f"status: {manifest['fcl_chain_validation']['status']}",
        f"chain: {manifest['fcl_chain_validation']['crosswalk_chain']}",
        f"ref_sections: {manifest['fcl_chain_validation']['ref_sections']}",
        f"dangling_refs: {manifest['fcl_chain_validation']['dangling_refs']}",
        "```",
        "",
    ]
    return "\n".join(lines)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    module = load_extractor_module()
    module.TAG = SOURCE_SNAPSHOT
    module.GROUNDING_V0 = REPO / "Grounding" / "v0_2"
    module.GROUNDING_V0_2 = OUTPUT_DIR
    module.raw_entries.clear()
    module.stats.clear()

    corpus = module.corpus_files()
    for source_file in corpus:
        module.parse_file(source_file)

    prior_entries = load_jsonl(PRIOR_DIR / "claim_inventory.jsonl")
    entries_v2_2, crosswalk = assign_stable_ids_relaxed(module, module.raw_entries, prior_entries)
    entries_v2_2.sort(key=lambda entry: (entry["claim_type"], module.parse_claim_id(entry["claim_id"])[1]))

    cross_document, duplicate_nc = module.build_recurrence(entries_v2_2)
    relation_counts = Counter(
        entry.get("relation_type", "unspecified")
        for entry in entries_v2_2
        if entry["claim_type"] == "DEP"
    )
    use_mention_counts = Counter(entry.get("use_mention_flag", "unknown") for entry in entries_v2_2)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(EXTRACTOR_PATH, OUTPUT_DIR / "extract_v0_2.py")

    chain_validation = validate_fcl_chain(entries_v2_2, crosswalk)
    if not chain_validation["passed"]:
        raise SystemExit(
            "v2.2 chain validation failed: "
            + json.dumps(chain_validation["dangling"], ensure_ascii=False)
        )

    id_counts = Counter(info["status"] for info in crosswalk.values())
    prior_manifest = load_json(PRIOR_DIR / "run_manifest.json")
    manifest = {
        "source_snapshot": SOURCE_SNAPSHOT,
        "extractor_version": module.EXTRACTOR_VERSION,
        "corpus_scope": {
            "included_dirs": module.INCLUDE_DIRS,
            "included_root_files": module.INCLUDE_ROOT_FILES,
            "excluded_dirs": module.EXCLUDE_DIRS,
            "n_files": len(corpus),
        },
        "counts_by_type": dict(sorted(Counter(entry["claim_type"] for entry in entries_v2_2).items())),
        "total_entries": len(entries_v2_2),
        "status_ceiling": "partially_admitted unless context/use_mention lowers support",
        "prior_inventory": "Grounding/v2_1/claim_inventory.jsonl",
        "id_crosswalk": "Grounding/v2_2/id_crosswalk.json",
        "id_counts": {
            "preserved": id_counts.get("preserved", 0),
            "merged_into": id_counts.get("merged_into", 0),
            "superseded_no_successor": id_counts.get("superseded_no_successor", 0),
            "new_in_v2_2": id_counts.get("new_in_v2_2", 0),
        },
        "dep_relation_counts": dict(sorted(relation_counts.items())),
        "use_mention_counts": dict(sorted(use_mention_counts.items())),
        "context_sensitive_entries": module.stats["context_sensitive_entries"],
        "new_entry_attribution": new_entry_attribution(entries_v2_2, crosswalk),
        "fcl_chain_validation": {
            "status": "passed" if chain_validation["passed"] else "failed",
            "crosswalk_chain": chain_validation["crosswalk_chain"],
            "ref_sections": chain_validation["ref_sections"],
            "dangling_refs": chain_validation["dangling"],
        },
        "recurrence_summary": {
            "cross_entry_terms": len(cross_document),
            "duplicate_nc_laws": len(duplicate_nc),
        },
        "artifact_hashes": {},
    }

    write_jsonl(OUTPUT_DIR / "claim_inventory.jsonl", entries_v2_2)
    with (OUTPUT_DIR / "recurrence_map.json").open("w", encoding="utf-8") as handle:
        json.dump(
            {
                "terms": dict(sorted(cross_document.items(), key=lambda item: (-item[1]["count"], item[0]))),
                "duplicate_nc_laws": duplicate_nc,
            },
            handle,
            indent=1,
            ensure_ascii=False,
        )
    with (OUTPUT_DIR / "id_crosswalk.json").open("w", encoding="utf-8") as handle:
        json.dump(crosswalk, handle, indent=2, ensure_ascii=False)
    with (OUTPUT_DIR / "run_manifest.json").open("w", encoding="utf-8") as handle:
        json.dump(manifest, handle, indent=2, ensure_ascii=False)
    with (OUTPUT_DIR / "ClaimInventory.POPULATED.v2_2.md").open("w", encoding="utf-8") as handle:
        handle.write(populated_summary(manifest, prior_manifest))

    manifest["artifact_hashes"] = {
        name: sha256_file(OUTPUT_DIR / name)
        for name in (
            "claim_inventory.jsonl",
            "recurrence_map.json",
            "run_manifest.json",
            "id_crosswalk.json",
            "ClaimInventory.POPULATED.v2_2.md",
            "extract_v0_2.py",
        )
    }
    with (OUTPUT_DIR / "run_manifest.json").open("w", encoding="utf-8") as handle:
        json.dump(manifest, handle, indent=2, ensure_ascii=False)

    print(json.dumps(manifest, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
