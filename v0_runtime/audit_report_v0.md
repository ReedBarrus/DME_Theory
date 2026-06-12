# v0 Extraction Quality Audit

```text
status: audit record / probabilistic-regime evaluation over deterministic outputs
audited_artifact: claim_inventory.jsonl @ theory-v2.0-pre-grounding, extractor v0.1
sample_seed: 7 (reproducible)
judge: Claude (LLM) — sample classifications are semantic judgments,
       declared as probabilistic-regime evaluations, NOT deterministic admissions
sample sizes: NC 25 / DEF 25 / BL-corelaw 15 / BL-modal 10 / OP 25 (all) / DEP 10
```

## Per-Class Verdicts

```text
NC (2,723 entries)         ~96-99% clean
  25/25 sampled were genuine non-collapse assertions.
  Known mention-risk subset exists (see Use/Mention below).
  VERDICT: trustworthy for FCL work.

DEF-block (431 entries)    ~96% clean
  24/25 sampled clean, well-formed term=body definitions.
DEF-label (12 entries)     mostly fragments
  Captures bare "Definition:" labels without following body.
  VERDICT: DEF-block trustworthy; DEF-label needs v0.2 fix.

BL-corelaw (269 entries)   ~65% clean
  Genuine laws present, but core-law fences are captured per-line:
  multi-line laws split into fragments ("not vague trust."),
  contextual sentences over-captured ("GitHub is the growth layer."),
  cross-class duplication (DEF lines re-captured as BL).

BL-modal (109 entries)     ~45% clean — WORST CLASS
  Fragments ("what must archive"), descriptive lines, and one
  serious hazard class: NEGATION-CONTEXT INVERSION —
  "identity cannot be tracked" captured from a "Without distinctions:"
  block. The captured line's meaning depends on an uncaptured
  conditional prefix. Standalone, it asserts the opposite of doctrine.
  VERDICT: BL unusable for doctrine decisions until v0.2.

OP (25 entries)            100% clean
DEP (309 entries)          ~100% clean
  Minor refinement: "related:" lists asserted as depends_on;
  should be typed related_to (weaker relation).
```

## Use/Mention Contamination

```text
58 entries originate from the three grounding-instrument docs.
Not all are contamination — the instruments' own non-collapse laws
are genuine assertions. But illustrative content IS captured as if
asserted, e.g.:

  CLAIM-NC-0173: verbatim_span: "coordinate regime != envelope"
  (the ClaimInventory's illustrative example, captured as a claim)

v0 cannot distinguish use from mention. This is now a measured
limitation, not a hypothetical one.
```

## Overall Estimate

```text
weighted clean rate: ~91% across all entries
clean rate excluding BL: >96%
FCL-relevant classes (NC, DEF from IdentityEnvelopeComposition + CTT):
  clean in all sampled instances
```

## v0.2 Patch Queue (deterministic fixes only)

```text
1. Core-law fences: capture whole fenced block as ONE BL entry,
   not per-line fragments
2. BL-modal: sentence-shape filter (capitalized start, terminal
   punctuation); exclude "what/which..." fragments
3. Negation-context guard: record context_prefix when preceding
   fence line ends with ":" — annotate, don't drop
4. use_mention_flag on entries from instrument docs and
   example-labeled sections
5. DEF-label: attach following fenced block as body, or drop bare labels
6. DEP relation typing: related_to vs depends_on
```

## Blocking Analysis

```text
FCL-001 / FCL-002: NOT BLOCKED.
  Their claim clusters draw on NC and DEF classes, which audited clean.
  FCL-001 cluster (IdentityEnvelopeComposition): 129 entries
  (68 NC, 22 DEF, 29 BL, 1 OP, 9 DEP) — use NC+DEF, treat BL with caution.

Doctrine compression decisions: BLOCKED until v0.2.
  The 559-duplicate analysis is NC-based (clean), but any
  BL-informed compression must wait for the core-law fence fix.
```

## Non-Collapse

```text
audit estimate != measured ground truth
judge classification != deterministic evaluation
clean sample != clean class
91% clean != 91% true
```
