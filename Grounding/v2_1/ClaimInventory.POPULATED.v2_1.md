# DME V2 - Claim Inventory (POPULATED, v2.1)

```text
status: grounding instrument / POPULATED
source_snapshot: theory-v2.1-grounded-canon
extraction_method: extractor v0.2, deterministic pattern grammar
population_status: populated - derived record, append-only
ledger_file: claim_inventory.jsonl (canonical; this doc is a projection of it)
```

## 1. Run Summary

```text
prior_inventory: Grounding/v0_2/claim_inventory.jsonl
total_entries: 4339
counts_by_type: {'BL': 208, 'DEF': 804, 'DEP': 314, 'NC': 2988, 'OP': 25}
new_in_v2_1: 1572
preserved: 2767
merged_into: 1520
superseded_no_successor: 0
strict_fcl_chain_validation: passed
```

## 2. Comparison Against v0.2

```text
total entries delta: +52  (4287 -> 4339)
BL delta:  +9
DEF delta: +2
DEP delta: +5
NC delta:  +36
OP delta:  +0
```

## 3. New Entry Attribution

```text
translation_path_composition: 2
identity_plurality: 2
support_and_authorization: 7
grounded_inquiry_protocol: 20
authority_debt_anchor: 0
unattributed_new_entries: 1541
```

## 4. Chain Validation

```text
status: passed
chain: ['Grounding/v0_2/id_crosswalk.json', 'Grounding/v2_1/id_crosswalk.json']
ref_sections: {'FCL-001': 10, 'FCL-002': 13}
dangling_refs: {}
```
