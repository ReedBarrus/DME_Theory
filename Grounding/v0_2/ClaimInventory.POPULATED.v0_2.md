# DME V2 - Claim Inventory (POPULATED, v0.2)

```text
status: grounding instrument / POPULATED
source_snapshot: theory-v2.0-pre-grounding
extraction_method: extractor v0.2, deterministic pattern grammar
population_status: populated - derived record, append-only
ledger_file: claim_inventory.jsonl (canonical; this doc is a projection of it)
```

## 1. Run Summary

```text
corpus: 37 active-doctrine files
  included: Core, Grammar, Substrates, Regime_Ecologies,
            Agentic_Reasoning, Implementation_Orientation,
            README.md, MEMORY_INDEX.md
  excluded: Archive (active != archive), Meta_Web_Gov_Hub (non-DME)

total entries:          4287
  BL    199
  DEP   309
  DEF   802
  NC    2952
  OP    25

cross-entry recurrent terms: 912
duplicate verbatim NC laws:  578
context-sensitive entries:   1
use_mention counts:         {'asserted': 4232, 'example': 4, 'instrument_self_assertion': 21, 'unknown': 30}
BL modal shape rejects:     103
DEF label rejects:          0
status ceiling:             partially_admitted unless context/use_mention lowers support
```

## 2. Counts by Type

```text
 BL  199
DEF  802
DEP  309
 NC  2952
 OP  25
```

## 3. Comparison Against v0.1

```text
total entries delta: +409  (3878 -> 4287)
BL count delta:      -179  (378 -> 199)
DEF count delta:     +359  (443 -> 802)
DEP relation typing summary:
  depends_on: 280
  downstream_of: 2
  related_to: 27
use_mention counts: {'asserted': 4232, 'example': 4, 'instrument_self_assertion': 21, 'unknown': 30}
context_sensitive count: 1
ID stability crosswalk:
  preserved: 3667
  merged_into: 114
  superseded_no_successor: 97
  new_in_v0_2: 620
```

## 4. Most Recurrent Terms

```text
authority                                      397 entries / 31 files
proof                                          275 entries / 31 files
truth                                          176 entries / 32 files
consent                                        117 entries / 24 files
distinction                                    105 entries / 21 files
canon                                           93 entries / 24 files
permission                                      83 entries / 19 files
reference                                       77 entries / 22 files
execution                                       76 entries / 21 files
projection                                      70 entries / 23 files
legitimacy                                      68 entries / 21 files
attention                                       66 entries / 14 files
source                                          65 entries / 22 files
meaning                                         63 entries / 17 files
deletion                                        53 entries / 21 files
feedback                                        50 entries / 19 files
identity                                        47 entries / 16 files
intention                                       47 entries / 13 files
decision                                        41 entries / 14 files
trust                                           41 entries / 13 files
```

## 5. Most Repeated NC Laws

```text
 23x  projection != source
 20x  embedding != meaning
 20x  trust != authority
 19x  proof != authority
 16x  reference != canon
 15x  feedback != proof
 14x  canon != final truth
 14x  ledger != truth
 13x  archive != deletion
 13x  attention != intention
 13x  decision != execution
 12x  attention != consent
 12x  execution != proof
 12x  receipt != authority
 11x  authority != reference
 11x  authority != truth
 11x  feedback != truth
 11x  token != distinction
 10x  access != authority
 10x  echo != proof
```

## 6. BL Cleanliness Re-sample

```text
sample_seed: 7
claim_id: CLAIM-BL-0012
source_file: Agentic_Reasoning/README.AgenticReasoning.SemanticConstraintProtocol.md
line_range: 310-310
verbatim_span: Provenance must preserve lineage, lens, loss, scope, and reconstruction conditions.
context_sensitive: false
use_mention_flag: asserted
audit_note: modal shape-filtered BL
claim_id: CLAIM-BL-0016
source_file: Agentic_Reasoning/README.AgenticReasoning.SemanticConstraintProtocol.md
line_range: 481-481
verbatim_span: Agent intelligence requires bounded claims.
context_sensitive: false
use_mention_flag: asserted
audit_note: core-law block capture
claim_id: CLAIM-BL-0019
source_file: Agentic_Reasoning/README.DME.V2.ActiveMemoryRepoPolicy.md
line_range: 97-99
verbatim_span: The newest explicit user instruction wins. / The canonical repo governs stable doctrine. / Archived files preserve lineage only.
context_sensitive: false
use_mention_flag: asserted
audit_note: core-law block capture
claim_id: CLAIM-BL-0028
source_file: Agentic_Reasoning/README.DME.V2.ConceptualWorkflowContract.md
line_range: 777-777
verbatim_span: Projection doc must include token / embedding / symbol lifecycle.
context_sensitive: false
use_mention_flag: asserted
audit_note: modal shape-filtered BL
claim_id: CLAIM-BL-0037
source_file: Core/README.DME.V2.CoreArchitecture.md
line_range: 223-223
verbatim_span: Runtime may not crown candidates.
context_sensitive: false
use_mention_flag: asserted
audit_note: modal shape-filtered BL
claim_id: CLAIM-BL-0040
source_file: Core/README.DME.V2.FormalCorrespondenceLedger.md
line_range: 68-70
verbatim_span: Admit against definitions. /  / Theorem transfer is a separate, higher gate.
context_sensitive: false
use_mention_flag: unknown
audit_note: use_mention=unknown; core-law block capture
claim_id: CLAIM-BL-0069
source_file: Core/README.DME.V2.Glossary.md
line_range: 2180-2180
verbatim_span: Archive must preserve lineage and retrieval conditions.
context_sensitive: false
use_mention_flag: asserted
audit_note: modal shape-filtered BL
claim_id: CLAIM-BL-0088
source_file: Core/README.DME.V2.IdentityEnvelopeComposition.md
line_range: 323-325
verbatim_span: Hypothetical topology may guide exploration. /  / Only admitted topology may support identity claims.
context_sensitive: false
use_mention_flag: asserted
audit_note: core-law block capture
claim_id: CLAIM-BL-0153
source_file: Implementation_Orientation/Prototypes/README.DME.V2.LinguisticConfigurationHarness.md
line_range: 1612-1613
verbatim_span: Embedding similarity may suggest relation. / It may not admit distinction by itself.
context_sensitive: false
use_mention_flag: asserted
audit_note: core-law block capture
claim_id: CLAIM-BL-0182
source_file: Regime_Ecologies/README.DME.V2.AuthorityReferenceEcology.md
line_range: 847-847
verbatim_span: A reference without invalid-use boundaries is authority risk.
context_sensitive: false
use_mention_flag: asserted
audit_note: core-law block capture
claim_id: CLAIM-BL-0213
source_file: Regime_Ecologies/README.DME.V2.BudgetAdmissibilityEcology.md
line_range: 918-919
verbatim_span: Proof can support admissibility. / Proof does not replace admissibility.
context_sensitive: false
use_mention_flag: asserted
audit_note: core-law block capture
claim_id: CLAIM-BL-0272
source_file: Regime_Ecologies/README.DME.V2.ProjectionEcology.md
line_range: 1207-1207
verbatim_span: Unmanaged projection becomes future attention distortion.
context_sensitive: false
use_mention_flag: asserted
audit_note: core-law block capture
claim_id: CLAIM-BL-0291
source_file: Regime_Ecologies/README.DME.V2.RetentionEcology.md
line_range: 773-773
verbatim_span: Retained memory may re-enter only through scoped admissibility.
context_sensitive: false
use_mention_flag: asserted
audit_note: core-law block capture
claim_id: CLAIM-BL-0313
source_file: Regime_Ecologies/README.DME.V2.RuntimeRegimeLifecycle.md
line_range: 1122-1123
verbatim_span: Authority may become reference only under scope. / Reference may become canon only through governance and revocation conditions.
context_sensitive: false
use_mention_flag: asserted
audit_note: core-law block capture
claim_id: CLAIM-BL-0344
source_file: Substrates/README.DME.V2.ProjectionIndexRasterization.md
line_range: 954-954
verbatim_span: Every projection handle must preserve or reference a provenance envelope.
context_sensitive: false
use_mention_flag: asserted
audit_note: modal shape-filtered BL
```

## 7. Known v0.2 Limits

```text
v0.2 remains deterministic Structure + Ledger only
modal coverage is conservative and still syntax-bound
use_mention_flag resolves instrument/example contamination, not full pragmatics
context annotation preserves conditional meaning but does not resolve it
paraphrased non-collapse laws and inference-dependent claims remain out of scope
```

## 8. Non-Collapse Laws

```text
v0.2 improvement != semantic understanding
context annotation != resolved meaning
use_mention flag != deletion
related_to != depends_on
cleaner BL != doctrine truth
renumbering != transformation
crosswalk != deletion
merged entry != erased provenance
retired ID != forgotten claim
ID stability != semantic equivalence
```
