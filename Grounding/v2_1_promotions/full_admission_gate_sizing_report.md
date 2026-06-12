# Full Admission Gate Sizing

```json
{
  "source_snapshot": "theory-v2.1-grounded-canon",
  "sizing_version": "full-admission-gate-sizing-v0.1",
  "inputs": {
    "claim_inventory_sha256": "b0d3d674b734296e3d4ed71c5ba6ac000291ba06ea5a2b906b0634c7e5c1f030",
    "recurrence_map_sha256": "baf22eda77a3ea5808df8e71154f940dec5b993ca9509f52157f41c65ed914d0",
    "run_manifest_sha256": "6acc94657a697afc49f6f44e96f8129ad936ce1728b4351807168c56c6c2df91",
    "promotion_report_v1_sha256": "ec05736eb098ee52bd059b7b100f5374bdc8a89ef20b8649e4a38ccec91af7ab"
  }
}
```

## 1. Baseline

```json
{
  "inventory_total_entries": 4339,
  "counts_by_type": {
    "BL": 208,
    "DEF": 804,
    "DEP": 314,
    "NC": 2988,
    "OP": 25
  },
  "nc_total_entries": 2988
}
```

## 2. Coverage Posture

```json
{
  "NC": "implementable in sizing instrument",
  "BL": "not_implementable without declared basis-pair witness logic",
  "DEF": "not_implementable without declared basis-pair witness logic",
  "DEP": "not_implementable without declared basis-pair witness logic",
  "OP": "not_implementable without declared basis-pair witness logic"
}
```

## 3. NC Gate Components

```json
{
  "definitional_basis_convergence": {
    "count": 694,
    "share_of_nc": 0.2322623828647925,
    "basis_rule": "both relata resolve to DEF basis subjects"
  },
  "recurrence_stability": {
    "count": 1481,
    "share_of_nc": 0.4956492637215529,
    "stability_rule": "recurs across at least two distinct source files at the declared snapshot"
  },
  "context_sensitive_inversion_flags": {
    "count": 0,
    "share_of_nc": 0.0,
    "rule": "context_sensitive entry inside the content recurrence class"
  },
  "deterministic_completeness": {
    "count": 2988,
    "share_of_nc": 1.0,
    "rule": "Distinction and Ledger axes evaluated; runtime/feedback/perturbation axes not required"
  },
  "full_gate_eligible": {
    "count": 506,
    "share_of_nc": 0.16934404283801874,
    "rule": "definitional basis + recurrence stability + no contradiction + deterministic completeness",
    "sample_claim_ids": [
      "CLAIM-NC-0002",
      "CLAIM-NC-0005",
      "CLAIM-NC-0007",
      "CLAIM-NC-0009",
      "CLAIM-NC-0025",
      "CLAIM-NC-0027",
      "CLAIM-NC-0029",
      "CLAIM-NC-0030",
      "CLAIM-NC-0032",
      "CLAIM-NC-0033",
      "CLAIM-NC-0035",
      "CLAIM-NC-0080",
      "CLAIM-NC-0085",
      "CLAIM-NC-0086",
      "CLAIM-NC-0089",
      "CLAIM-NC-0091",
      "CLAIM-NC-0094",
      "CLAIM-NC-0095",
      "CLAIM-NC-0099",
      "CLAIM-NC-0116",
      "CLAIM-NC-0117",
      "CLAIM-NC-0118",
      "CLAIM-NC-0123",
      "CLAIM-NC-0126",
      "CLAIM-NC-0128"
    ]
  }
}
```

## 4. Readout

```text
NC population: 2988
definitional-basis convergence: 694 (23.23%)
recurrence stability: 1481 (49.56%)
context-sensitive inversion flags: 0 (0.00%)
full gate eligible: 506 (16.93%)
The gate is discriminating: neither vacuous nor trivial.
```
