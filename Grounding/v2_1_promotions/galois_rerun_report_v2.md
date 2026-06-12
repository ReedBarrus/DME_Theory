# Galois Measurement Rerun Under Promotion Overlay

```json
{
  "source_snapshot": "theory-v2.1-grounded-canon",
  "promotion_layer_version": "full-admission-gate-v0.2",
  "base_inventory_sha256": "b0d3d674b734296e3d4ed71c5ba6ac000291ba06ea5a2b906b0634c7e5c1f030",
  "status_overlay_sha256": "49bb9f2b6a4cc21c656033f284ba56d185f8de5fdea5a9ab5b1f2f752bcaf485",
  "base_suite_sha256": "4089762eed4b336a61f24354e7d78ffcb362ba2c3f1900d8c255b7bbb60a402f",
  "sizing_report_sha256": "f5058cde9546a743fb694318bdc00c91ca345ca9599aae811cf581caeaf32e54"
}
```

## 1. Base vs Overlay

```json
{
  "base": {
    "idempotence_noninflation_composite": {
      "violation_count": 0
    },
    "unit_soundness_proxy": {
      "total_entries": 4339,
      "support_inflation_against_own_requirements": [],
      "violation_count": 0
    },
    "within_class_comparability": {
      "class_key": [
        "claim_type",
        "verbatim_span (canonicalized)"
      ],
      "class_count": 705,
      "pair_count": 6640,
      "relations": {
        "equal": 6635,
        "left_leq_right": 5,
        "right_leq_left": 0,
        "incomparable": 0
      },
      "fcl_affected_relations": {
        "equal": 7,
        "left_leq_right": 0,
        "right_leq_left": 0,
        "incomparable": 0
      },
      "fcl_affected_non_equal_comparable_pairs": []
    },
    "recurrence_class_quotient": {
      "class_key": [
        "claim_type",
        "verbatim_span (canonicalized)",
        "opacity_status",
        "evaluated_axes",
        "omitted_axes"
      ],
      "class_count": 705,
      "pair_count": 6640,
      "relations": {
        "equal": 6635,
        "left_leq_right": 5,
        "right_leq_left": 0,
        "incomparable": 0
      }
    }
  },
  "overlay": {
    "idempotence_noninflation_composite": {
      "violation_count": 0
    },
    "unit_soundness_proxy": {
      "total_entries": 4339,
      "support_inflation_against_own_requirements": [],
      "violation_count": 0
    },
    "idempotence_confirmation": {
      "hash_equality": true,
      "field_deltas": [],
      "profile_deltas": [],
      "order_comparison_deltas": [],
      "run_a_hashes": {
        "alpha_profiles_hash": "de9dd027e7794a131969e8331f766c093c43d5e0feeb7c13764ce4b801f02732",
        "concrete_profiles_hash": "2c712d1dac00c69d5ecb128ab2087823e0e221bc51dd2305583e3ec51c952a64",
        "pair_stats_hash": "de328591f0281c9a9d43cbcc821440571fc8fc03aa7e0ae599a815b85f51eb14",
        "composite_results_hash": "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945",
        "unit_results_hash": "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945"
      },
      "run_b_hashes": {
        "alpha_profiles_hash": "de9dd027e7794a131969e8331f766c093c43d5e0feeb7c13764ce4b801f02732",
        "concrete_profiles_hash": "2c712d1dac00c69d5ecb128ab2087823e0e221bc51dd2305583e3ec51c952a64",
        "pair_stats_hash": "de328591f0281c9a9d43cbcc821440571fc8fc03aa7e0ae599a815b85f51eb14",
        "composite_results_hash": "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945",
        "unit_results_hash": "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945"
      }
    },
    "within_class_comparability": {
      "class_key": [
        "claim_type",
        "verbatim_span (canonicalized)"
      ],
      "class_count": 705,
      "pair_count": 6640,
      "relations": {
        "equal": 6635,
        "left_leq_right": 0,
        "right_leq_left": 5,
        "incomparable": 0
      },
      "fcl_affected_relations": {
        "equal": 2,
        "left_leq_right": 0,
        "right_leq_left": 5,
        "incomparable": 0
      },
      "fcl_affected_non_equal_comparable_pairs": [
        {
          "left_claim_id": "CLAIM-DEF-0141",
          "right_claim_id": "CLAIM-DEF-0165",
          "relation": "right_leq_left"
        },
        {
          "left_claim_id": "CLAIM-NC-0522",
          "right_claim_id": "CLAIM-NC-3351",
          "relation": "right_leq_left"
        },
        {
          "left_claim_id": "CLAIM-NC-0522",
          "right_claim_id": "CLAIM-NC-3393",
          "relation": "right_leq_left"
        },
        {
          "left_claim_id": "CLAIM-NC-0523",
          "right_claim_id": "CLAIM-NC-3352",
          "relation": "right_leq_left"
        },
        {
          "left_claim_id": "CLAIM-NC-0523",
          "right_claim_id": "CLAIM-NC-3394",
          "relation": "right_leq_left"
        }
      ]
    },
    "recurrence_class_quotient": {
      "class_key": [
        "claim_type",
        "verbatim_span (canonicalized)",
        "opacity_status",
        "evaluated_axes",
        "omitted_axes"
      ],
      "class_count": 704,
      "pair_count": 6635,
      "relations": {
        "equal": 6635,
        "left_leq_right": 0,
        "right_leq_left": 0,
        "incomparable": 0
      }
    }
  },
  "delta": {
    "non_inflation_violation_delta": 0,
    "unit_soundness_violation_delta": 0,
    "within_class_non_equal_comparable_delta": 0,
    "quotient_non_equal_comparable_delta": -5
  }
}
```
