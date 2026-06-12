# DME V2 - Claim Inventory (POPULATED, v2.2.1)

```text
status: grounding instrument / POPULATED
source_snapshot: theory-v2.2-registry-canon
extraction_method: extractor v0.3, deterministic pattern grammar
population_status: populated - derived record, append-only
ledger_file: claim_inventory.jsonl (canonical; this doc is a projection of it)
```

## 1. Run Summary

```text
prior_inventory: Grounding/v2_2/claim_inventory.jsonl
total_entries: 6008
counts_by_type: {'BL': 211, 'DEF': 804, 'DEP': 314, 'NC': 4654, 'OP': 25}
basis_strata: {'doctrine_occurrence': {'counts_by_type': {'BL': 211, 'DEF': 804, 'DEP': 314, 'NC': 3007, 'OP': 25}, 'total_entries': 4361, 'nc_unique_contents': 1666}, 'registry_canonical': {'counts_by_type': {'NC': 1647}, 'total_entries': 1647, 'nc_unique_contents': 1647}}
new_in_v2_2_1: 0
reclassified_basis: 1647
preserved: 4361
merged: 0
superseded: 0
strict_fcl_chain_validation: passed
```

## 2. Comparison Against v2.2

```text
total entries delta: +0  (6008 -> 6008)
BL delta:  +0
DEF delta: +0
DEP delta: +0
NC delta:  +0
OP delta:  +0
```

## 3. Chain Validation

```text
status: passed
chain: ['Grounding/v0_2/id_crosswalk.json', 'Grounding/v2_1/id_crosswalk.json', 'Grounding/v2_2/id_crosswalk.json', 'Grounding/v2_2_1/id_crosswalk.json']
ref_sections: {'FCL-001': 10, 'FCL-002': 13, 'FCL-003': 7}
dangling_refs: {}
```

## 4. Derivation Sanity

```json
{
  "registry_canonical": {
    "total_new_unique_contents": 1647,
    "files": [
      {
        "source_file": "Core/README.DME.V2.NonCollapseRegistry.md",
        "new_unique_contents": 1647,
        "share": 1.0,
        "flag_review": true,
        "expected_dominance": true,
        "warning_candidate": false
      }
    ]
  }
}
```
