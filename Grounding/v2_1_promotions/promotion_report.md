# First Promotion-Gate Evaluation

## 1. Source Anchor

```text
source_snapshot: theory-v2.1-grounded-canon
v2_1_inventory_sha256: b0d3d674b734296e3d4ed71c5ba6ac000291ba06ea5a2b906b0634c7e5c1f030
status_overlay_sha256: 22be66ad7db048500ee52768cf29fb7f5908f4c5d75b4af790f4fab31f1099f9
```

## 2. FCL Chain Resolution

```text
total FCL-cited refs: 23
live resolved refs: 23
unresolved refs: 0
section counts: {'FCL-001': 10, 'FCL-002': 13}
section live counts: {'FCL-001': 8, 'FCL-002': 8}
overlap live ids: ['CLAIM-DEF-0131', 'CLAIM-NC-0528']
```

Resolved claims:

```text
FCL-001: CLAIM-BL-0071 -> CLAIM-BL-0071 (Core/README.DME.V2.IdentityEnvelopeComposition.md:156-157)
FCL-001: CLAIM-BL-0074 -> CLAIM-BL-0073 (Core/README.DME.V2.IdentityEnvelopeComposition.md:242-245)
FCL-001: CLAIM-BL-0093 -> CLAIM-BL-0093 (Core/README.DME.V2.IdentityEnvelopeComposition.md:593-593)
FCL-001: CLAIM-DEF-0131 -> CLAIM-DEF-0131 (Core/README.DME.V2.IdentityEnvelopeComposition.md:557-559)
FCL-001: CLAIM-DEF-0132 -> CLAIM-DEF-0132 (Core/README.DME.V2.IdentityEnvelopeComposition.md:71-73)
FCL-001: CLAIM-DEF-0133 -> CLAIM-DEF-0133 (Core/README.DME.V2.IdentityEnvelopeComposition.md:125-128)
FCL-001: CLAIM-DEF-0141 -> CLAIM-DEF-0141 (Core/README.DME.V2.IdentityEnvelopeComposition.md:661-663)
FCL-001: CLAIM-NC-0551 -> CLAIM-NC-0528 (Core/README.DME.V2.IdentityEnvelopeComposition.md:504-504)
FCL-001: CLAIM-NC-0552 -> CLAIM-NC-0528 (Core/README.DME.V2.IdentityEnvelopeComposition.md:504-504)
FCL-001: CLAIM-NC-0553 -> CLAIM-NC-0528 (Core/README.DME.V2.IdentityEnvelopeComposition.md:504-504)
FCL-002: CLAIM-BL-0088 -> CLAIM-BL-0088 (Core/README.DME.V2.IdentityEnvelopeComposition.md:323-325)
FCL-002: CLAIM-DEF-0134 -> CLAIM-DEF-0131 (Core/README.DME.V2.IdentityEnvelopeComposition.md:557-559)
FCL-002: CLAIM-DEF-0135 -> CLAIM-DEF-0131 (Core/README.DME.V2.IdentityEnvelopeComposition.md:557-559)
FCL-002: CLAIM-DEF-0138 -> CLAIM-DEF-0138 (Core/README.DME.V2.IdentityEnvelopeComposition.md:348-350)
FCL-002: CLAIM-NC-0522 -> CLAIM-NC-0522 (Core/README.DME.V2.IdentityEnvelopeComposition.md:386-386)
FCL-002: CLAIM-NC-0523 -> CLAIM-NC-0523 (Core/README.DME.V2.IdentityEnvelopeComposition.md:387-387)
FCL-002: CLAIM-NC-0528 -> CLAIM-NC-0528 (Core/README.DME.V2.IdentityEnvelopeComposition.md:504-504)
FCL-002: CLAIM-NC-0529 -> CLAIM-NC-0528 (Core/README.DME.V2.IdentityEnvelopeComposition.md:504-504)
FCL-002: CLAIM-NC-0530 -> CLAIM-NC-0528 (Core/README.DME.V2.IdentityEnvelopeComposition.md:504-504)
FCL-002: CLAIM-NC-0532 -> CLAIM-NC-0528 (Core/README.DME.V2.IdentityEnvelopeComposition.md:504-504)
FCL-002: CLAIM-NC-0533 -> CLAIM-NC-0528 (Core/README.DME.V2.IdentityEnvelopeComposition.md:504-504)
FCL-002: CLAIM-NC-2764 -> CLAIM-NC-2764 (Core/README.DME.V2.IdentityEnvelopeComposition.md:361-361)
FCL-002: CLAIM-NC-2765 -> CLAIM-NC-2765 (Core/README.DME.V2.IdentityEnvelopeComposition.md:411-411)
```

## 3. Divergence Summary

```text
axis profile distribution before overlay: {'Distinction | Ledger': 4339}
axis profile distribution after overlay:  {'Distinction | Ledger': 4325, 'Distinction | Ledger | Proof': 14}
support/status distribution before overlay: {'partially_admitted': 4294, 'structurally_supported': 45}
support/status distribution after overlay:  {'partially_admitted': 4325, 'structurally_supported': 14}
overlay update count: 45
```

## 4. FCL Proof-Axis Evaluation Summary

```text
number of unique live FCL claims evaluated on Proof axis: 14
historical cited refs chain-resolved: 23
FCL-001 unique live count: 8
FCL-002 unique live count: 8
overlap: 2
```

## 5. Gate Evaluation Summary

```text
structurally_supported -> partially_admitted promotions: 31
structurally_supported -> partially_admitted not eligible: 14
fully_admitted -> ledger_supported not eligible: 0
```

Not eligible examples:

```json
{
  "structurally_supported": [
    {
      "claim_id": "CLAIM-BL-0040",
      "failed_requirements": [
        "RecurrenceMap entry created"
      ],
      "use_mention_flag": "unknown",
      "context_sensitive": false
    },
    {
      "claim_id": "CLAIM-BL-0102",
      "failed_requirements": [
        "RecurrenceMap entry created"
      ],
      "use_mention_flag": "asserted",
      "context_sensitive": true
    },
    {
      "claim_id": "CLAIM-BL-0161",
      "failed_requirements": [
        "RecurrenceMap entry created"
      ],
      "use_mention_flag": "unknown",
      "context_sensitive": false
    },
    {
      "claim_id": "CLAIM-BL-0171",
      "failed_requirements": [
        "RecurrenceMap entry created"
      ],
      "use_mention_flag": "example",
      "context_sensitive": false
    },
    {
      "claim_id": "CLAIM-BL-0172",
      "failed_requirements": [
        "RecurrenceMap entry created"
      ],
      "use_mention_flag": "example",
      "context_sensitive": false
    },
    {
      "claim_id": "CLAIM-BL-0379",
      "failed_requirements": [
        "RecurrenceMap entry created"
      ],
      "use_mention_flag": "unknown",
      "context_sensitive": false
    },
    {
      "claim_id": "CLAIM-DEF-0246",
      "failed_requirements": [
        "RecurrenceMap entry created"
      ],
      "use_mention_flag": "unknown",
      "context_sensitive": false
    },
    {
      "claim_id": "CLAIM-DEF-0247",
      "failed_requirements": [
        "RecurrenceMap entry created"
      ],
      "use_mention_flag": "unknown",
      "context_sensitive": false
    },
    {
      "claim_id": "CLAIM-DEF-0248",
      "failed_requirements": [
        "RecurrenceMap entry created"
      ],
      "use_mention_flag": "unknown",
      "context_sensitive": false
    },
    {
      "claim_id": "CLAIM-DEF-0249",
      "failed_requirements": [
        "RecurrenceMap entry created"
      ],
      "use_mention_flag": "unknown",
      "context_sensitive": false
    },
    {
      "claim_id": "CLAIM-DEF-0250",
      "failed_requirements": [
        "RecurrenceMap entry created"
      ],
      "use_mention_flag": "unknown",
      "context_sensitive": false
    },
    {
      "claim_id": "CLAIM-DEF-0638",
      "failed_requirements": [
        "RecurrenceMap entry created"
      ],
      "use_mention_flag": "unknown",
      "context_sensitive": false
    },
    {
      "claim_id": "CLAIM-DEF-0839",
      "failed_requirements": [
        "RecurrenceMap entry created"
      ],
      "use_mention_flag": "unknown",
      "context_sensitive": false
    },
    {
      "claim_id": "CLAIM-NC-1118",
      "failed_requirements": [
        "RecurrenceMap entry created"
      ],
      "use_mention_flag": "unknown",
      "context_sensitive": false
    }
  ],
  "fully_admitted": []
}
```

## 6. Blocked Gate Census

```text
gate_undeclared count: 4294
affected source/target rungs:
  partially_admitted -> fully_admitted
blocked examples: ['CLAIM-BL-0001', 'CLAIM-BL-0003', 'CLAIM-BL-0005', 'CLAIM-BL-0006', 'CLAIM-BL-0007', 'CLAIM-BL-0008', 'CLAIM-BL-0009', 'CLAIM-BL-0010', 'CLAIM-BL-0011', 'CLAIM-BL-0012', 'CLAIM-BL-0013', 'CLAIM-BL-0014', 'CLAIM-BL-0016', 'CLAIM-BL-0017', 'CLAIM-BL-0019', 'CLAIM-BL-0022', 'CLAIM-BL-0025', 'CLAIM-BL-0027', 'CLAIM-BL-0029', 'CLAIM-BL-0030', 'CLAIM-BL-0035', 'CLAIM-BL-0037', 'CLAIM-BL-0038', 'CLAIM-BL-0043', 'CLAIM-BL-0045']
candidate ODQ-7 text:
What are the declared conditions for promotion from partially_admitted to fully_admitted, and how do Proof-axis evaluation, feedback survival, recurrence stability, and reconstruction burden contribute to that promotion without collapsing support into authorization?
```

## 7. Galois Rerun Summary

```text
non-inflation violation delta: 0
unit-soundness violation delta: 0
idempotence stable: true
within-class non-equal comparable delta: 0
quotient non-equal comparable delta: -5
FCL-affected non-equal comparable pairs: [{'left_claim_id': 'CLAIM-DEF-0141', 'right_claim_id': 'CLAIM-DEF-0165', 'relation': 'right_leq_left'}, {'left_claim_id': 'CLAIM-NC-0522', 'right_claim_id': 'CLAIM-NC-3351', 'relation': 'right_leq_left'}, {'left_claim_id': 'CLAIM-NC-0522', 'right_claim_id': 'CLAIM-NC-3393', 'relation': 'right_leq_left'}, {'left_claim_id': 'CLAIM-NC-0523', 'right_claim_id': 'CLAIM-NC-3352', 'relation': 'right_leq_left'}, {'left_claim_id': 'CLAIM-NC-0523', 'right_claim_id': 'CLAIM-NC-3394', 'relation': 'right_leq_left'}]
```

## 8. Verdict

```text
first divergence stable but gate gap requires ODQ-7 before FCL-003
```
