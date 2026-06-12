# DME V2 - Language Admission Prototype

```text
status: grounding instrument / v0 extraction specification / pre-implementation
folder: Implementation_Orientation
related:
  - Core/README.DME.V2.IdentityEnvelopeComposition.md
  - Core/README.DME.V2.ClaimInventory.md
  - Core/README.DME.V2.FormalCorrespondenceLedger.md
  - Substrates/README.DME.V2.StructureSubstrate.md
  - Substrates/README.DME.V2.LedgerSubstrate.md
schema posture: deferred
source_snapshot: pending tag theory-v2.0-pre-grounding
```

---

## 1. Purpose

This document specifies the first executable projection path:

```text
DME Theory markdown
-> provenance-backed claim ledger
```

It defines what is extracted, how entries are typed, what scale they are assigned, and what provenance every entry must carry before extraction runs.

```text
This is an extraction specification, not a runtime design.

The extractor it specifies is the v0 instrument,
not the DME engine.
```

---

## 2. v0 Scope Boundary

v0 exercises two substrates only:

```text
Structure = parse source into charts and spans
Ledger    = record typed entries with full provenance
```

v0 explicitly does not include:

```text
runtime regime activation
attention dynamics
distinction pressure
hypergraph ledger
reprojection to language
structural signature taxonomy
semantic inference
LLM-assisted extraction
```

Structural signatures are discovered after extraction through recurrence analysis.

They are not pre-declared.

Core law:

```text
v0 extracts what the source explicitly asserts.

Anything requiring inference is out of scope and declared so.
```

---

## 3. The v0 Pipeline

```text
MarkdownSource at tagged snapshot
-> RootSymbolChart
-> SpanGraph
-> PatternPass
-> ClaimEntry
-> FlatLedger
-> RecurrencePass
```

Expanded:

```text
MarkdownSource
= markdown files from source_snapshot

RootSymbolChart
= lines, offsets, blocks, headings, code fences, metadata blocks

SpanGraph
= token / span / sentence / paragraph / section spans

PatternPass
= deterministic extraction grammar

ClaimEntry
= typed, provenanced record

FlatLedger
= append-only JSONL or markdown table

RecurrencePass
= post-extraction recurrence mapping
```

---

## 4. Scale Ladder

```text
token =
exact symbol/order; used for verbatim spans

span =
contiguous sub-sentence region; pattern match unit

sentence =
claim relation; default band for most entries

paragraph =
argument unit; context field, not extraction unit in v0

section =
doctrine role; recorded as context on every entry

document =
purpose/dependency role; recorded as source_file

repo_doctrine =
canonical chain; recorded via source_snapshot
```

v0 extracts primarily at span and sentence scale.

v0 records paragraph, section, document, and repo context as provenance.

Higher-band claims are composed later.

They are not extracted directly in v0.

---

## 5. Extraction Grammar

v0 uses six deterministic pattern classes.

Each pattern class declares surface forms, captured content, default scale, and known limits.

---

### 5.1 DefinitionDistinction - DEF

```text
surface forms:
  code-block definitions: "Term =" followed by body
  inline equations:       "X = Y" in text blocks
  labeled definitions:    "Definition:" lines
  glossary entries

captures:
  defined term
  definition body span

default scale:
  sentence

known limit:
  prose definitions without explicit definition markers are missed in v0
```

---

### 5.2 NonCollapseDistinction - NC

```text
surface forms:
  "A != B"
  "A is not B"
  "A does not imply B"
  "must not be collapsed with"
  "must not be confused with"

captures:
  left term
  right term
  relation = non_equivalence

default scale:
  sentence / doctrine_law

known limit:
  paraphrased non-collapse claims are missed in v0
```

---

### 5.3 BoundaryLawDistinction - BL

```text
surface forms:
  "Core law:" labeled blocks
  "may not X without Y"
  "requires"
  "must"
  "never"
  "only when"
  "only if"

captures:
  governed action
  condition
  modality

default scale:
  sentence / doctrine_law
```

---

### 5.4 OperatorRelationDistinction - OP

```text
surface forms:
  arrow chains whose elements match operator vocabulary
  "Operator path:" labeled blocks

operator vocabulary source:
  Grammar/README.DME.V2.OperatorGrammar.md

captures:
  ordered operator sequence
  span

default scale:
  span
```

---

### 5.5 DependencyDistinction - DEP

```text
surface forms:
  metadata lists: "related:", "depends_on:"
  forward references: "defined in <file>"
  forward references: "specified later in <file>"
  "downstream of" statements

captures:
  source doc
  target doc / section
  dependency direction

default scale:
  document
```

---

### 5.6 General Assertive Claims - OUT OF SCOPE IN v0

General claims lacking the above surface forms require inference.

They are deferred to v1.

This omission is declared, not hidden.

```text
v0 inventory completeness claim:

complete over the declared grammar,
not complete over the theory's meaning.
```

---

## 6. ClaimEntry Record Shape

```text
claim_id
claim_type
source_file
line_range
char_span
source_snapshot
verbatim_span
normalized_terms
scale_band
section_context
evaluated_axes
omitted_axes
opacity_status
support_status
recurrence_refs
extraction_method
notes
```

ID format:

```text
CLAIM-{TYPE}-{NNNN}
```

ID rules:

```text
IDs are append-only.
IDs are never reused.
IDs are never silently renumbered.
```

Required source fields:

```text
source_file
line_range
char_span
source_snapshot
verbatim_span
```

---

## 7. v0 Status Defaults

A deterministic pattern match evaluates exactly two axes:

```text
Distinction =
the difference or relation is explicitly asserted.

Ledger =
exact source provenance exists.
```

All other axes are omitted at extraction.

Default axis profile:

```text
evaluated_axes:
  - Distinction
  - Ledger

omitted_axes:
  - Constraint
  - Identity
  - Projection
  - Feedback
  - Consequence
  - Proof
  - Authority
  - Budget
```

Therefore v0 default status is:

```text
opacity_status: partially_supported
support_status: partially_admitted
```

No v0 entry may carry fully_admitted, ledger_supported, or feedback_tested status.

Promotion requires evaluation beyond extraction.

---

## 8. RecurrencePass

After extraction, compute:

```text
RecurrenceMap:
  normalized_terms -> claim_id list
  cross-document recurrence counts
  co-occurrence within sections
  repeated relation patterns
```

StructuralSignature candidates emerge from RecurrenceMap.

They are outputs of this pass, not inputs to it.

---

## 9. v0 -> v1 Relation

v1 re-derives entries from the same tagged snapshot using runtime-derived architecture.

The v0/v1 delta is a feedback test:

```text
Did v1 recover what deterministic v0 extraction found?
What did v1 find that v0 missed?
What did v0 find that v1 missed?
On which axes do their evaluations differ?
```

v0 is the ground-truth benchmark for v1, not a throwaway.

---

## 10. Non-Collapse Laws

```text
extraction != endorsement
pattern match != semantic understanding
inventory completeness != theory completeness
claim entry != invariant
claim entry != canon
recurrence != importance
v0 ledger != hypergraph ledger
structural signature != predeclared taxonomy
```

---

## 11. Deferred Work

```text
v1 inference-assisted extraction
general assertive claims
paraphrased laws
hypergraph ledger design
candidate ladder mechanics
reprojection to language
CoherenceDelta evaluation
structural signature taxonomy after RecurrencePass
```
