# DME V2 — Architecture Compression Map

https://github.com/ReedBarrus/DynamicalMemoryEngine_V2

```text
status: restructuring plan / conceptual skeleton / pre-schema compression map
purpose: map current DME/RIFT documents into a smaller, theory-first architecture stack
schema posture: deferred
```

---

## 1. Purpose

This document maps the current DME/RIFT document ecology into a compressed conceptual architecture.

The goal is to reduce file sprawl without losing the living theory.

This map decides:

```text
what gets preserved
what gets merged
what gets mutated
what gets archived
what becomes a core substrate
what becomes a regime ecology
what becomes a lifecycle object
what should not become schema yet
```

The current restructuring priority is:

```text
conceptual skeleton first
minimal object anchors second
formal schema later
```

Schemas are intentionally deferred until the architecture is stable enough that schemas express the theory instead of bloating or prematurely freezing it.

---

## 2. Compression Principle

The architecture has matured from many parallel “fields” into a cleaner structure:

```text
4 primary substrates
+ operator grammar
+ read/write topology
+ runtime regime lifecycle
+ regime ecologies
+ glossary / non-collapse laws
```

The four substrates are:

```text
Structure
Runtime
Ledger
Projection / Index / Rasterization
```

The main dynamical spaces are:

```text
Distinction Space
Agentic Space
Decision Space
```

The major cross-cutting ecologies are:

```text
Admissibility
Retention
Proof
Budget / Constraint / Authority / Reference
Governance
```

The major lifecycle dynamics include:

```text
Expectation
Belief
Consent
Intention
Execution
Consequence
Feedback
Integrate
Rupture
Repair
Contestation
Revocation
Translation
Canon
Meta-reconciliation
```

These are not all equal-level substrates.

Most are regime/lifecycle dynamics distributed across the four primary substrates.

---

## 3. Proposed New Document Stack

### 00_CORE

```text
README.DME.V2.TheoryFoundation.md
README.DME.V2.CoreArchitecture.md
README.DME.V2.ConceptualWorkflowContract.md
README.DME.V2.GlossaryAndNonCollapseLaws.md
```

### 01_SUBSTRATES

```text
README.DME.V2.StructureSubstrate.md
README.DME.V2.RuntimeSubstrate.md
README.DME.V2.LedgerSubstrate.md
README.DME.V2.ProjectionIndexRasterization.md
```

### 02_GRAMMAR

```text
README.DME.V2.OperatorGrammar.md
README.DME.V2.ReadWriteTopology.md
README.DME.V2.RuntimeRegimeLifecycle.md
```

### 03_REGIME_ECOLOGIES

```text
README.DME.V2.AdmissibilityEcology.md
README.DME.V2.DecisionConsequenceEcology.md
README.DME.V2.AgencyEcology.md
README.DME.V2.RetentionEcology.md
README.DME.V2.ProofEcology.md
README.DME.V2.BudgetConstraintAuthorityReferenceLifecycle.md
```

### 04_IMPLEMENTATION_ORIENTATION

```text
README.DME.V2.MemoryEcologyAndImplementationWedges.md
README.DME.V2.LocalRuntimeGeometry.md
```

### 05_DEFERRED

```text
README.DME.V2.SchemaIndex.md
schemas/*
```

Schema elaboration is intentionally deferred.

Minimal object sketches may appear inside each conceptual document.

---

## 4. New Stack Responsibilities

## 4.1 CoreArchitecture

### Role

The top-level architecture overview.

### Preserves

```text
DME as generalized configuration-space memory ecology
RIFT as primitive/operator/field framing
four-substrate structure
source → structure → runtime → ledger → projection recursion
governed emergence
non-collapse law
```

### Mutates

The architecture is no longer presented as many equal fields.

It is presented as:

```text
Structure exposes.
Runtime activates.
Ledger records.
Projection rasterizes.
```

All other regimes are lifecycle/dynamical ecologies across these substrates.

### Should include

```text
core thesis
four substrates
main runtime loop
read/write topology summary
main regimes
minimum non-collapse laws
why DME is not just agent memory
why DME is not just a knowledge graph
why DME is not just a governance framework
```

---

## 4.2 GlossaryAndNonCollapseLaws

### Role

Controls term drift.

### Preserves

```text
projection ≠ source
structure ≠ meaning
runtime ≠ canon
proof ≠ authority
trust ≠ authority
access ≠ permission
agreement ≠ consent
reference ≠ canon
canon ≠ final truth
```

### Mutates

Terms become explicitly placed by substrate/regime/lifecycle role.

### Should include

```text
term definitions
non-claims
collapse warnings
minimal examples
```

---

## 4.3 StructureSubstrate

### Role

Explains how source-native material becomes lawful structure.

### Preserves from old docs

```text
Structural Admission Layer
Configurable Primitive Identity
primitive field theory elements
source family handling
native emissions
payload refs
transforms
charts
features
structural signatures
distinction evidence packets
```

### Mutates

Structural admission becomes the read-side entry of the four-substrate system, not a standalone universe.

### Core chain

```text
NativeEmission
→ PayloadRef
→ StructuralAdmission
→ Chart / Lens / Transform
→ StructuralSignature
→ Feature
→ DistinctionEvidencePacket
→ DistinctionRegion
```

### Minimal object anchors

```text
NativeEmission
StructuralObject
Chart
StructuralSignature
DistinctionEvidencePacket
DistinctionRegion
```

### Archive / retire

Duplicate primitive explanations that are re-expressed in CoreArchitecture or OperatorGrammar.

---

## 4.4 RuntimeSubstrate

### Role

Explains active distinction/attention dynamics.

### Preserves from old docs

```text
RuntimeMap
RuntimeManifoldDynamics
CoreContinuumThesis
active Distinction-State
local frame
attention-energy
field differentials
interference traces
relation candidates
topology candidates
runtime observables
```

### Mutates

Runtime becomes the dynamic substrate of active configuration-attention flux.

It does not own proof, authority, projection, or canon.

### Core chain

```text
DistinctionRegion
→ Distinction-State
→ LocalFrame
→ Attention Allocation
→ FieldProfile
→ InterferenceTrace
→ CandidateTransition
→ RelationCandidate
→ TopologyCandidate
→ Decision-pressure / proof-route / projection-route
```

### Minimal object anchors

```text
Distinction-State
LocalFrame
FieldProfile
InterferenceTrace
CandidateTransition
RelationCandidate
TopologyCandidate
RuntimeObservable
```

### Archive / retire

Any wording implying runtime can self-authorize, self-canonize, or become truth.

---

## 4.5 LedgerSubstrate

### Role

Explains how causal/temporal continuity is recorded.

### Preserves from old docs

```text
LedgerHypergraph
causal signatures
operator receipts
lineage
proof traces
governance records
retention records
projection records
authority records
```

### Mutates

Ledger becomes the static causal/temporal counterpart to active runtime.

Ledger records what became causally accountable; it does not simulate active dynamics.

### Core chain

```text
SourceRef
→ PayloadRef
→ OperatorReceipt
→ DistinctionRecord
→ DecisionRecord
→ Execution / Consequence Record
→ Feedback / Integrate Record
→ Retention / Proof / Authority / Reference Record
```

### Minimal object anchors

```text
LedgerRecord
CausalSignature
OperatorReceipt
DecisionRecord
ConsequenceSignature
IntegratedConsequenceRecord
RetentionRecord
ProofTrace
AuthorityRecord
ReferenceRecord
```

### Archive / retire

Any duplicate ledger explanation that exists in individual regime docs.

---

## 4.6 ProjectionIndexRasterization

### Role

Explains how internal topology becomes addressable, legible, tokenized, embedded, symbolized, queried, and exposed.

### Preserves from old docs

```text
ProjectionField
ProjectionIndexSubstrate
Language Kernel boundary ideas
agent read packets
projection loss / uncertainty
projection authority ceiling
index handles
```

### Mutates

Projection is now explicitly:

```text
governed rasterization of topology into addressable view-space
```

Projection owns the interface between DME and:

```text
tokens
embeddings
symbols
language packets
JSON packets
dashboards
LLM context
agent read surfaces
tool targeting
```

### Core chain

```text
Runtime / Ledger / Structure refs
→ ProjectionObject
→ ProjectionHandle
→ ProjectionToken
→ EmbeddingRegion
→ SymbolCandidate
→ LanguageOperatorPacket / DashboardView / AgentReadPacket
```

### Minimal object anchors

```text
ProjectionObject
ProjectionHandle
ProjectionToken
EmbeddingRegion
SymbolCandidate
SymbolObject
LanguageOperatorPacket
DashboardView
```

### Archive / retire

Older projection/index split docs become superseded by this unified rasterization treatment.

---

## 4.7 OperatorGrammar

### Role

Defines lawful movement between substrates, regimes, and lifecycle objects.

### Preserves from old docs

```text
RIFT OperatorFieldGrammar
PhaseOperators
ConservationInvariants
Transform/Compare/Project laws
Proof operator ideas
Integrate addition
```

### Mutates

Operators are no longer just field movements; they become regime-boundary grammar.

### Operators

```text
Expose
Select
Transform
Compare
Project
Record
Echo
Commit
Release
Integrate
```

### Core questions

```text
What operation occurred?
What regime boundary did it cross?
What was conserved?
What was lost?
What authority ceiling applied?
What receipt was produced?
```

### Archive / retire

Duplicate operator definitions scattered across old docs.

---

## 4.8 ReadWriteTopology

### Role

Defines the most important structural compression:

```text
read-side configuration topology
write-side attentional topology
```

### Preserves

```text
configuration topology
attention topology
projection as read-side mediation
execution as write-side mediation
ledger records both
runtime dynamically couples both
```

### Core model

```text
Read-side:
source → structure → distinction → projection

Write-side:
attention → intention → execution → consequence → integrate
```

### Important thesis

```text
Projection mediates reading.
Execution mediates writing.
Integrate closes the feedback loop.
```

### Minimal object anchors

```text
ProjectionObject
IntentionGradient
ExecutionCandidate
ConsequenceSignature
IntegratedConsequenceRecord
```

---

## 4.9 RuntimeRegimeLifecycle

### Role

Explains how lifecycle dynamics emerge across the four substrates.

### Preserves

```text
distinction
expectation
belief
decision
intention
agency
projection
consent
execution
consequence
feedback
integrate
retention
proof
authority
reference
canon
governance
```

### Mutates

These are not all peer-level regimes.

They are lifecycle states, pressure regimes, or object ecologies.

### Core chain

```text
Distinction
→ Expectation
→ Belief
→ Decision
→ Intention
→ Projection
→ Consent / Admissibility
→ Execution
→ Consequence
→ Feedback
→ Integrate
→ Retention / Proof / Authority
→ Reference / Canon
```

### Archive / retire

Any old document framing minor lifecycle dynamics as standalone equal fields unless they require standalone treatment.

---

## 4.10 AdmissibilityEcology

### Role

Explains transition permission before proof/authority.

### Preserves from old docs

```text
AdmissibilityField
StructuralAdmissionLayer overlap
possible ≠ admissible
admissible ≠ proven
admissibility decisions
quarantine / defer / allow-limited
consent as agent-decision admissibility
```

### Mutates

Admissibility becomes broader:

```text
transition permission under constraint, projection, consent, budget, and consequence tier
```

### Core chain

```text
CandidateTransition
→ AdmissibilityProfile
→ AdmissibilityDecision
→ allowed / limited / deferred / rejected / quarantined
```

### Minimal object anchors

```text
AdmissibilityProfile
AdmissibilityDecision
ConsentState
ConsentRecord
```

---

## 4.11 DecisionConsequenceEcology

### Role

Explains decision space as branch, intention, execution, consequence, feedback, and integration topology.

### Preserves from old docs

```text
DecisionTopologyMapping
ConsequenceEcology
intention gradients
execution handles
consequence signatures
feedback
Integrate
authority curvature over decision space
```

### Mutates

Consequence is not a separate peer regime.

It is the realized write-side topology of decision space.

Execution is not a full universe.

Execution is the boundary where a decision branch emits effect into a target regime.

### Core chain

```text
Distinction
→ CandidateTransition
→ DecisionNode
→ IntentionGradient
→ ExecutionCandidate
→ ExecutionHandle
→ ConsequenceSignature
→ EnvironmentalFeedback
→ IntegratedConsequenceRecord
```

### Minimal object anchors

```text
DecisionNode
TransitionEdge
IntentionGradient
ExecutionCandidate
ExecutionHandle
ConsequenceSignature
EnvironmentalFeedback
IntegratedConsequenceRecord
```

---

## 4.12 AgencyEcology

### Role

Explains agentic loci as stable observer/action/pressure regions, not sovereign subjects by default.

### Preserves from old docs

```text
AgencyField
agent authority separation
projection-bound agency
agent read packet
agent action receipts
tool scopes
agentic attractors
```

### Mutates

Agency is now understood as a stable locus across:

```text
projection
belief
intention
decision
execution
receipt
retention
authority budget
```

### Core chain

```text
Projection access
→ Belief / expectation topology
→ Intention pressure
→ Decision participation
→ Execution receipts
→ Feedback
→ Trust evidence
→ Access / authority modulation
```

### Minimal object anchors

```text
AgenticLocus
AgentReadPacket
AgentActionRequest
AgentActionReceipt
AccessProfile
AuthorityVector
```

---

## 4.13 RetentionEcology

### Role

Explains memory persistence, echo, decay, archive, and re-entry.

### Preserves from old docs

```text
RetentionField
echo eligibility
retention pressure
recurrence
decay
quarantine
archive
```

### Mutates

Retention is budgeted and interacts with projection handles, token/embedding rasterization, proof triggers, and access budgets.

### Core chain

```text
Ledger trace
→ RetentionCandidate
→ RetentionRecord
→ EchoEligibility
→ Re-entry through admissibility
→ Runtime support vector
```

### Minimal object anchors

```text
RetentionRecord
EchoEligibility
RetentionSupportVector
DecaySchedule
QuarantineRecord
```

---

## 4.14 ProofEcology

### Role

Explains proof as survival/load testing and budget escalation filter.

### Preserves from old docs

```text
Proof Ecology
ProofExecutionLayer
proof as survival under perturbation
detected ≠ proven
proven ≠ authorized
```

### Mutates

Proof is now explicitly a budget filter:

```text
Does this candidate deserve more retention, projection, access, authority, reference, or canon status?
```

### Core chain

```text
Candidate
→ ProofRequest
→ Load / Perturb / Replay / Reconstruct
→ Survival / Failure / Bifurcation
→ ProofTrace
→ Budget / Authority / Reference route
```

### Minimal object anchors

```text
ProofRequest
ProofTrace
ProofResult
LoadProfile
RuptureRecord
RepairPath
```

---

## 4.15 BudgetConstraintAuthorityReferenceLifecycle

### Role

Defines the metabolic law of recursion and authority-to-reference lifecycle.

### Preserves

```text
BudgetConstraintAuthorityReferenceLifecycle
coherence capacitance
resource-regenerating invariance
access budget
authority as consequence budget
reference
canon
sovereignty
```

### Mutates

AuthorityFieldGovernance folds into a broader lifecycle:

```text
budget → trust evidence → access → authority → reference → canon
```

### Core chain

```text
Constraint
→ Budget
→ CoherenceCapacitance
→ Proof
→ TrustEvidence
→ AccessBudget
→ AuthorityBudget
→ Reference
→ Canon
```

### Minimal object anchors

```text
BudgetVector
CoherenceCapacitanceProfile
TrustEvidence
AccessBudget
AuthorityBudget
ReferenceObject
CanonPosture
```

---

## 4.16 MemoryEcologyAndImplementationWedges

### Role

Keeps the market/product orientation separate from the core theory.

### Preserves

```text
Nexus comparison
agent memory as implementation specimen
DME execution memory
generalized memory ecology
```

### Mutates

This becomes an applied strategy doc, not a core architecture root.

### Use

```text
local agent memory comparison
implementation wedge selection
market-facing compression
```

---

## 4.17 LocalRuntimeGeometry

### Role

First practical implementation wedge.

### Preserves

```text
OS runtime events
LLM coupling
agentic attractors
local dashboard
tool-call/runtime feedback
execution memory dataset idea
```

### Mutates

This becomes the concrete development path:

```text
DME gives agents a nervous system for the local OS.
```

### Core chain

```text
OS events
→ structural admission
→ runtime distinctions
→ attractor formation
→ projection/dashboard
→ LLM/operator packet
→ execution feedback
→ integrate
```

---

## 5. Old Document Mapping

| Old / Current Doc | New Home | Preserve | Mutate | Archive / Retire |
|---|---|---|---|---|
| README.DME.V2.Architecture.md | CoreArchitecture | four-substrate root, overall system posture | compress around Structure/Runtime/Ledger/Projection | old overview after merge |
| README.DME.V2.RuntimeMap.md | RuntimeSubstrate + CoreArchitecture | full runtime sequence | become substrate/lifecycle chain | old sequence after integration |
| README.DME.V2.RuntimeManifoldDynamics.md | RuntimeSubstrate | active Distinction-State, attention, interference | clarify no proof/authority/canon emission | keep as source until merged |
| README.RIFT.CoreContinuumThesis.md | CoreArchitecture + RuntimeSubstrate | Ω(t), unified attentional continuum | make continuum active substrate, not all fields | keep as theory source |
| README.DME.V2.StructuralAdmissionLayer.md | StructureSubstrate | source-to-structure laws | merge with source family and distinction evidence | supersede after merge |
| README.DME.V2.AdmissibilityField.md | AdmissibilityEcology | possible/admissible/proven/authorized chain | include consent and consequence-tier gating | supersede after merge |
| README.DME.V2.DecisionTopologyMapping.md | DecisionConsequenceEcology | decision nodes, branches, failure/repair | include intention/execution/consequence as decision-space topology | supersede after merge |
| README.DME.V2.AgencyField.md | AgencyEcology | projection-bound agents, action receipts | agency as stable locus over projection/intention/execution | supersede after merge |
| README.DME.V2.RetentionField.md | RetentionEcology | echo, decay, retention pressure | budgeted retention and token/projection interaction | supersede after merge |
| README.DME.V2.LedgerHypergraph.md | LedgerSubstrate | causal hypergraph, receipts, records | ledger as static causal counterpart to runtime | supersede after merge |
| README.DME.V2.ProjectionField.md | ProjectionIndexRasterization | bounded view, loss, uncertainty, ceiling | projection as rasterization into tokens/embeddings/handles | supersede after merge |
| README.DME.V2.ProjectionIndexSubstrate.md | ProjectionIndexRasterization | index handles, routing, projection index | merge into rasterization layer | supersede after merge |
| README.DME.V2.ProofExecutionLayer.md | ProofEcology + LedgerSubstrate | proof execution traces | proof as budget filter and ledgered survival | supersede after merge |
| README.DME.V2RIFT.Proof Ecology.md | ProofEcology | proof ecology, survival under load | consolidate with proof budget role | supersede after merge |
| README.DME.V2.RIFT.AuthorityFieldGovernance.md | BudgetConstraintAuthorityReferenceLifecycle + AgencyEcology | authority vector, governance | authority as consequence budget, reference lifecycle | supersede after merge |
| README.RIFT.OperatorFieldGrammar.md | OperatorGrammar | operators and grammar | add Integrate, regime-boundary grammar | supersede after merge |
| README.DME.V2.RIFT.PhaseOperators.md | OperatorGrammar | phase transitions | consolidate operator set | supersede after merge |
| README.DME.V2.RIFT.ConservationInvariants.md | OperatorGrammar + BudgetConstraintAuthorityReferenceLifecycle | invariants | express as budget/conservation laws | keep as source until merged |
| README.RIFT.ConfigurablePrimitiveIdentity.md | StructureSubstrate + RuntimeRegimeLifecycle | primitive identity, identity under configuration | identity becomes persistence condition across regimes | merge and archive |
| README.DME.V2.RIFT.PrimitiveFieldTheory.md | CoreArchitecture + StructureSubstrate | primitives and field terms | compress into fundamental configuration geometry | archive after extraction |
| README.DME.V2.RIFT.ObservablesDetectorsStabilizers.md | StructureSubstrate + RuntimeSubstrate | observables, detectors, stabilizers | map as structure/runtime object classes | archive after extraction |
| README.DME.V2.RIFT.AuthorityFieldGovernance.md | BudgetConstraintAuthorityReferenceLifecycle | authority field | authority → reference → canon lifecycle | supersede |
| README.DME.V2.FeedbackEcology.md | DecisionConsequenceEcology + LocalRuntimeGeometry | feedback loops | integrate feedback as consequence return signal | merge |
| README.DME.V2.MetaRegimeReconcilliation.md | RuntimeRegimeLifecycle + Glossary + future Meta doc | meta-reconciliation | demote to meta-readiness for now | archive active implementation |
| README.RIFT.TranslationMap.md | ProjectionIndexRasterization + RuntimeRegimeLifecycle | translation across lenses | translate as projection/operator lifecycle dynamic | merge |
| README.RIFT.ThermodynamicOrderingBridge.md | BudgetConstraintAuthorityReferenceLifecycle + ReadWriteTopology | ordering, thermodynamic bridge | budget as thermodynamic/metabolic law | merge |
| README.DME.V2.MemoryEcologyAndImplementationWedges.md | ImplementationOrientation | implementation wedge strategy | keep as applied doc | keep |
| README.DME.V2.ConsequenceEcology.md | DecisionConsequenceEcology | consequence, integrate, trust/stake/access | consequence becomes realized decision topology | supersede/merge |
| README.DME.V2.BudgetConstraintAuthorityReferenceLifecycle.md | BudgetConstraintAuthorityReferenceLifecycle | budget, coherence capacitance, authority/reference | becomes central regime ecology doc | keep as current draft |

---

## 6. Concepts Being Promoted

The following concepts are promoted to core architecture:

```text
four substrates
read/write topology
projection as rasterization
tokens as handles
embeddings as coordinate lenses
symbols as proof-supported handle/distinction bindings
budget as dynamic constraint
coherence capacitance
authority as consequence budget
reference as stabilized authority-bearing configuration
canon as governed revocable reference
Integrate as feedback closure operator
consent as admissibility dynamics between agentic loci and consequence-bearing decisions
```

---

## 7. Concepts Being Demoted

The following concepts are demoted from standalone field status to lifecycle/object dynamics unless later needed:

```text
belief
expectation
agreement
consensus
rupture
repair
contestation
revocation
translation
meta-regime
```

They remain important, but they should not explode the doc stack.

---

## 8. Concepts Being Mutated

### Projection

Old:

```text
bounded view
```

New:

```text
governed rasterization of topology into addressable handles, tokens, embeddings, symbols, packets, and views
```

### Decision

Old:

```text
branch mapping
```

New:

```text
branch, intention, execution, consequence, feedback, and authority curvature topology
```

### Proof

Old:

```text
survival under perturbation
```

New:

```text
survival under load + budget escalation filter
```

### Authority

Old:

```text
bounded consequence permission
```

New:

```text
scoped consequence budget earned through coherence-regenerating feedback and stake/accountability
```

### Ledger

Old:

```text
causal structural memory substrate
```

New:

```text
static causal/temporal counterpart to active runtime, recording regime lifecycle history
```

### Runtime

Old:

```text
active manifold dynamics
```

New:

```text
active configuration-attention substrate where distinction, relation, decision, and attractor dynamics form
```

---

## 9. Schema Posture

Formal schema is deferred.

Current posture:

```text
theory-first
minimal object anchors
no exhaustive schemas
no large schema directory until conceptual skeleton stabilizes
```

Each conceptual doc may include small object sketches only where needed to clarify structure.

Do not create a standalone SchemaIndex until:

```text
the four substrate docs are stable
the operator grammar is stable
the regime lifecycle is stable
the main regime ecology docs are stable
implementation target is selected
```

---

## 10. Drafting Order

Recommended drafting order:

```text
1. CoreArchitecture
2. ReadWriteTopology
3. ProjectionIndexRasterization
4. StructureSubstrate
5. RuntimeSubstrate
6. LedgerSubstrate
7. OperatorGrammar
8. RuntimeRegimeLifecycle
9. DecisionConsequenceEcology
10. BudgetConstraintAuthorityReferenceLifecycle revision
11. AdmissibilityEcology
12. AgencyEcology
13. RetentionEcology
14. ProofEcology
15. GlossaryAndNonCollapseLaws
16. LocalRuntimeGeometry
```

Rationale:

```text
CoreArchitecture gives root.
ReadWriteTopology gives global dynamic grammar.
ProjectionIndexRasterization locks the token/embedding/symbol breakthrough.
Then the substrates can be rewritten coherently.
Then operators and lifecycle regimes can be reconciled.
Then individual ecologies can be stabilized.
```

---

## 11. Success Criteria

The compression succeeds if the new architecture can explain:

```text
how source becomes structure
how structure becomes distinction
how distinction becomes active runtime
how active runtime becomes projected handles
how handles become language/operator packets
how decisions form
how intention pressures execution
how consequence feeds back
how budget regulates recursion
how authority becomes reference
how reference becomes canon
how agents gain bounded access
how humans retain sovereignty
```

without requiring 25 parallel fields.

---

## 12. Final Anchor

```text
DME is not a pile of regimes.

DME is a four-substrate configuration-attention architecture
whose lifecycle regimes describe how structure becomes active,
addressable, consequential, retained, proof-loaded, authoritative,
and eventually reference-stable without collapsing projection into truth
or consequence into legitimacy.
```
