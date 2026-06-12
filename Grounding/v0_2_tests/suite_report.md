# v0.2 Idempotence + Round-Trip Measurement Suite

```text
source_snapshot: theory-v2.1-grounded-canon
extractor_version: v0.2
committed_baseline: Grounding/v2_1
```

## 1. Baseline

```text
total_entries: 4339
counts_by_type: {'BL': 208, 'DEF': 804, 'DEP': 314, 'NC': 2988, 'OP': 25}
support_counts: {'partially_admitted': 4294, 'structurally_supported': 45}
use_mention_counts: {'asserted': 4274, 'example': 4, 'instrument_self_assertion': 21, 'unknown': 40}
blocked_entry_count: 45
context_sensitive_entry_count: 1
```

## 2. Idempotence

```text
classification: measurable
passed: true
strict_current_corpus_rerun: measurable
strict_current_corpus_error: None
committed_vs_rerun_a hashes equal: true
rerun_a_vs_rerun_b hashes equal: true
committed_vs_rerun_a field deltas: 0
rerun_a_vs_rerun_b field deltas: 0
```

## 3. Round-Trip Proxies

### status_fixed_point

```text
classification: measurable
passed: true
evidence: {'committed_vs_rerun_a_field_delta_count': 0, 'rerun_a_vs_rerun_b_field_delta_count': 0}
```

### counit_like_non_inflation

```text
classification: partially_measurable
passed: true
evidence: {'committed_vs_rerun_a_support_inflations': [], 'rerun_a_vs_rerun_b_support_inflations': [], 'demoted_entry_count': 45, 'context_sensitive_entry_count': 1}
```

### unit_like_no_loss_of_admitted_structure

```text
classification: blocked
passed: n/a
reason: No doctrine-declared gamma map or concrete order on admitted topology exists yet, so no-loss concretization cannot be formalized as a measurement.
```

## 4. ODQ Measurability

### ODQ-4

```text
classification: partially_measurable
rationale: ODQ-4 is partially measurable because the inventory exposes candidate carriers for the two domains, but canon still does not declare the domain orders themselves.
measurable_surfaces:
  - The abstract-side carrier is observable in the inventory: support_status, opacity_status, blocked_uses, and evaluated/omitted axes are serialized fields.
  - Current v2.1 support-status distribution is measurable: {'partially_admitted': 4294, 'structurally_supported': 45}.
  - Blocked-use divergence is measurable: 45 entries carry blocked uses while remaining epistemically supported.
blocked_surfaces:
  - The doctrine still does not declare an order on admitted topology objects themselves.
  - The doctrine still does not declare an order on hypothetical descriptions themselves beyond status ladders on statuses.
  - Without declared concrete and abstract orders, monotonicity cannot be promoted from proxy observation to formal test.
```

### ODQ-5

```text
classification: partially_measurable
rationale: ODQ-5 is partially measurable because strict rerun idempotence and deflationary proxy behavior are testable now, while full unit/counit admission remains blocked by undeclared maps and orders.
measurable_surfaces:
  - Same-version idempotence is directly measurable as a fixed-point test over a fresh rerun pair.
  - Status non-inflation is measurable as a counit-like proxy by comparing support_status across fresh reruns.
  - Demotion preservation is measurable for context-sensitive and blocked-use entries because those annotations are serialized and comparable by claim_id.
blocked_surfaces:
  - Alpha and gamma are not declared as total monotone maps in doctrine.
  - Unit (no-loss concretization round-trip) cannot be formally tested without a declared order on admitted topology.
  - Counit can only be tested as a proxy fixed-point / non-inflation surface, not as an admitted adjunction law.
proxy_results: {'committed_vs_rerun_a_field_delta_count': 0, 'rerun_a_vs_rerun_b_field_delta_count': 0, 'rerun_a_vs_rerun_b_support_inflations': 0}
```

## 5. Verdict

```text
ODQ-4: partially_measurable
ODQ-5: partially_measurable
No doctrine patched in this suite.
```
