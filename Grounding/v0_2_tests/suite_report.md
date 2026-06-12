# v0.2 Idempotence + Round-Trip Measurement Suite

```text
source_snapshot: theory-v2.0-pre-grounding
extractor_version: v0.2
committed_baseline: Grounding/v0_2
```

## 1. Baseline

```text
total_entries: 4287
counts_by_type: {'BL': 199, 'DEF': 802, 'DEP': 309, 'NC': 2952, 'OP': 25}
support_counts: {'partially_admitted': 4252, 'structurally_supported': 35}
use_mention_counts: {'asserted': 4232, 'example': 4, 'instrument_self_assertion': 21, 'unknown': 30}
blocked_entry_count: 35
context_sensitive_entry_count: 1
```

## 2. Idempotence

```text
classification: partially_measurable
passed: false
strict_current_corpus_rerun: blocked
strict_current_corpus_error: FCL-001 validation failed: dangling claim references -> CLAIM-BL-0093, CLAIM-DEF-0141, CLAIM-NC-0551, CLAIM-NC-0552, CLAIM-NC-0553
provisional_current_corpus_rerun: measurable
provisional_current_corpus_passed: true
committed_vs_rerun_a hashes equal: false
rerun_a_vs_rerun_b hashes equal: true
committed_vs_rerun_a field deltas: 697
rerun_a_vs_rerun_b field deltas: 0
```

## 3. Round-Trip Proxies

### status_fixed_point

```text
classification: measurable
passed: true
evidence: {'rerun_a_vs_rerun_b_field_delta_count': 0, 'baseline_drift_field_delta_count': 697}
```

### counit_like_non_inflation

```text
classification: partially_measurable
passed: true
evidence: {'rerun_a_vs_rerun_b_support_inflations': [], 'baseline_drift_support_inflations_uninterpreted': ['CLAIM-BL-0379', 'CLAIM-DEF-0522', 'CLAIM-DEF-0636', 'CLAIM-DEF-0637', 'CLAIM-DEF-0638', 'CLAIM-NC-2735', 'CLAIM-NC-2741', 'CLAIM-NC-2742', 'CLAIM-NC-2743', 'CLAIM-NC-2744'], 'demoted_entry_count': 35, 'context_sensitive_entry_count': 1}
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
rationale: ODQ-4 is partially measurable because inventory fields expose candidate status carriers, but the orders those carriers should instantiate are not yet canonically declared.
measurable_surfaces:
  - The abstract-side carrier is observable in the inventory: support_status, opacity_status, blocked_uses, and evaluated/omitted axes are all serialized fields.
  - Current v0.2 support-status distribution is measurable: {'partially_admitted': 4252, 'structurally_supported': 35}.
  - Blocked-use divergence is measurable: 35 entries carry blocked uses while remaining epistemically supported.
blocked_surfaces:
  - The doctrine still does not declare an order on admitted topology objects themselves.
  - The doctrine still does not declare an order on hypothetical descriptions themselves beyond status ladders on statuses.
  - Without declared concrete and abstract orders, monotonicity cannot be promoted from proxy observation to formal test.
  - The current strict rerun is additionally blocked by dangling FCL-001 references, so canon-safe measurement cannot proceed until grounding navigation is refreshed.
```

### ODQ-5

```text
classification: partially_measurable
rationale: ODQ-5 is partially measurable because idempotence and deflationary proxy behavior are testable now, while full unit/counit admission remains blocked by undeclared maps and orders.
measurable_surfaces:
  - Same-version idempotence is directly measurable as a fixed-point test over committed v0.2 outputs.
  - Status non-inflation is measurable as a counit-like proxy by comparing support_status across reruns.
  - Demotion preservation is measurable for context-sensitive and blocked-use entries because those annotations are serialized and comparable by claim_id.
blocked_surfaces:
  - Alpha and gamma are not declared as total monotone maps in doctrine.
  - Unit (no-loss concretization round-trip) cannot be formally tested without a declared order on admitted topology.
  - Counit can only be tested as a proxy fixed-point / non-inflation surface, not as an admitted adjunction law.
  - The strict canon-safe rerun is currently blocked by dangling FCL-001 references, so only provisional measurement can run end-to-end.
proxy_results: {'rerun_a_vs_rerun_b_support_inflations': 0, 'baseline_drift_field_delta_count': 697, 'rerun_a_vs_rerun_b_field_delta_count': 0}
```

## 5. Verdict

```text
ODQ-4: partially_measurable
ODQ-5: partially_measurable
No doctrine patched in this suite.
```
