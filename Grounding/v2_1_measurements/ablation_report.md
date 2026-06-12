# Component Ablation Diagnostic

```json
{
  "source_snapshot": "theory-v2.1-grounded-canon",
  "diagnostic_version": "component-ablation-v0.1",
  "inputs": {
    "claim_inventory_sha256": "b0d3d674b734296e3d4ed71c5ba6ac000291ba06ea5a2b906b0634c7e5c1f030",
    "run_manifest_sha256": "6acc94657a697afc49f6f44e96f8129ad936ce1728b4351807168c56c6c2df91",
    "provisional_suite_sha256": "4089762eed4b336a61f24354e7d78ffcb362ba2c3f1900d8c255b7bbb60a402f"
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
  "provisional_summary_verdict": "ODQ-4/5 require more instrument work"
}
```

## 2. Component Ablation

```json
{
  "support_status_only": {
    "total_pairs": 4856353,
    "equal": 4796446,
    "left_leq_right": 32051,
    "right_leq_left": 27856,
    "incomparable": 0,
    "comparability_rate": 1.0
  },
  "opacity_status_only": {
    "total_pairs": 4856353,
    "equal": 4856353,
    "left_leq_right": 0,
    "right_leq_left": 0,
    "incomparable": 0,
    "comparability_rate": 1.0
  },
  "evaluated_axes_only": {
    "total_pairs": 4856353,
    "equal": 4856353,
    "left_leq_right": 0,
    "right_leq_left": 0,
    "incomparable": 0,
    "comparability_rate": 1.0
  },
  "span_provenance_only": {
    "total_pairs": 4856353,
    "equal": 0,
    "left_leq_right": 0,
    "right_leq_left": 0,
    "incomparable": 4856353,
    "comparability_rate": 0.0
  }
}
```

## 3. Recurrence-Class Quotient

```json
{
  "class_key": [
    "claim_type",
    "verbatim_span (canonicalized)",
    "opacity_status",
    "evaluated_axes",
    "omitted_axes"
  ],
  "class_count": 705,
  "within_class_pair_count": 6640,
  "pointwise_order_components": [
    "support_status",
    "opacity_status",
    "evaluated_axes",
    "omitted_axes (negative)"
  ],
  "summary": {
    "total_pairs": 6640,
    "equal": 6635,
    "left_leq_right": 5,
    "right_leq_left": 0,
    "incomparable": 0,
    "comparability_rate": 1.0
  }
}
```

## 4. Confirmation

```json
{
  "identity_coordinate_annihilation_confirmed": true,
  "recurrence_class_quotient_restoration_confirmed": true,
  "conservative_resolution_gate": true,
  "homogeneity_caveat": "Support, opacity, and evaluated-axis signatures are highly homogeneous in the current inventory. The ablation cleanly isolates identity-coordinate annihilation, but it does not by itself verify discriminating order behavior under future status divergence."
}
```

## 5. Readout

```text
span/provenance-only comparability: 0.000000
quotient within-class comparability: 1.0000 over 6640 pairs in 705 classes
Support, opacity, and evaluated-axis signatures are highly homogeneous in the current inventory. The ablation cleanly isolates identity-coordinate annihilation, but it does not by itself verify discriminating order behavior under future status divergence.
```
