# DME V2 - Claim Inventory

```text
status: grounding instrument / scaffold / population pending
folder: Core
related:
  - Implementation_Orientation/README.DME.V2.LanguageAdmissionPrototype.md
  - Core/README.DME.V2.FormalCorrespondenceLedger.md
schema posture: deferred
source_snapshot: pending tag theory-v2.0-pre-grounding
population_status: scaffold only - no entries yet
```

---

## 1. Purpose

This document is the registry of claims extracted from DME Theory at a declared snapshot.

It is the theory's distinction field rendered as a provenance-backed inventory.

```text
The inventory is a derived artifact.

It is populated only from a tagged snapshot,
only via the declared extraction method.
```

---

## 2. Population Rules

Entries derive exclusively from the extraction specified in:

```text
Implementation_Orientation/README.DME.V2.LanguageAdmissionPrototype.md
```

The extraction must run against `source_snapshot`.

Hand-authored entries are not permitted in v0.

Entries are append-only.

Corrections are recorded as superseding entries referencing the original `claim_id`.

If the theory changes, the inventory is re-derived against a new tag.

Inventories are never silently edited to track a moving source.

---

## 3. Entry Record Shape

Entries follow the ClaimEntry Record Shape in `LanguageAdmissionPrototype`.

Illustrative example only, not a populated entry:

```text
claim_id: CLAIM-NC-0001
claim_type: NC
source_file: Core/README.DME.V2.IdentityEnvelopeComposition.md
line_range: pending
char_span: pending
verbatim_span: "coordinate regime != envelope"
normalized_terms: coordinate_regime | envelope | non_equivalence
scale_band: sentence / doctrine_law
evaluated_axes: Distinction, Ledger
omitted_axes: Constraint, Identity, Projection, Feedback, Consequence, Proof, Authority, Budget
opacity_status: partially_supported
support_status: partially_admitted
source_snapshot: theory-v2.0-pre-grounding
```

---

## 4. Status Enums

```text
opacity_status:
  fully_supported
  partially_supported
  candidate
  conjectural
  opaque

support_status:
  inferred_candidate
  structurally_supported
  partially_admitted
  fully_admitted
  ledger_supported
  feedback_tested
```

---

## 5. Non-Collapse Laws

```text
inventory != doctrine
entry != endorsement
entry count != claim importance
extracted != true
populated inventory != stable theory
claim inventory != formal correspondence ledger
```

---

## 6. Population Pending

No entries are populated before the `theory-v2.0-pre-grounding` tag.

This document is scaffold only until extraction runs.
