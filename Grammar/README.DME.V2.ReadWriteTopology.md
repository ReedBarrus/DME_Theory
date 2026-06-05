# DME V2 — Read / Write Topology

https://github.com/ReedBarrus/DME_Theory

```text
status: topology grammar / architecture bridge / pre-operator grammar
depends_on:
  - README.DME.V2.TheoryFoundation.md
  - README.DME.V2.CoreArchitecture.md
  - README.DME.V2.ConceptualWorkflowContract.md
schema posture: deferred
```

---

## 1. Purpose

This document defines the read/write topology of DME V2.

It explains how DME couples:

```text
configuration topology
↔
attentional topology
```

through:

```text
projection
decision
execution
feedback
integration
ledgering
retention
proof
authority
```

The Core Architecture defines the four primary substrates:

```text
Structure
Runtime
Ledger
Projection / Index / Rasterization
```

This document defines the dynamic polarity that moves through them:

```text
read-side configuration topology
write-side attentional topology
```

Operator Grammar should be written after this document, because operators define lawful movement across the read/write topology described here.

---

## 2. Core Thesis

```text
Read-side topology exposes configuration.
Write-side topology emits consequence.
Projection mediates reading.
Execution mediates writing.
Integrate closes the feedback loop.
Ledger records both.
Runtime dynamically couples both.
```

DME is not only a system that stores information.

DME is a system that governs how structures become visible, how visibility shapes attention, how attention forms decisions, how decisions emit consequence, and how consequence feeds back into future configuration.

---

## 3. Read-Side Configuration Topology

### 3.1 Definition

```text
Read-side configuration topology =
the organization of what can be observed, distinguished, mapped, queried, projected, compared, indexed, or understood under a declared lens.
```

Read-side topology answers:

```text
What exists as source?
What can be exposed as structure?
What can be distinguished?
What can be projected?
What can be compared?
What can be addressed?
What can be read by an agent, user, tool, or runtime?
```

### 3.2 Read-Side Chain

```text
source emission
→ structural admission
→ distinction evidence
→ distinction region
→ projection / index / rasterization
→ read packet / view / handle / token / embedding / symbol candidate
```

### 3.3 Read-Side Outputs

Read-side processes produce:

```text
StructuralObject
StructuralSignature
Feature
DistinctionEvidencePacket
DistinctionRegion
ProjectionObject
ProjectionHandle
ProjectionToken
EmbeddingRegion
SymbolCandidate
AgentReadPacket
DashboardView
```

### 3.4 Read-Side Boundary Law

```text
What can be read is not the same as what is true.
What can be projected is not the same as what exists.
What can be indexed is not the same as what is understood.
What can be named is not the same as what is proven.
```

---

## 4. Write-Side Attentional Topology

### 4.1 Definition

```text
Write-side attentional topology =
the organization of what becomes weighted, pressurized, selected, intended, executed, retained, proof-loaded, authorized, or released.
```

Write-side topology answers:

```text
What receives attention?
What becomes salient?
What branch is being pressured?
What intention is accumulating?
What consequence is forming?
What may be executed?
What feedback returns?
What future budget changes?
```

### 4.2 Write-Side Chain

```text
attention allocation
→ salience / pressure
→ decision topology
→ intention gradient
→ admissibility / consent
→ execution candidate
→ execution handle
→ consequence signature
→ environmental feedback
→ integrate
→ budget / retention / proof / authority modulation
```

### 4.3 Write-Side Outputs

Write-side processes produce:

```text
AttentionAllocation
CandidateTransition
DecisionNode
IntentionGradient
AdmissibilityDecision
ConsentState
ExecutionCandidate
ExecutionHandle
ConsequenceSignature
EnvironmentalFeedback
IntegratedConsequenceRecord
BudgetDelta
RetentionModulation
AuthorityDelta
```

### 4.4 Write-Side Boundary Law

```text
Attention is not consent.
Intention is not authority.
Execution is not proof.
Consequence is not legitimacy.
Feedback is not self-authorization.
```

---

## 5. The Four Substrates Under Read / Write Topology

Read/write topology does not replace the four substrates.

It describes how movement occurs through them.

---

## 5.1 Structure Substrate

### Read-side role

Structure receives source-native emissions and exposes configuration.

```text
source → structure → distinction evidence
```

Read-side structure asks:

```text
What can be exposed from the source?
What basis/lens is used?
What signatures are extracted?
What differences are supported?
```

### Write-side role

Structure may be affected by write-side consequences when execution modifies the source environment.

Examples:

```text
file edit changes future structural input
tool action changes runtime state
database write changes source state
sensor control changes physical input
language response changes future human input
```

Write-side structure asks:

```text
What source configuration changed because of consequence?
What new emissions will now appear?
What structural distinctions become possible or impossible?
```

### Boundary

```text
Structure exposes configuration.
Structure does not decide how consequence should be interpreted.
```

---

## 5.2 Runtime Substrate

### Read-side role

Runtime reads active distinctions, relations, pressures, and attractors.

```text
Distinction-State
→ FieldProfile
→ RelationCandidate
→ TopologyCandidate
```

Runtime read-side asks:

```text
What active topology is forming?
What distinctions are interacting?
What branches are possible?
What attractors are stabilizing?
```

### Write-side role

Runtime allocates attention and forms pressure toward decision and consequence.

```text
attention
→ decision pressure
→ intention gradient
→ execution candidate
```

Runtime write-side asks:

```text
What receives budget?
What branch is pressurizing?
What action-bearing topology is forming?
```

### Boundary

```text
Runtime may form candidates.
Runtime may not crown candidates.
```

---

## 5.3 Ledger Substrate

### Read-side role

Ledger provides recorded causal continuity.

```text
records
→ lineage
→ receipts
→ history
→ reference candidates
```

Ledger read-side asks:

```text
What happened?
What produced it?
What path did it take?
What was retained, proven, authorized, or revoked?
```

### Write-side role

Ledger receives records from consequence, integration, retention, proof, authority, and reference lifecycle.

```text
operator receipt
→ decision record
→ consequence signature
→ feedback record
→ integrated consequence record
```

Ledger write-side asks:

```text
What must be recorded?
What causal trace must be preserved?
What can be compressed?
What must remain reconstructable?
```

### Boundary

```text
Ledger records continuity.
Ledger does not decide truth or grant authority.
```

---

## 5.4 Projection / Index / Rasterization Substrate

### Read-side role

Projection makes topology addressable.

```text
runtime / ledger / structure refs
→ projection object
→ handle
→ token
→ embedding
→ symbol candidate
→ packet / view
```

Projection read-side asks:

```text
What view is exposed?
What handle addresses it?
What lens is applied?
What is omitted?
What uncertainty remains?
```

### Write-side role

Projection shapes future attention by controlling what agents, users, tools, and LLMs can see or respond to.

Projection write-side asks:

```text
What attention does this view induce?
What response handles are available?
What action pressure might this projection create?
What consequences are blocked?
```

### Boundary

```text
Projection is causally active but not execution.
Projection may shape pressure.
Projection may not become source, proof, authority, or canon.
```

---

## 6. Projection as Read Mediation

Projection is the primary mediation layer for read-side coupling.

It converts internal topology into:

```text
views
handles
tokens
embeddings
symbols
packets
dashboards
summaries
queries
agent-readable contexts
```

Projection allows actors to read the system without receiving the entire system.

It must declare:

```text
scope
lens
audience
preserved axes
omitted axes
loss
uncertainty
authority ceiling
allowed response handles
blocked response handles
expiry
revocation conditions
```

Projection is not passive.

A projection affects the next runtime by changing what an actor can attend to.

Core law:

```text
Projection changes attention conditions.
Projection does not itself authorize consequence.
```

---

## 7. Execution as Write Mediation

Execution is the primary mediation layer for write-side coupling.

Execution is not a full separate substrate.

Execution is the boundary where a decision branch emits effect into a target regime.

```text
decision branch
→ intention pressure
→ execution candidate
→ execution handle
→ target-regime effect
→ consequence signature
```

Target regimes may include:

```text
language
JSON
filesystem
shell
database
network
UI
tool runtime
agent runtime
governance surface
training export
physical environment
```

Execution must declare:

```text
target regime
side-effect level
scope
reversibility
stake
admissibility
authority ceiling
receipt requirement
feedback path
```

Core law:

```text
Execution emits consequence.
Execution does not prove consequence.
Execution success is not legitimacy.
```

---

## 8. Integrate as Feedback Closure

Integrate closes the read/write loop.

### 8.1 Definition

```text
Integrate reconciles emitted consequence with environmental feedback and updates future configuration, budget, trust evidence, access, retention, proof routing, and authority conditions.
```

### 8.2 Integration Chain

```text
consequence signature
→ environmental feedback
→ coherence delta
→ integrated consequence record
→ budget modulation
→ retention modulation
→ proof route
→ access / authority modulation
→ future projection and runtime pressure
```

### 8.3 Core Law

```text
Feedback may shape future pressure.
Feedback may not self-authorize consequence.
```

Integrate prevents the system from treating raw feedback as truth, authority, or canon.

---

## 9. Attention / Configuration Classes

The read/write topology requires classes of configuration and attention.

---

## 9.1 Configuration Classes

### Source Configuration

```text
configuration native to the source before DME transformation
```

Examples:

```text
raw OS event
audio waveform
file diff
language emission
tool response
sensor data
```

### Structural Configuration

```text
configuration exposed after admission, lensing, transformation, or feature extraction
```

### Distinction Configuration

```text
configuration organized as selectable difference under declared support
```

### Projection Configuration

```text
configuration rasterized into handles, tokens, embeddings, symbols, packets, or views
```

### Decision Configuration

```text
configuration organized as branches, possible transitions, rejected paths, realized paths, and consequence potentials
```

### Agentic Configuration

```text
configuration organized around loci of observation, attention, projection, intention, execution, memory, and feedback
```

### Reference Configuration

```text
configuration stabilized enough to guide future processing under declared scope
```

---

## 9.2 Attention Classes

### Sampling Attention

```text
attention used to select what source regions are processed
```

### Salience Attention

```text
attention used to amplify or prioritize active distinctions
```

### Projection Attention

```text
attention used to expose, rasterize, or render topology
```

### Decision Attention

```text
attention used to hold and compare possible branches
```

### Intention Attention

```text
budgeted write-side attention accumulating toward branch realization
```

### Retention Attention

```text
attention allocated to persistence, echo eligibility, recall, or decay
```

### Proof Attention

```text
attention allocated to challenge, perturbation, replay, reconstruction, and survival testing
```

### Execution Attention

```text
attention allocated to producing bounded consequence
```

### Governance Attention

```text
attention allocated to stake, access, authority, review, contestation, revocation, and canon lifecycle
```

---

## 10. Decision Space Across Read / Write

Decision space is the most important bridge between read-side and write-side topology.

Read-side decision space exposes:

```text
available branches
constraints
distinction support
risk
uncertainty
history
projection context
```

Write-side decision space forms:

```text
selection pressure
intention gradients
execution candidates
consequence potential
authority curvature
```

Decision space therefore includes:

```text
possible branches
rejected branches
simulated branches
realized branches
execution candidates
consequences
feedback
repair paths
authority gradients
```

Core law:

```text
A decision is not real merely because a branch exists.
A decision becomes realized when a branch emits consequence and is recorded.
```

---

## 11. Consent and Admissibility

### 11.1 Admissibility

```text
Admissibility is the general transition-permission field.
```

Admissibility determines whether a candidate transition may proceed.

It applies to:

```text
structural admission
runtime activation
projection exposure
memory re-entry
decision transition
execution handle
proof escalation
authority change
reference promotion
```

### 11.2 Consent

```text
Consent is a specialized agentic admissibility relation involving loci of agency, stake, consequence, and revocation.
```

Consent applies when a consequence may affect an agentic locus.

Consent requires:

```text
projection
understanding sufficient to scope consequence
stake visibility
boundary declaration
revocation path where applicable
authority ceiling
```

Consent is not mere agreement.

Consent is not permanent authority.

Consent is not valid if projected consequence differs materially from executed consequence.

---

## 12. Belief and Expectation in Read / Write Topology

Belief lives between read-side recurrence and write-side decision pressure.

### Expectation

```text
Expectation = anticipated recurrence.
```

Expectation forms when repeated distinctions create a predisposition to expect recurrence.

### Belief

```text
Belief = retained expectation topology associated with an agentic locus.
```

Belief shapes:

```text
what is noticed
what projections are trusted
what branches are considered
what risks are expected
what consent means
what intentions can form
```

Belief is not truth.

Belief is a decision-space prior.

---

## 13. Budget in Read / Write Topology

Budget drives recursion across the read/write continuum.

Budget determines:

```text
what gets sampled
what gets activated
what gets projected
what gets tokenized or embedded
what gets retained
what gets proof-loaded
what gets executed
what gets released
what gets authority
```

Budget is therefore the dynamic lens that prevents the system from blowing up, collapsing, or drifting.

Core law:

```text
A structure earns future budget when its recurrence regenerates coherence under feedback.
```

---

## 14. Authority in Read / Write Topology

Authority shapes write-side decision space.

```text
Authority = scoped, revocable consequence capacity.
```

Authority appears as:

```text
which branches may execute
which target regimes may be affected
which side-effect levels are allowed
which actors may request execution
which structures may become references
```

Authority is not arbitrary permission.

Authority is consequence budget earned through:

```text
coherence-regenerating execution history
feedback
trust evidence
stake accounting
proof where required
constraint preservation
revocation path
```

---

## 15. Reference in Read / Write Topology

Reference is authority stabilized into future guidance.

```text
Reference = stabilized authority-bearing configuration that future processes may use as a constraint, lens, handle, comparison basis, or decision support within declared scope.
```

Reference feeds back into read-side topology as a stable comparison object.

It also affects write-side topology by shaping future decisions.

Core law:

```text
Authority may become reference only under scope.
Reference may become canon only through governance.
Canon remains revocable.
```

---

## 16. Main Read / Write Loop

The full loop:

```text
source configuration
→ structural configuration
→ distinction configuration
→ runtime attention
→ projection configuration
→ agentic reading
→ decision configuration
→ intention attention
→ admissibility / consent
→ execution
→ consequence
→ environmental feedback
→ integrate
→ ledger record
→ retention / proof / authority modulation
→ reference update
→ future source/runtime/projection conditions
```

Compressed:

```text
read
→ attend
→ decide
→ write
→ receive feedback
→ integrate
→ recurse
```

---

## 17. Non-Collapse Laws

```text
read ≠ write
projection ≠ execution
attention ≠ consent
intention ≠ authority
decision ≠ consequence
execution ≠ proof
feedback ≠ truth
integration ≠ self-authorization
admissibility ≠ proof
consent ≠ agreement
access ≠ authority
authority ≠ reference
reference ≠ canon
```

---

## 18. Relationship to Operator Grammar

This document defines the topology.

Operator Grammar defines lawful movement through this topology.

For example:

```text
Expose
makes configuration available to read-side processing.

Select
bounds what receives attention.

Transform
moves configuration through a basis or lens.

Compare
creates contrast, invariance, or evidence.

Project
rasterizes topology into view-space.

Record
writes causal trace into ledger.

Echo
returns retained trace into runtime.

Commit
stabilizes under declared scope.

Release
removes, decays, or quarantines active pressure.

Integrate
closes consequence-feedback into future topology.
```

Operator Grammar should preserve the read/write distinction defined here.

---

## 19. Final Compression

```text
Read-side topology is the geometry of what can be seen, distinguished, projected, and addressed.

Write-side topology is the geometry of what can be attended, intended, executed, and integrated.

Projection turns read-side topology into handles.
Execution turns write-side pressure into consequence.
Integrate returns consequence to configuration.
Ledger records the path.
Runtime couples the whole loop through attention.
```

Final anchor:

```text
DME is a read/write topology over configuration and attention,
where every act of seeing may shape future action,
and every act of consequence must return through feedback, record, budget, and constraint.
```
