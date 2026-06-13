# Validation Plan

## Scope

This plan defines validation for the v0.4 NormativeClaim chart-basis candidate only.

No extractor implementation is authorized by this document.

## Corpora

```text
Corpus A: IndieWeb Principles
  path: Runtime/v1_admission/runs/indieweb_principles_001/
  provenance strength: partial / observed-prefix only

Corpus B: The Twelve-Factor App
  path: Runtime/v1_admission/runs/twelve_factor_001/
  provenance strength: full source hash

Corpus C: DME NC corpus
  source options:
    - Core/README.DME.V2.NonCollapseRegistry.md
    - Grounding/v2_2_1/claim_inventory.jsonl with basis=doctrine_occurrence and claim_type=NC
```

## Validation Questions

```text
1. Can NormativeClaim candidates be populated for IndieWeb without overfitting slogans?
2. Can NormativeClaim candidates be populated for 12-Factor with polarity, scope, and rationale?
3. Can DME NC laws populate the structure without manufacturing missing rationale?
4. What fields are systematically elided across each corpus?
5. Does polarity improve comparison between prohibitions and non-collapse claims?
6. Does the candidate basis preserve non-collapse between source form and projected structure?
```

## Sampling Requirement For Corpus C

```text
Corpus C first pass:
  Use a seeded random sample of DME NC laws before full projection.
  sample_size: 50
  seed: 20260613
  population: unique doctrine_occurrence NC contents from Grounding/v2_2_1/claim_inventory.jsonl, excluding registry_canonical basis entries.

Full DME NC projection is NOT authorized until the seeded sample does not falsify H3.
```

## Falsification Criteria

Declared before any validation run:

```text
H3 is FALSIFIED if any of the following occur:

1. Population requires invention:
   Populating polarity, action, scope, actor, or rationale requires inventing content not recoverable from the law's own text or local source context.

2. Rationale fabrication threshold:
   More than 30% of sampled NC laws require a rationale that exists nowhere in their source text or immediate context.

3. Collapse:
   Projection maps distinct NC laws to identical NormativeClaim structures while losing the distinction that made the source laws separate.

4. Actor fabrication:
   Projection requires an actor that the corpus never names, implies, or structurally licenses.

5. Polarity ambiguity:
   More than 30% of sampled NC laws cannot determine polarity without interpretive invention.

If H3 is falsified:
  The bridge is elegant but unsupported under this instrument.
  Record the bridge as a closed or revised hypothesis with the failure mode.
  Do NOT canonize.
  Do NOT treat falsification as a program failure.

A falsified bridge is a successful validation outcome.
```

## Planned Outputs

Create later, not now:

```text
Runtime/v1_admission/v0_4_normative_claim_spec/validation_runs/
  indieweb_normative_projection.jsonl
  twelve_factor_normative_projection.jsonl
  dme_ncr_normative_projection_sample.jsonl
  validation_report.md
```

## Guardrails

```text
Bridge remains hypothesis, not doctrine.
Shared chart basis remains comparison structure, not identity.
Foreign corpora remain non-canon throughout validation.
```
