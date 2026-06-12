# v2.2.1 Strict Suite

```text
source_snapshot: theory-v2.2-registry-canon
committed_baseline: Grounding/v2_2_1
strict_status: passed
strict_error: None
chain_validation: passed
crosswalk_chain: ['Grounding/v0_2/id_crosswalk.json', 'Grounding/v2_1/id_crosswalk.json', 'Grounding/v2_2/id_crosswalk.json', 'Grounding/v2_2_1/id_crosswalk.json']
```

## 1. Committed vs Rerun

```json
{
  "all_output_hashes_equal": true,
  "file_hashes_equal": {
    "claim_inventory.jsonl": true,
    "recurrence_map.json": true,
    "run_manifest.json": true,
    "id_crosswalk.json": true,
    "new_entry_registry.json": true,
    "ClaimInventory.POPULATED.v2_2_1.md": true,
    "extract_v0_3.py": true
  },
  "manifest_hash_equal": true
}
```

## 2. Idempotence

```json
{
  "all_output_hashes_equal": true,
  "file_hashes_equal": {
    "claim_inventory.jsonl": true,
    "recurrence_map.json": true,
    "run_manifest.json": true,
    "id_crosswalk.json": true,
    "new_entry_registry.json": true,
    "ClaimInventory.POPULATED.v2_2_1.md": true,
    "extract_v0_3.py": true
  },
  "manifest_hash_equal": true
}
```

## 3. Derivation Sanity

```json
{
  "threshold": 0.1,
  "review_flags": [
    {
      "basis": "registry_canonical",
      "source_file": "Core/README.DME.V2.NonCollapseRegistry.md",
      "new_unique_contents": 1647,
      "share": 1.0,
      "flag_review": true,
      "expected_dominance": true,
      "warning_candidate": false
    }
  ],
  "registry_expected_flags": [
    {
      "basis": "registry_canonical",
      "source_file": "Core/README.DME.V2.NonCollapseRegistry.md",
      "new_unique_contents": 1647,
      "share": 1.0,
      "flag_review": true,
      "expected_dominance": true,
      "warning_candidate": false
    }
  ],
  "doctrine_warning_candidates": [],
  "status": "flagged"
}
```
