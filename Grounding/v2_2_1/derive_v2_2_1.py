#!/usr/bin/env python3
"""Lawfully re-derive the claim inventory at theory-v2.2-registry-canon.

This wrapper applies extractor v0.3 to the already-anchored v2.2
source snapshot. The source tag is unchanged; this is an instrument
mutation with a required crosswalk link from v2_2 -> v2_2_1.
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
PRIOR_DIR = REPO / "Grounding" / "v2_2"
OUTPUT_DIR = REPO / "Grounding" / "v2_2_1"
EXTRACTOR_PATH = REPO / "Grounding" / "v0" / "extract_v0.py"
REGISTRY_SURFACE = "Core/README.DME.V2.NonCollapseRegistry.md"


def load_extractor_module():
    spec = importlib.util.spec_from_file_location("dme_v2_2_1_extract_wrapper", EXTRACTOR_PATH)
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


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


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
    for key in ("v0_2_id", "v2_1_id", "v2_2_id", "v2_2_1_id"):
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
        if status in {"superseded", "superseded_no_successor"}:
            return {
                "valid": False,
                "final_id": None,
                "chain": chain,
                "reason": status,
            }
        if target:
            current = target
            chain.append(current)
        if current in live_ids:
            return {"valid": True, "final_id": current, "chain": chain, "reason": status}

    if current in live_ids:
        return {"valid": True, "final_id": current, "chain": chain, "reason": "live_after_chain"}
    return {"valid": False, "final_id": None, "chain": chain, "reason": f"unresolved:{current}"}


def validate_fcl_chain(entries_new: list[dict], crosswalk_new: dict) -> dict:
    live_ids = {entry["claim_id"] for entry in entries_new}
    crosswalks = [
        load_json(REPO / "Grounding" / "v0_2" / "id_crosswalk.json"),
        load_json(REPO / "Grounding" / "v2_1" / "id_crosswalk.json"),
        load_json(PRIOR_DIR / "id_crosswalk.json"),
        crosswalk_new,
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
            "Grounding/v2_2_1/id_crosswalk.json",
        ],
    }


def split_crosswalk_records(crosswalk: dict):
    transition_map = {}
    new_entry_registry = {}
    for claim_id, info in crosswalk.items():
        if info.get("status") == "new_in_v2_2_1":
            new_entry_registry[claim_id] = info
        else:
            transition_map[claim_id] = info
    return transition_map, new_entry_registry


def assign_stable_ids(module, entries_new: list[dict], entries_old: list[dict]):
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
            "status": "superseded",
            "v2_2_1_id": None,
            "reason": "No deterministic v2.2.1 successor matched on source_file, claim_type, overlap, or content identity.",
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
            if top_score[0] > 0:
                matched_old = [
                    candidate[1]
                    for candidate in candidates
                    if candidate[0][0] == top_score[0]
                    and candidate[1]["line_range"] == candidates[0][1]["line_range"]
                ]
            else:
                matched_old = [
                    candidate[1]
                    for candidate in candidates
                    if candidate[0][1] == top_score[1]
                    and candidate[0][2] == top_score[2]
                    and module.identity_text(candidate[1]) == module.identity_text(candidates[0][1])
                    and (candidate[0][1] > 0 or candidate[0][2] > 0)
                ]
            keeper = min(matched_old, key=lambda old: module.parse_claim_id(old["claim_id"])[1])
            entry["claim_id"] = keeper["claim_id"]
            consumed_old.add(keeper["claim_id"])

            old_basis = keeper.get("basis", "doctrine_occurrence")
            new_basis = entry.get("basis", "doctrine_occurrence")
            status = "reclassified_basis" if old_basis != new_basis else "preserved"
            reason = (
                f"Basis reclassified from {old_basis} to {new_basis} under registry-aware extraction."
                if status == "reclassified_basis"
                else "Deterministic v2.2.1 match preserved via source_file, claim_type, overlap, and content identity."
            )
            crosswalk[keeper["claim_id"]] = {
                "status": status,
                "v2_2_1_id": keeper["claim_id"],
                "reason": reason,
            }

            absorbed = []
            for old in matched_old:
                if old["claim_id"] == keeper["claim_id"]:
                    continue
                consumed_old.add(old["claim_id"])
                absorbed.append(old["claim_id"])
                crosswalk[old["claim_id"]] = {
                    "status": "merged",
                    "v2_2_1_id": keeper["claim_id"],
                    "reason": f"Merged into {keeper['claim_id']} after deterministic overlap/content-identity match.",
                }
            if absorbed:
                entry["supersedes"] = absorbed
        else:
            claim_type = entry["claim_type"]
            next_serial[claim_type] += 1
            entry["claim_id"] = f"CLAIM-{claim_type}-{next_serial[claim_type]:04d}"
            crosswalk[entry["claim_id"]] = {
                "status": "new_in_v2_2_1",
                "v2_2_1_id": entry["claim_id"],
                "reason": "No prior v2.2 entry matched deterministically; allocated above the v2.2 type ceiling.",
                "source_file": entry["source_file"],
                "claim_type": entry["claim_type"],
                "basis": entry.get("basis", "doctrine_occurrence"),
            }

    return entries_new, crosswalk


def content_identity_key(module, entry: dict):
    if entry.get("basis") == "registry_canonical":
        return (entry["claim_type"], entry.get("canonical_text_normalized", module.identity_text(entry)))
    if entry["claim_type"] == "NC":
        return (entry["claim_type"], module.identity_text(entry))
    return (entry["claim_type"], module.identity_text(entry), tuple(entry.get("normalized_terms", [])))


def basis_strata_summary(module, entries: list[dict]) -> dict:
    strata = defaultdict(list)
    for entry in entries:
        strata[entry.get("basis", "doctrine_occurrence")].append(entry)

    summary = {}
    for basis, bucket in sorted(strata.items()):
        counts = Counter(entry["claim_type"] for entry in bucket)
        nc_entries = [entry for entry in bucket if entry["claim_type"] == "NC"]
        unique_nc = len({module.identity_text(entry) for entry in nc_entries})
        summary[basis] = {
            "counts_by_type": dict(sorted(counts.items())),
            "total_entries": len(bucket),
            "nc_unique_contents": unique_nc,
        }
    return summary


def new_content_attribution_by_basis(module, entries: list[dict], transition_map: dict, new_entry_registry: dict) -> dict:
    tracked_ids = set(new_entry_registry)
    tracked_ids.update(
        claim_id
        for claim_id, info in transition_map.items()
        if info.get("status") == "reclassified_basis"
    )
    grouped = defaultdict(lambda: defaultdict(set))
    totals = Counter()
    for entry in entries:
        if entry["claim_id"] not in tracked_ids:
            continue
        basis = entry.get("basis", "doctrine_occurrence")
        key = content_identity_key(module, entry)
        grouped[basis][entry["source_file"]].add(key)
    result = {}
    for basis, file_map in grouped.items():
        total_unique = len({item for values in file_map.values() for item in values})
        files = []
        for source_file, content_keys in sorted(file_map.items()):
            count = len(content_keys)
            share = count / total_unique if total_unique else 0.0
            files.append(
                {
                    "source_file": source_file,
                    "new_unique_contents": count,
                    "share": share,
                    "flag_review": share > 0.10,
                    "expected_dominance": basis == "registry_canonical" and source_file == REGISTRY_SURFACE,
                    "warning_candidate": basis == "doctrine_occurrence" and source_file == REGISTRY_SURFACE and share > 0.10,
                }
            )
        result[basis] = {
            "total_new_unique_contents": total_unique,
            "files": files,
        }
    return result


def populated_summary(manifest: dict, prior_manifest: dict) -> str:
    counts = manifest["counts_by_type"]
    prior_counts = prior_manifest.get("counts_by_type", {})
    total_delta = manifest["total_entries"] - prior_manifest.get("total_entries", 0)
    lines = [
        "# DME V2 - Claim Inventory (POPULATED, v2.2.1)",
        "",
        "```text",
        "status: grounding instrument / POPULATED",
        f"source_snapshot: {SOURCE_SNAPSHOT}",
        "extraction_method: extractor v0.3, deterministic pattern grammar",
        "population_status: populated - derived record, append-only",
        "ledger_file: claim_inventory.jsonl (canonical; this doc is a projection of it)",
        "```",
        "",
        "## 1. Run Summary",
        "",
        "```text",
        "prior_inventory: Grounding/v2_2/claim_inventory.jsonl",
        f"total_entries: {manifest['total_entries']}",
        f"counts_by_type: {counts}",
        f"basis_strata: {manifest['basis_strata']}",
        f"new_in_v2_2_1: {manifest['id_counts']['new_in_v2_2_1']}",
        f"reclassified_basis: {manifest['id_counts']['reclassified_basis']}",
        f"preserved: {manifest['id_counts']['preserved']}",
        f"merged: {manifest['id_counts']['merged']}",
        f"superseded: {manifest['id_counts']['superseded']}",
        f"strict_fcl_chain_validation: {manifest['fcl_chain_validation']['status']}",
        "```",
        "",
        "## 2. Comparison Against v2.2",
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
        "## 3. Chain Validation",
        "",
        "```text",
        f"status: {manifest['fcl_chain_validation']['status']}",
        f"chain: {manifest['fcl_chain_validation']['crosswalk_chain']}",
        f"ref_sections: {manifest['fcl_chain_validation']['ref_sections']}",
        f"dangling_refs: {manifest['fcl_chain_validation']['dangling_refs']}",
        "```",
        "",
        "## 4. Derivation Sanity",
        "",
        "```json",
        json.dumps(manifest["new_content_attribution_by_basis"], indent=2, ensure_ascii=False),
        "```",
        "",
    ]
    return "\n".join(lines)


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
    entries_new, crosswalk = assign_stable_ids(module, module.raw_entries, prior_entries)
    entries_new.sort(key=lambda entry: (entry["claim_type"], module.parse_claim_id(entry["claim_id"])[1]))

    cross_document, duplicate_nc = module.build_recurrence(entries_new)
    relation_counts = Counter(
        entry.get("relation_type", "unspecified")
        for entry in entries_new
        if entry["claim_type"] == "DEP"
    )
    use_mention_counts = Counter(entry.get("use_mention_flag", "unknown") for entry in entries_new)
    transition_map, new_entry_registry = split_crosswalk_records(crosswalk)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(EXTRACTOR_PATH, OUTPUT_DIR / "extract_v0_3.py")

    chain_validation = validate_fcl_chain(entries_new, transition_map)
    if not chain_validation["passed"]:
        raise SystemExit(
            "v2.2.1 chain validation failed: "
            + json.dumps(chain_validation["dangling"], ensure_ascii=False)
        )

    id_counts = Counter(info["status"] for info in transition_map.values())
    id_counts["new_in_v2_2_1"] = len(new_entry_registry)
    prior_manifest = load_json(PRIOR_DIR / "run_manifest.json")
    basis_strata = basis_strata_summary(module, entries_new)
    new_content_attr = new_content_attribution_by_basis(module, entries_new, transition_map, new_entry_registry)
    doctrine_summary = basis_strata.get("doctrine_occurrence", {"counts_by_type": {}, "total_entries": 0, "nc_unique_contents": 0})
    registry_summary = basis_strata.get("registry_canonical", {"counts_by_type": {}, "total_entries": 0, "nc_unique_contents": 0})

    manifest = {
        "source_snapshot": SOURCE_SNAPSHOT,
        "extractor_version": module.EXTRACTOR_VERSION,
        "corpus_scope": {
            "included_dirs": module.INCLUDE_DIRS,
            "included_root_files": module.INCLUDE_ROOT_FILES,
            "excluded_dirs": module.EXCLUDE_DIRS,
            "n_files": len(corpus),
        },
        "counts_by_type": dict(sorted(Counter(entry["claim_type"] for entry in entries_new).items())),
        "total_entries": len(entries_new),
        "status_ceiling": "partially_admitted unless context/use_mention lowers support",
        "prior_inventory": "Grounding/v2_2/claim_inventory.jsonl",
        "id_crosswalk": "Grounding/v2_2_1/id_crosswalk.json",
        "new_entry_registry": "Grounding/v2_2_1/new_entry_registry.json",
        "id_counts": {
            "preserved": id_counts.get("preserved", 0),
            "merged": id_counts.get("merged", 0),
            "superseded": id_counts.get("superseded", 0),
            "reclassified_basis": id_counts.get("reclassified_basis", 0),
            "new_in_v2_2_1": id_counts.get("new_in_v2_2_1", 0),
        },
        "basis_strata": basis_strata,
        "doctrine_occurrence_summary": {
            "counts_by_type": doctrine_summary["counts_by_type"],
            "total_entries": doctrine_summary["total_entries"],
            "nc_unique_contents": doctrine_summary["nc_unique_contents"],
            "duplicate_nc_laws": len(duplicate_nc),
            "cross_entry_terms": len(cross_document),
        },
        "registry_canonical_summary": registry_summary,
        "dep_relation_counts": dict(sorted(relation_counts.items())),
        "use_mention_counts": dict(sorted(use_mention_counts.items())),
        "context_sensitive_entries": module.stats["context_sensitive_entries"],
        "new_content_attribution_by_basis": new_content_attr,
        "fcl_chain_validation": {
            "status": "passed" if chain_validation["passed"] else "failed",
            "crosswalk_chain": chain_validation["crosswalk_chain"],
            "ref_sections": chain_validation["ref_sections"],
            "dangling_refs": chain_validation["dangling"],
        },
        "recurrence_summary": {
            "cross_entry_terms": len(cross_document),
            "duplicate_nc_laws": len(duplicate_nc),
            "basis": "doctrine_occurrence_only",
        },
        "artifact_hashes": {},
    }

    write_jsonl(OUTPUT_DIR / "claim_inventory.jsonl", entries_new)
    with (OUTPUT_DIR / "recurrence_map.json").open("w", encoding="utf-8") as handle:
        json.dump(
            {
                "basis": "doctrine_occurrence_only",
                "terms": dict(sorted(cross_document.items(), key=lambda item: (-item[1]["count"], item[0]))),
                "duplicate_nc_laws": duplicate_nc,
            },
            handle,
            indent=1,
            ensure_ascii=False,
        )
    with (OUTPUT_DIR / "id_crosswalk.json").open("w", encoding="utf-8") as handle:
        json.dump(transition_map, handle, indent=2, ensure_ascii=False)
    with (OUTPUT_DIR / "new_entry_registry.json").open("w", encoding="utf-8") as handle:
        json.dump(new_entry_registry, handle, indent=2, ensure_ascii=False)
    with (OUTPUT_DIR / "run_manifest.json").open("w", encoding="utf-8") as handle:
        json.dump(manifest, handle, indent=2, ensure_ascii=False)
    with (OUTPUT_DIR / "ClaimInventory.POPULATED.v2_2_1.md").open("w", encoding="utf-8") as handle:
        handle.write(populated_summary(manifest, prior_manifest))

    manifest["artifact_hashes"] = {
        name: sha256_file(OUTPUT_DIR / name)
        for name in (
            "claim_inventory.jsonl",
            "recurrence_map.json",
            "run_manifest.json",
            "id_crosswalk.json",
            "new_entry_registry.json",
            "ClaimInventory.POPULATED.v2_2_1.md",
            "extract_v0_3.py",
        )
    }
    with (OUTPUT_DIR / "run_manifest.json").open("w", encoding="utf-8") as handle:
        json.dump(manifest, handle, indent=2, ensure_ascii=False)

    print(json.dumps(manifest, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
