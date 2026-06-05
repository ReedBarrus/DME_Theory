# DME V2 — System Walkthrough

GitHub repository:
https://github.com/ReedBarrus/DME_Theory

```text
status: explanatory walkthrough / source-to-consequence trace / implementation orientation
depends_on:
  - README.DME.V2.TheoryFoundation.md
  - README.DME.V2.CoreArchitecture.md
  - README.DME.V2.ReadWriteTopology.md
  - README.DME.V2.OperatorGrammar.md
  - README.DME.V2.StructureSubstrate.md
  - README.DME.V2.RuntimeSubstrate.md
  - README.DME.V2.LedgerSubstrate.md
  - README.DME.V2.ProjectionIndexRasterization.md
  - README.DME.V2.RuntimeRegimeLifecycle.Hierarchical.md
  - README.DME.V2.DistinctionEcology.md
  - README.DME.V2.AgencyEcology.md
  - README.DME.V2.DecisionConsequenceEcology.md
  - README.DME.V2.ArchiveMigrationMap.md
schema posture: deferred
```

---

## 1. Purpose

This document walks through one concrete DME V2 lifecycle.

It shows how a source event becomes:

```text
structural support
→ distinction topology
→ runtime activation
→ projection
→ agentic attention
→ decision topology
→ execution
→ consequence
→ feedback
→ ledger provenance topology
→ future runtime curvature
```

This document is not a schema.

It is an orientation trace for understanding how the compressed DME V2 architecture operates as one coherent system.

---

## 2. Scenario

A local development environment is building a website.

A test runner emits a failure:

```text
Test failed:
Homepage navigation button does not route to /about.
Expected: /about
Actual: /about-us
```

The user’s active goal is:

```text
Build and stabilize the website navigation.
```

A local LLM/tool agent is available to inspect files, propose changes, and request execution.

DME is observing OS/runtime/tool events and coordinating source admission, runtime attention, projection, decision formation, execution, feedback, and provenance.

---

## 3. Compressed Walkthrough Chain

```text
NativeEmission
→ StructureSubstrate
→ DistinctionEcology
→ RuntimeSubstrate
→ Projection / ObserverFrame
→ AttentionEnvelope
→ CommitmentEnvelope
→ DecisionEnvelope
→ ExecutionCandidate
→ ExecutionReceipt
→ ConsequenceSignature
→ FeedbackRecord
→ IntegratedConsequenceRecord
→ Ledger / ProvenanceTopology
→ Retention / Proof / Authority modulation
→ LedgerCurvature
→ future Runtime
```

Core law:

```text
The system does not move from signal to action directly.
It moves through bounded distinctions, agentic attention, admissible decision topology,
accountable execution, consequence feedback, and provenance conservation.
```

---

## 4. Step 1 — NativeEmission

The test runner emits a native event.

```text
source: test_runner
event_type: test_failure
payload: homepage navigation button routes to /about-us instead of /about
context: website build/test loop
```

At this stage, the event is not yet a DME distinction.

It is source-native emission.

Non-collapse:

```text
source event ≠ distinction
test failure ≠ decision
error message ≠ proof
```

---

## 5. Step 2 — StructureSubstrate Admission

The Structure Substrate admits the source event.

Canonical chain:

```text
NativeEmission
→ SourceDeclaration
→ ProvenanceEnvelope
→ Normalize / Align
→ Parse / Decode
→ Window / Segment
→ Transform / Chart
→ CrossBasisMap
→ ExtractFeature / Observable
→ Detect / Stabilize
→ StructuralSignature
→ DistinctionEvidencePacket
→ StructuralAdmissibility
→ DistinctionRegion
→ RuntimeActivationCandidate
```

In this scenario:

```text
SourceDeclaration:
test_runner / local dev environment / current project

ProvenanceEnvelope:
source = test output
lens = test failure parser
loss = raw runner logs may be summarized
scope = current website build session

StructuralSignature:
navigation route mismatch

DistinctionEvidencePacket:
expected route differs from actual route

StructuralAdmissibility:
permit as DistinctionRegion
```

Output:

```text
DistinctionRegion:
homepage_nav_route_mismatch
```

Non-collapse:

```text
StructuralSignature ≠ DistinctionRegion
DistinctionRegion ≠ active runtime state
admissible ≠ true
```

---

## 6. Step 3 — DistinctionEcology

Distinction Ecology turns the admitted support into staged distinction geometry.

Lifecycle:

```text
RawDifference
→ DifferentialEvidence
→ StructuralSignature
→ DistinctionEnvelope
→ DistinctionEvidencePacket
→ StructuralAdmissibility
→ DistinctionRegion
```

For the test failure:

```text
RawDifference:
actual route differs from expected route

DifferentialEvidence:
expected /about, actual /about-us

StructuralSignature:
route_mismatch_signature

DistinctionEnvelope:
bounded support field around route mismatch

DistinctionRegion:
homepage_nav_route_mismatch
```

The distinction carries:

```text
source refs
test runner provenance
window/session
expected/actual values
uncertainty
projection eligibility
decision relevance
proof burden
release condition
```

This distinction is not yet action.

It is an accountable unit of attention, relation, projection, proof, decision, and consequence.

Non-collapse:

```text
distinction ≠ token
distinction ≠ proof
distinction ≠ authority
salience ≠ support
```

---

## 7. Step 4 — RuntimeSubstrate Activation

Runtime receives the DistinctionRegion as a RuntimeActivationCandidate.

Runtime asks:

```text
Should this admitted distinction become active now?
With what attention budget?
Under what local frame?
With what projection, retention, proof, and decision routes?
```

Runtime activates it as:

```text
Distinction-State:
active homepage_nav_route_mismatch
```

It enters a LocalFrame:

```text
LocalFrame:
current website build/test loop
```

A FieldProfile forms:

```text
attention pressure: high
decision relevance: high
proof tension: medium
retention need: medium
authority ceiling: local reversible file edit only
```

Runtime detects relation candidates:

```text
homepage component
router config
navigation button
prior test failure
current goal: stabilize website navigation
```

Non-collapse:

```text
active ≠ true
salient ≠ globally important
decision pressure ≠ execution
```

---

## 8. Step 5 — Projection / ObserverFrame

Projection makes selected runtime topology addressable.

DME projects the active distinction to the user/LLM/tool agent as a view.

```text
ProjectionHandle:
route_mismatch/homepage_nav_button

DashboardView:
Homepage nav button routes to /about-us; test expects /about.

AgentReadPacket:
active distinction + supporting test output + related files + uncertainty + allowed handles
```

Projection declares:

```text
source: test runner
lens: summarized route mismatch
loss: full raw logs not shown unless requested
allowed response handles: inspect files, propose patch, simulate patch
blocked response handles: direct deploy, external write
```

Non-collapse:

```text
projection ≠ source
handle ≠ topology
dashboard ≠ reality
```

---

## 9. Step 6 — AgencyEcology and AttentionEnvelope

The local LLM/tool agent receives an ObserverFrame and ProjectionAccessProfile.

It attends to the projected mismatch.

Agency forms an AttentionEnvelope:

```text
AttentionEnvelope:
agentic_locus = local_llm_tool_agent
target = homepage_nav_route_mismatch
projection = route_mismatch/homepage_nav_button
salience = high
budget = local debugging session
provenance = test runner output
uncertainty = low/medium
allowed handles = inspect, compare, propose, simulate
blocked handles = deploy, external send
```

The AttentionEnvelope prevents collapse:

```text
agent sees projection
→ salience spikes
→ request forms
→ intention pressure forms
```

The envelope preserves:

```text
this attention is bounded
this projection is partial
this action is not yet permitted
this salience does not authorize execution
```

Non-collapse:

```text
attention ≠ intention
attention ≠ permission
attention ≠ authority
```

---

## 10. Step 7 — CommitmentEnvelope

The user has an active goal:

```text
GoalProjection:
website navigation is correct and tests pass
```

A CommitmentEnvelope may exist:

```text
CommitmentEnvelope:
agentic_locus = user / development workflow
goal = stabilize website navigation
scope = current website project
budget = local dev session
decision relevance rules = test failures affecting navigation are relevant
feedback condition = tests pass / user review
repair path = revert patch or adjust route
revocation path = user cancels goal or changes expected route
```

This commitment pressures decision topology:

```text
CommitmentEnvelope
+ DecisionRelevance
+ AttentionEnvelope
+ Budget / Admissibility
→ DecisionPressure
```

Non-collapse:

```text
goal ≠ commitment
commitment ≠ authority
commitment ≠ permission
```

---

## 11. Step 8 — DecisionEnvelope

A DecisionEnvelope forms around possible transitions.

```text
DecisionEnvelope:
transition = fix homepage nav route mismatch
supporting distinctions = route mismatch, related file candidate
agentic pressure = user goal + LLM attention
authority ceiling = local reversible code edit
stake = project correctness / user time
consent = user approval required before file edit if not pre-authorized
consequence tier = C3 local reversible tool action
feedback path = rerun tests
repair path = revert or adjust patch
```

BranchTopology:

```text
branch A: change button route from /about-us to /about
branch B: change test expectation from /about to /about-us
branch C: inspect router config before patch
branch D: defer and ask user
branch E: release if test is stale
```

Simulation / Projection:

```text
simulate branch A:
likely fixes test if product requirement is /about

simulate branch B:
may pass test but could violate intended route

simulate branch C:
reduces uncertainty
```

Decision vector:

```text
high SimulateVector
medium ProofVector
medium ExecuteVector for local reversible inspection
low ExecuteVector for direct patch until file context is inspected
```

Non-collapse:

```text
decision ≠ execution
selected ≠ authorized
simulation ≠ reality
```

---

## 12. Step 9 — Admissibility / Consent / Authority Check

Before execution, DME checks transition constraints.

Admissibility:

```text
inspect files: permit
edit local file: permit_limited or ask_user depending policy
deploy externally: reject / blocked
```

Consent:

```text
user consent required for file edit unless current session grants local edit authority
```

Authority:

```text
agent authority ceiling:
read local files
propose patch
maybe edit local reversible files if allowed
cannot deploy
cannot send external messages
```

Non-collapse:

```text
available budget ≠ permission
consent ≠ blanket execution
authority ≠ decision
```

---

## 13. Step 10 — ExecutionCandidate and ExecutionReceipt

Assume the user approves a local reversible patch.

ExecutionCandidate:

```text
branch = change homepage nav button route to /about
target regime = filesystem
side effect tier = C3 local reversible tool action
authority ceiling = local patch only
reversibility = git diff / revert patch
feedback path = rerun tests
```

Execution occurs.

ExecutionReceipt records:

```text
actor = local_llm_tool_agent
approved_by = user / current session policy
branch = route change patch
target = file path
side effect tier = C3
provenance = DecisionEnvelope refs
reversibility = patch diff
```

Non-collapse:

```text
execution_candidate ≠ execution
execution ≠ proof
execution_receipt ≠ legitimacy
```

---

## 14. Step 11 — ConsequenceSignature

After execution, DME records what changed.

```text
ConsequenceSignature:
file edited
homepage nav route changed from /about-us to /about
affected object = homepage navigation component
affected agentic locus = user/dev workflow
reversibility = patch diff available
unexpected effects = unknown until tests
```

Non-collapse:

```text
execution success ≠ consequence success
change ≠ coherence
impact ≠ authority
```

---

## 15. Step 12 — FeedbackRecord

Tests are rerun.

Feedback returns:

```text
test runner result:
homepage navigation test passes
all navigation tests pass
```

FeedbackRecord:

```text
expected consequence = test passes
actual consequence = test passes
coherence delta = positive
rupture = none detected
repair need = low
```

Non-collapse:

```text
positive feedback ≠ legitimacy
feedback ≠ proof
feedback ≠ self-authorization
```

---

## 16. Step 13 — IntegratedConsequenceRecord

DME integrates the execution, consequence, and feedback.

IntegratedConsequenceRecord:

```text
execution = route patch
consequence = file route changed
feedback = test passed
coherence delta = positive under current test scope
retention posture = retain patch history and route mismatch repair pattern
proof tension = lowered for this local branch
authority impact = small positive trust evidence for local reversible code edits
reference potential = possible repair pattern, not canon
```

This updates:

```text
runtime pressure
ledger provenance topology
retention posture
proof tension
trust evidence
authority ceiling
projection state
commitment progress
```

Non-collapse:

```text
integration ≠ proof
trust evidence ≠ authority
reference potential ≠ reference
```

---

## 17. Step 14 — Ledger / ProvenanceTopology

Ledger folds the accountable lifecycle into provenance topology.

Records include:

```text
SourceReceipt
StructuralAdmissionReceipt
DistinctionRecord
RuntimeActivationRecord
ProjectionRecord
AttentionEnvelope reference
CommitmentEnvelope reference
DecisionRecord
ExecutionReceipt
ConsequenceSignature
FeedbackRecord
IntegratedConsequenceRecord
RetentionRecord
TrustEvidence
```

LedgerFold may create or update:

```text
CausalAttractor:
navigation_test_failure_repair_pattern

ReconstructionPath:
test failure
→ route mismatch distinction
→ attention envelope
→ decision envelope
→ patch execution
→ test feedback
→ integrated repair result
```

Non-collapse:

```text
ledger ≠ truth
receipt ≠ authority
reconstructable ≠ complete
```

---

## 18. Step 15 — Retention / Proof / Authority Modulation

Retention:

```text
retain route mismatch repair as echo-eligible pattern
do not keep active if tests remain stable
```

Proof:

```text
local test pass supports branch under current test scope
additional proof may be required before deploy
```

Authority:

```text
local agent gains small scoped trust evidence for reversible local patches
no authority granted for external deploy
```

Reference:

```text
repair pattern may become reference after repeated coherent use
not canon
```

Non-collapse:

```text
retention ≠ truth
proof ≠ authority
authority ≠ reference
reference ≠ canon
```

---

## 19. Step 16 — LedgerCurvature Back Into Runtime

Future runtime is curved by provenance topology.

If a similar route mismatch appears later, LedgerCurvature may return:

```text
prior repair path
similar distinction topology
known affected file type
test feedback history
authority ceiling recommendation
repair route
proof caution
```

Runtime may allocate attention more efficiently:

```text
recognize similar failure
project prior repair pattern
simulate likely patch
retain caution around route expectations
ask user if route semantics are ambiguous
```

Core law:

```text
Ledger topology may curve future runtime.
Ledger topology may not dictate consequence by itself.
```

---

## 20. Full Vehicle Chain

```text
NativeEmission
→ ProvenanceEnvelope
→ StructuralSignature
→ DistinctionEnvelope
→ DistinctionEvidencePacket
→ DistinctionRegion
→ RuntimeActivationCandidate
→ Distinction-State
→ ProjectionHandle / ObserverFrame
→ AttentionEnvelope
→ CommitmentEnvelope
→ DecisionEnvelope
→ BranchTopology
→ ExecutionCandidate
→ ExecutionReceipt
→ ConsequenceSignature
→ FeedbackRecord
→ IntegratedConsequenceRecord
→ ProvenanceTopology
→ LedgerCurvature
```

With the key envelope roles:

```text
ProvenanceEnvelope =
conserves identity through transformation.

DistinctionEnvelope =
bounds what difference is supported.

AttentionEnvelope =
bounds what a locus attends to through projection, salience, budget, belief,
uncertainty, and provenance.

CommitmentEnvelope =
bounds retained intention toward a desired goal across time.

DecisionEnvelope =
bounds what branch or transition may become consequential.
```

---

## 21. Full Non-Collapse Chain

```text
source event ≠ distinction
difference ≠ distinction
distinction ≠ attention
attention ≠ intention
intention ≠ permission
goal ≠ commitment
commitment ≠ authority
decision ≠ execution
execution ≠ consequence coherence
consequence ≠ legitimacy
feedback ≠ proof
trust ≠ authority
authority ≠ reference
reference ≠ canon
ledger ≠ truth
archive ≠ deletion
```

---

## 22. Final Compression

```text
DME does not move directly from data to action.

It admits source emissions into structural support,
forms bounded and provenanced distinctions,
activates them under runtime attention,
projects selected topology into agentic observer frames,
bounds attention through AttentionEnvelope,
preserves long-horizon intention through CommitmentEnvelope when needed,
forms DecisionEnvelopes around branch topology,
executes only permitted consequence-bearing branches,
records consequence and feedback,
integrates coherence deltas,
folds the lifecycle into Ledger / ProvenanceTopology,
and lets retained, provenanced history curve future runtime without dictating it.
```

Final anchor:

```text
The DME system lifecycle is accountable distinction recursion from source signal to consequence feedback.
```
