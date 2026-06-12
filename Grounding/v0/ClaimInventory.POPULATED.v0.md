# DME V2 — Claim Inventory (POPULATED, v0)

```text
status: grounding instrument / POPULATED
source_snapshot: theory-v2.0-pre-grounding
extraction_method: extractor v0.1, deterministic pattern grammar
  per Implementation_Orientation/README.DME.V2.LanguageAdmissionPrototype.md
population_status: populated — derived record, append-only
ledger_file: claim_inventory.jsonl (canonical; this doc is a projection of it)
```

## 1. Run Summary

```text
corpus: 37 active-doctrine files
  included: Core, Grammar, Substrates, Regime_Ecologies,
            Agentic_Reasoning, Implementation_Orientation,
            README.md, MEMORY_INDEX.md
  excluded: Archive (active != archive), Meta_Web_Gov_Hub (non-DME)

total entries:          3878
  NC    2723
  DEF    443
  BL     378
  DEP    309
  OP      25

unique NC laws:         1408  (of 2723 NC entries)
duplicated NC laws:     559
cross-entry recurrent terms: 804
arrow chains rejected (non-operator vocab): 262

status ceiling honored: all entries partially_admitted
evaluated_axes: Distinction, Ledger only — all others omitted
```

## 2. Most Recurrent Terms (cross-document)

```text
authority                                   376 entries / 31 files
proof                                       260 entries / 31 files
truth                                       166 entries / 31 files
consent                                     104 entries / 24 files
distinction                                  98 entries / 20 files
canon                                        84 entries / 23 files
permission                                   76 entries / 19 files
reference                                    72 entries / 22 files
execution                                    68 entries / 21 files
legitimacy                                   65 entries / 21 files
source                                       64 entries / 22 files
attention                                    60 entries / 13 files
meaning                                      60 entries / 17 files
projection                                   58 entries / 23 files
deletion                                     49 entries / 20 files
intention                                    42 entries / 12 files
feedback                                     42 entries / 18 files
decision                                     37 entries / 14 files
trust                                        36 entries / 13 files
identity                                     34 entries / 15 files
```

## 3. Most Repeated Non-Collapse Laws (verbatim)

```text
 23x  projection != source
 20x  embedding != meaning
 20x  trust != authority
 19x  proof != authority
 16x  reference != canon
 15x  feedback != proof
 14x  canon != final truth
 14x  ledger != truth
 13x  attention != intention
 13x  archive != deletion
 13x  decision != execution
 12x  execution != proof
 12x  receipt != authority
 12x  attention != consent
 11x  authority != truth
 11x  token != distinction
 11x  authority != reference
 11x  feedback != truth
 10x  access != authority
 10x  echo != proof
```

## 4. Claim Density by Document (top 12)

```text
  443  Core/README.DME.V2.Glossary.md
  223  Regime_Ecologies/README.DME.V2.AuthorityReferenceEcology.md
  189  Implementation_Orientation/Dynamics/README.DME.V2.StructuralAdmissionCoordinateMechanics.md
  187  Regime_Ecologies/README.DME.V2.FeedbackIntegrationEcology.md
  182  Implementation_Orientation/Prototypes/README.DME.V2.LinguisticConfigurationHarness.md
  179  Regime_Ecologies/README.DME.V2.AgencyEcology.md
  179  Regime_Ecologies/README.DME.V2.ProjectionEcology.md
  179  Regime_Ecologies/README.DME.V2.ProofEcology.md
  174  Regime_Ecologies/README.DME.V2.BudgetAdmissibilityEcology.md
  167  Grammar/README.DME.V2.OperatorGrammar.md
  167  Regime_Ecologies/README.DME.V2.LedgerProvenanceEcology.md
  159  Regime_Ecologies/README.DME.V2.RetentionEcology.md
```

## 5. Known v0 Limits (declared)

```text
BL-modal class carries fragment noise (~unverified rate; see samples)
prose definitions without '=' markers: missed
paraphrased non-collapse laws: missed
262 non-operator arrow chains (lifecycle/flow chains) excluded:
  evidence that v1 needs a FlowChain claim class
```

## 6. Non-Collapse

```text
inventory != doctrine
entry != endorsement
recurrence != importance
extracted != true
```
