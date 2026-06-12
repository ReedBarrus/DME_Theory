# Provisional Orders and Maps

```text
source_snapshot: theory-v2.1-grounded-canon
measurement_layer_version: provisional-galois-v0.1
status: hypothetical topology for measurement only
doctrine_status: not admitted
```

## 1. Boundary

This document defines candidate orders and maps for measuring ODQ-4 and ODQ-5 over the lawfully re-derived v2.1 inventory.

These are hypothetical topology only.

They do not declare doctrine.

They do not admit a Galois connection.

## 2. Order Convention

Both candidate orders are pointwise product partial orders.

```text
Profile A <= Profile B iff A <= B on every component.
higher = stronger epistemic grounding
omitted axes count negatively
scalar scoring, weighted sums, and rank aggregation are forbidden
incomparability is a reported result, not a failure
```

## 3. Abstract-Side Candidate Order

Components:

```text
support_status order
opacity_status order
evaluated-axis coverage order
provenance/source-span completeness order
omitted-axis penalty order
```

Component realizations in this layer:

```text
support_status: inferred_candidate < structurally_supported < partially_admitted < fully_admitted < ledger_supported < feedback_tested
opacity_status: opaque < conjectural < candidate < partially_supported < fully_supported
evaluated-axis coverage: stronger = superset
provenance/source-span completeness: stronger = superset of present provenance/source-span fields
omitted-axis penalty: stronger = subset of omitted axes
```

## 4. Concrete-Side Candidate Order

Components:

```text
axis-evaluation dominance
provenance inclusion
source-span specificity
declared loss / preservation completeness
live claim resolution through the v2.1 inventory
```

Component realizations in this layer:

```text
axis-evaluation dominance: stronger = more evaluated axes and fewer omitted axes
provenance inclusion: stronger = superset of provenance + source-lineage fields
source-span specificity: stronger = narrower span within the same source file
loss/preservation completeness: absent < declared
live claim resolution: unresolved < resolved_via_chain < live_direct
```

## 5. Deontic Separation

Blocked uses remain outside the epistemic orders.

```text
blocked_uses does not lower support_status
blocked_uses is tracked as a separate deontic/use-authorization profile
support and authorization are measured separately and never folded
```

## 6. Provisional Maps

### alpha(entry)

Maps a live v2.1 claim entry to an abstract admission profile containing:

```text
claim_id
claim_type
support_status
opacity_status
evaluated_axes
omitted_axes
provenance/source-span completeness
context_sensitive flag
use_mention flag
deontic profile: blocked_uses only as authorization constraints
```

### gamma(profile)

Maps an abstract admission profile to a required concrete evidence envelope containing:

```text
required evaluated axes
required provenance/source-span fields
required source lineage
required loss/preservation declaration status
required opacity/context annotations
required blocked-use separation, if blocked uses exist
```

### profile_of(envelope)

```text
the strongest admission profile warranted by exactly that evidence envelope.
```

In this provisional layer, `profile_of` is treated as a candidate component of any future declared gamma structure.

## 7. Current Measured Posture

```text
total_entries: 4339
blocked_entry_count: 45
within_type_total_pairs: 4856353
across_type_total_pairs: 4554938
```
