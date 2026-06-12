# DME V2 - Claim Inventory (POPULATED, v2.2)

```text
status: grounding instrument / POPULATED
source_snapshot: theory-v2.2-registry-canon
extraction_method: extractor v0.2, deterministic pattern grammar
population_status: populated - derived record, append-only
ledger_file: claim_inventory.jsonl (canonical; this doc is a projection of it)
```

## 1. Run Summary

```text
prior_inventory: Grounding/v2_1/claim_inventory.jsonl
total_entries: 6008
counts_by_type: {'BL': 211, 'DEF': 804, 'DEP': 314, 'NC': 4654, 'OP': 25}
new_in_v2_2: 3169
preserved: 2839
merged_into: 1500
superseded_no_successor: 0
strict_fcl_chain_validation: passed
```

## 2. Comparison Against v2.1

```text
total entries delta: +1669  (4339 -> 6008)
BL delta:  +3
DEF delta: +0
DEP delta: +0
NC delta:  +1666
OP delta:  +0
```

## 3. New Entry Attribution

```text
noncollapse_registry: 1651
fcl003_operating_point_a: 0
memory_index_registry_routes: 0
unattributed_new_entries: 1518
```

## 4. Chain Validation

```text
status: passed
chain: ['Grounding/v0_2/id_crosswalk.json', 'Grounding/v2_1/id_crosswalk.json', 'Grounding/v2_2/id_crosswalk.json']
ref_sections: {'FCL-001': 10, 'FCL-002': 13, 'FCL-003': 7}
dangling_refs: {}
```
