# v2.2 Strict Suite

```text
source_snapshot: theory-v2.2-registry-canon
committed_baseline: Grounding/v2_2
strict_status: passed
strict_error: None
chain_validation: passed
crosswalk_chain: ['Grounding/v0_2/id_crosswalk.json', 'Grounding/v2_1/id_crosswalk.json', 'Grounding/v2_2/id_crosswalk.json']
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
    "ClaimInventory.POPULATED.v2_2.md": true,
    "extract_v0_2.py": true
  },
  "manifest_hash_equal": true,
  "projection_hash_equal": true,
  "total_entries_equal": true,
  "counts_by_type_equal": true
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
    "ClaimInventory.POPULATED.v2_2.md": true,
    "extract_v0_2.py": true
  },
  "manifest_hash_equal": true,
  "projection_hash_equal": true,
  "total_entries_equal": true,
  "counts_by_type_equal": true
}
```
