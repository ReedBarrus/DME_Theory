# DME V2 — Structural Admission Coordinate Mechanics

```text
status: implementation support / coordinate mechanics / pre-schema representation contract
canonical_repo: https://github.com/ReedBarrus/DME_Theory
folder: Implementation_Orientation
depends_on:
  - README.DME.V2.LinguisticConfigurationHarness.md
  - README.DME.V2.ModularMechanizationLadder.md
  - README.DME.V2.StructureSubstrate.md
  - README.DME.V2.RuntimeSubstrate.md
  - README.DME.V2.ProjectionIndexRasterization.md
  - README.DME.V2.LedgerSubstrate.md
  - README.DME.V2.DistinctionEcology.md
  - README.DME.V2.BudgetAdmissibilityEcology.md
  - README.DME.V2.FeedbackIntegrationEcology.md
  - README.DME.V2.LedgerProvenanceEcology.md
  - README.DME.V2.ProjectionEcology.md
  - README.DME.V2.Glossary.md
schema posture: pre-schema / representation contract
```

---

## 1. Purpose

This document defines the coordinate mechanics needed before schema construction for the DME Linguistic Configuration Harness.

It clarifies how root configuration surfaces, derived coordinate regimes, structural signatures, salience profiles, distinction volumes, runtime updates, projection, and provenance relate without collapsing into each other.

This document is not a formal schema.

It is the representation contract that the first schema should preserve.

Core purpose:

```text
Prevent schema collapse between:
configuration space,
derived chart space,
signature space,
distinction space,
runtime topology,
projection space,
semantic feedback,
and ledger provenance.
```

---

## 2. Core Thesis

```text
Structural admission begins with conserved configuration.
Derived coordinate regimes measure that configuration.
Signatures detect invariance.
Distinction updates apply convergence/divergence pressure to runtime distinction space.
Salience potential couples structural convergence to attention without becoming authority.
Projection later renders topology into symbolic meaning.
```

Compressed:

```text
Root configuration gives addressability.
Derived charts give measurements.
Signatures give invariance.
Salience gives activation pressure.
Distinction volumes give runtime locality.
Projection gives semantic access.
Ledger gives continuity.
```

Core law:

```text
Payloads do not become distinctions by default.
Payloads create admission frames.
Admission frames update distinction space.
```

---

## 3. Coordinate Space, Metric Geometry, and Graph Topology

DME should preserve a clean separation between coordinate space, metric geometry, and graph topology.

### Coordinate Space

```text
Coordinate space =
where units are addressable.
```

For language:

```text
symbol coordinates
span intervals
line/column coordinates
container regions
section paths
source offsets
```

Coordinate space answers:

```text
Where is this?
What address does it occupy?
What source coordinate supports it?
```

### Metric / Information Geometry

```text
Metric geometry =
how distances, densities, recurrence, neighborhoods, and transformation patterns
are measured across coordinates.
```

For language:

```text
distance between spans
frequency distribution
co-occurrence distance
boundary proximity
cluster density
cross-window recurrence
transformation persistence
```

Metric geometry answers:

```text
How close?
How dense?
How recurrent?
How stable?
How coupled?
How changed?
```

### Graph Topology

```text
Graph topology =
how admitted objects, signatures, distinctions, and runtime regions relate as nodes,
edges, hyperedges, and neighborhoods.
```

For language:

```text
span supports signature
signature supports evidence packet
distinction shares cluster with distinction
distinction co-occurs with distinction
distinction persists across window
distinction drifts toward another distinction
```

Graph topology answers:

```text
What relates?
How is support connected?
What topology is formed from admitted evidence?
```

### Non-Collapse

```text
coordinate space ≠ metric geometry
metric geometry ≠ graph topology
graph topology ≠ semantic meaning
semantic meaning ≠ authority
```

---

## 4. Root Configuration Surfaces

For the first linguistic harness, root configuration should remain simple and conserved.

Root conservation surfaces:

```text
SymbolicConfigurationChart
ContainerStructureChart
```

Distributed through both:

```text
Provenance / lineage bindings
UncertaintyProfile
```

Ingest record:

```text
NormalizationTransformReceipt
```

### Root Law

```text
Root charts conserve the admitted configuration field.
They do not interpret meaning.
```

---

## 4.1 SymbolicConfigurationChart

### Definition

```text
SymbolicConfigurationChart =
root conservation surface of a linguistic payload as a discrete ordered symbolic field.
```

It maps every admitted character/symbol as a source-addressable point.

At minimum, each symbol point should preserve:

```text
symbol_point_id
payload_id
symbol_index
symbol_value
raw_symbol_value
normalized_symbol_value
symbol_class
line
column
byte_offset / char_offset if available
previous_symbol_point_id
next_symbol_point_id
source_ref
normalization_receipt_ref
provenance_binding
uncertainty_profile
```

### Field Framing

The root linguistic chart acts like a symbolic configuration wave:

```text
all later span, boundary, recurrence, window, neighborhood, and relation structures
are derived measurements over this ordered symbolic field.
```

Schema-safe formulation:

```text
Language is admitted as a discrete symbolic configuration field.
DME derives field geometry from recurrence, distance, boundary, neighborhood,
and transformation measurements over that field.
```

### Non-Collapse

```text
symbol point ≠ lexical span
symbol sequence ≠ distinction
symbol field ≠ meaning
discrete symbolic field ≠ probabilistic field by default
```

---

## 4.2 ContainerStructureChart

### Definition

```text
ContainerStructureChart =
root conservation surface for non-semantic structure supplied by the source container.
```

For markdown, this may include:

```text
heading markers
heading levels
list markers
code fences
frontmatter markers
tables
links
block quotes
indentation
blank-line regions
line/block structure
```

For later source adapters, this may include:

```text
JSON paths
DOCX paragraph styles
HTML tags
PDF layout regions
Git commit metadata
file metadata
audio frame metadata
sensor stream metadata
OS event metadata
```

### Non-Collapse

```text
container structure ≠ semantic meaning
heading marker ≠ doctrine
formatting ≠ authority
container metadata ≠ source truth
```

---

## 4.3 Provenance / Lineage Bindings

### Definition

```text
Provenance / Lineage Bindings =
distributed coordinate bindings connecting every point, span, region, chart entry,
signature, evidence packet, distinction volume, projection, and ledger record back
to source origin, transformation path, loss, and uncertainty.
```

Provenance is not a root chart in the same way as symbolic or container structure.

It is the conservation binding across all layers.

At symbol level:

```text
symbol point → source file / byte offset / character offset / line / column
```

At span level:

```text
structural span → symbol point range / line range / container region
```

At signature level:

```text
signature → supporting spans / derived chart entries / thresholds / transform path
```

At distinction level:

```text
distinction evidence → convergent signatures / source spans / uncertainty / support level
```

At projection level:

```text
projection token/view → distinction volume / evidence / signatures / source refs / loss
```

### Non-Collapse

```text
provenance ≠ truth
provenance ≠ proof
provenance ≠ authority
provenance continuity ≠ semantic validity
```

---

## 4.4 NormalizationTransformReceipt

### Definition

```text
NormalizationTransformReceipt =
ingest provenance record describing how raw source became admitted configuration.
```

Normalization is not neutral.

It may include:

```text
encoding normalization
Unicode normalization
line-ending normalization
whitespace normalization
frontmatter extraction
code fence preservation
hidden character handling
markdown marker preservation
offset remapping
container metadata extraction
```

It should preserve:

```text
raw span refs
normalized span refs
transform applied
loss / no-loss declaration
offset mapping
uncertainty
timestamp
operator trace
```

### Non-Collapse

```text
normalization ≠ source
cleaned text ≠ raw text
preprocessing ≠ neutral
normalization receipt ≠ proof
```

---

## 5. AdmissionFrame

### Definition

```text
AdmissionFrame =
bounded source-local coordinate frame created when a payload enters structural admission.
```

The payload is not a distinction.

The payload creates an admission frame.

Distinctions form within, across, or from updates caused by admission frames.

An AdmissionFrame should preserve:

```text
admission_frame_id
payload_id
source_receipt_ref
raw_payload_ref
root_chart_refs
derived_chart_refs
admission_time
source scope
payload extent
symbol coordinate range
container regions
relation to prior frames if available
integration budget / attention bandwidth if available
uncertainty profile
```

### Generalized Definition

```text
AdmissionFrame =
bounded source-local coordinate frame defining the scope, extent, provenance,
and integration budget for admitted configuration evidence.
```

For language:

```text
symbolic length
line/block extent
container structure
```

For audio:

```text
temporal length
sample rate
frequency-band extent
```

For image/video:

```text
spatial or spatiotemporal extent
frame boundaries
```

For OS events:

```text
event window
source process
runtime context
```

### Non-Collapse

```text
payload ≠ distinction
admission frame ≠ runtime topology
admission frame ≠ semantic context
admission frame ≠ authority
```

---

## 6. Derived Coordinate Regimes

Derived coordinate regimes are measurement regimes over the root conservation surfaces.

They should be general enough to transfer across source families.

Canonical derived coordinate regimes:

```text
1. Locality Regime
2. Boundary Regime
3. Metric Regime
4. Density / Recurrence Regime
5. Neighborhood / Coupling Regime
6. Sequence / Transition Regime
7. Transformation Regime
8. Salience Potential Regime
```

For the first markdown harness, these correspond to the derived structural chart classes:

```text
Segmentation
Boundary
Position / Metric
Recurrence / Distribution
Neighborhood / Co-occurrence
Transformation / Perturbation
```

The salience potential regime is derived from convergence across the others.

---

## 6.1 Locality Regime

### Definition

```text
Locality Regime =
coordinate regime describing where structure appears and how it occupies bounded regions.
```

In language, locality may include:

```text
symbol coordinate locality
span locality
line locality
block locality
section locality
container locality
```

Questions:

```text
Where does this structure appear?
Is it localized or diffuse?
Does it occupy a bounded region?
```

Possible measurements:

```text
span interval
line range
container region
section path
local concentration
source-local support
```

Non-collapse:

```text
locality ≠ meaning
locality ≠ importance
source locality ≠ runtime locality
```

---

## 6.2 Boundary Regime

### Definition

```text
Boundary Regime =
coordinate regime describing where structure separates, begins, ends, changes phase,
or crosses into another region.
```

In language:

```text
heading boundary
line break
blank line
indent change
list marker
code fence
punctuation boundary
symbolic delimiter
container boundary
```

Questions:

```text
Where does local structure change?
Where is separation or transition marked?
What regions are bounded?
```

Non-collapse:

```text
boundary ≠ semantic category
boundary ≠ distinction by itself
boundary strength ≠ authority
```

---

## 6.3 Metric Regime

### Definition

```text
Metric Regime =
coordinate regime describing distance, interval, depth, and relative position.
```

In language:

```text
symbol distance
span distance
line distance
window distance
distance to boundary
section depth
container path distance
```

Questions:

```text
How close are structures?
How far apart are spans?
What is near a boundary?
What is the relative position of a region?
```

Non-collapse:

```text
near ≠ semantically related
distance ≠ meaning
position ≠ importance by itself
```

---

## 6.4 Density / Recurrence Regime

### Definition

```text
Density / Recurrence Regime =
coordinate regime describing repeated forms, distribution, concentration,
and recurrence stability.
```

In language:

```text
symbol frequency
lexical span frequency
n-gram frequency
section frequency
cross-window recurrence
burstiness
distribution shape
```

Questions:

```text
What repeats?
Where does it concentrate?
Does recurrence persist across regions?
Is recurrence local, global, or bursty?
```

Non-collapse:

```text
frequency ≠ importance
recurrence ≠ truth
repetition ≠ authority
```

---

## 6.5 Neighborhood / Coupling Regime

### Definition

```text
Neighborhood / Coupling Regime =
coordinate regime describing local co-presence, adjacency, co-occurrence,
and covariance among structures.
```

In language:

```text
adjacent symbols
adjacent spans
window co-occurrence
cluster density
boundary-adjacent clusters
repeated local neighborhoods
```

Questions:

```text
What appears together?
What clusters?
What covaries locally?
What neighborhoods recur?
```

Non-collapse:

```text
co-occurrence ≠ support
neighborhood ≠ semantic relation
cluster ≠ ontology
coupling ≠ causality
```

---

## 6.6 Sequence / Transition Regime

### Definition

```text
Sequence / Transition Regime =
coordinate regime describing order, succession, chain structure, and transition patterns.
```

In language:

```text
ordered lists
arrow chains
line ordering
paragraph ordering
repeated sequence forms
symbolic transition patterns
```

Questions:

```text
What follows what?
Does ordering persist?
Does the same sequence recur?
Does a transition form appear structurally?
```

Non-collapse:

```text
sequence ≠ causality
ordered appearance ≠ decision path
transition marker ≠ execution
```

---

## 6.7 Transformation Regime

### Definition

```text
Transformation Regime =
coordinate regime describing persistence, drift, split, merge, rupture, or loss across
normalization, versions, edits, summaries, perturbations, or other transformations.
```

In language:

```text
term rename
section movement
heading change
summary compression
span deletion
operator symbol mutation
paragraph reorder
file split / merge
```

Questions:

```text
What persists under transformation?
What drifts?
What ruptures?
What splits or merges?
What loss occurs?
```

Non-collapse:

```text
persistent ≠ true
changed ≠ invalid
rupture ≠ total failure
compression ≠ erasure unless loss removes reconstructability
```

---

## 6.8 Salience Potential Regime

### Definition

```text
SaliencePotential =
derived activation pressure produced when multiple structural coordinate regimes
converge on a locality, span, region, pattern, or distinction volume.
```

Salience potential is not attention.

Salience potential is not meaning.

Salience potential is not authority.

It answers:

```text
Where does the system have enough structural convergence to deserve runtime activation?
```

Core relationship:

```text
Structural convergence ≠ salience.
Structural convergence produces salience potential.
Attention allocates salience into active runtime.
```

### SalienceProfile

```text
SalienceProfile =
multi-axis activation profile over structural coordinate regimes.
```

Possible axes:

```text
locality_strength
boundary_strength
recurrence_strength
density_strength
neighborhood_coupling_strength
sequence_stability
transformation_persistence
novelty_strength
rupture_strength
cross_regime_convergence
provenance_fidelity
uncertainty_penalty
compressed_salience_score
```

The compressed score is optional and derived.

The real object is the multi-axis profile.

### Deterministic v1

For the first harness, salience should be deterministic.

It may be computed from:

```text
locality strength
boundary strength
recurrence density
neighborhood coupling
sequence stability
transformation persistence
novelty / rupture
provenance fidelity
uncertainty penalty
```

Do not make probability the root.

Probability or vector-space projections may be added later as derived projection/metric regimes.

### Non-Collapse

```text
salience potential ≠ attention
salience potential ≠ meaning
salience potential ≠ authority
compressed salience score ≠ distinction
high salience ≠ truth
low salience ≠ irrelevance
```

---

## 7. Structural Signatures

### Definition

```text
StructuralSignature =
detected invariance, persistence, deformation, recurrence, boundary, cluster,
or transition pattern across derived coordinate regimes.
```

Signatures are first-derivative invariance detections over derived chart regimes.

They are not meaning.

They are not distinctions.

They are evidence-bearing structural derivatives.

Initial signature families:

```text
RecurrenceSignature
BoundaryLocalitySignature
ClusterSignature
OperatorFormSignature
CrossWindowPersistenceSignature
DriftSignature
RuptureSignature
```

### Signature Role

Signatures serve five roles:

```text
compress raw chart data into structural evidence
detect stability across windows or frames
create topology relation candidates
support perturbation testing
conserve provenance of distinction admission
```

Core law:

```text
Charts measure.
Signatures stabilize.
Distinctions bind.
Topology relates.
Projection interprets.
```

Non-collapse:

```text
signature ≠ distinction
signature ≠ meaning
signature ≠ proof
signature convergence ≠ semantic truth
```

---

## 8. SignatureGraph

### Definition

```text
SignatureGraph =
relation graph among structural signatures, supporting spans, chart regimes,
source regions, and candidate distinction centers.
```

SignatureGraph tracks:

```text
which signatures support the same candidate
which signatures converge
which signatures diverge
which signatures conflict structurally
which signatures persist across windows
which signatures drift across versions
which signatures imply structural topology edges
```

SignatureGraph is the immediate precursor to distinction evidence.

Non-collapse:

```text
signature graph ≠ distinction topology
signature convergence ≠ semantic meaning
graph edge ≠ semantic relation
```

---

## 9. Distinction Origin

### Definition

```text
DistinctionOrigin =
source-local convergence locality where structural signatures first support a bounded
difference strongly enough to form distinction evidence.
```

Distinction origin is not usually a single point.

It is a provenance-supported locality.

It may include:

```text
origin_span_set
origin_signature_set
origin_boundary_context
origin_cluster_context
origin_admission_frame
origin_salience_profile
origin_uncertainty_profile
```

DistinctionOrigin answers:

```text
Where did this distinction first become structurally supportable?
```

Non-collapse:

```text
distinction origin ≠ label
distinction origin ≠ meaning
distinction origin ≠ single character by default
```

---

## 10. Distinction Locality

### Definition

```text
DistinctionLocality =
bounded region of configuration/runtime topology where a distinction is currently supported,
active, projected, or related.
```

Locality types:

```text
source locality
chart locality
signature locality
runtime locality
projection locality
ledger locality
```

### Source Locality

```text
where evidence appears in the payload or source frame
```

### Chart Locality

```text
where supporting measurements occur across derived coordinate regimes
```

### Signature Locality

```text
where signatures converge or diverge
```

### Runtime Locality

```text
where the distinction volume sits in active runtime topology
```

### Projection Locality

```text
where the distinction is rendered, queried, tokenized, or viewed
```

### Ledger Locality

```text
where the distinction history is recorded and reconstructable
```

Non-collapse:

```text
source locality ≠ runtime locality
runtime locality ≠ projection locality
projection locality ≠ semantic meaning
ledger locality ≠ active relevance
```

---

## 11. Distinction Volume

### Definition

```text
DistinctionVolume =
bounded region of configuration topology where structural support, salience,
locality, and provenance converge enough to become runtime-addressable.
```

A distinction is not a point.

A distinction is not a string label.

A distinction volume may include:

```text
origin locality
supporting spans
supporting signatures
signature graph neighborhood
convergence profile
divergence profile
salience profile
uncertainty profile
provenance bindings
relation edges
persistence state
projection eligibility
```

Refined core:

```text
Distinction volumes are bounded regions of configuration topology where structural
support, salience, locality, and provenance converge.
```

Non-collapse:

```text
distinction volume ≠ string label
distinction volume ≠ projection token
distinction volume ≠ meaning
distinction volume ≠ authority
```

---

## 12. DistinctionUpdate

### Definition

```text
DistinctionUpdate =
field update applied to runtime distinction topology from a new AdmissionFrame,
preserving convergence/divergence geometry, affected volumes, locality,
salience potential, provenance, and uncertainty.
```

A payload does not decide what a distinction is.

A payload applies pressure to distinction space.

Core formula:

```text
existing distinction topology
+ admitted structural evidence
+ provenance
+ convergence/divergence profile
= updated distinction topology
```

If it is the first payload:

```text
empty / seed runtime
+ first AdmissionFrame
= initial distinction configuration
```

DistinctionUpdate may preserve:

```text
admission_frame_id
affected_distinction_ids
new_candidate_ids
convergence_profile
divergence_profile
salience_delta
support_delta
locality_delta
topology_edge_delta
uncertainty_delta
provenance_refs
ledger_receipt_refs
```

### Update Modes

Update modes are descriptive outcomes, not agentic decisions:

```text
seed
create_candidate
extend
strengthen
weaken
split
merge
drift
rupture
quarantine
release
```

Core law:

```text
DistinctionUpdate = topology delta under provenance.
```

Non-collapse:

```text
distinction update ≠ agentic decision
update mode ≠ semantic judgment
merge ≠ semantic equivalence
split ≠ contradiction by itself
rupture ≠ total failure
```

---

## 13. RuntimeDistinctionField

### Definition

```text
RuntimeDistinctionField =
active structural topology of distinction volumes, salience profiles, relation edges,
provenance bindings, uncertainty, and update history.
```

At this stage, runtime is not agentic.

It is a structural distinction runtime.

It answers:

```text
What distinction volumes exist?
How are they structurally related?
What salience profiles are active?
Which relations persist under perturbation?
Which volumes deform, split, merge, or rupture?
What can be projected?
```

Runtime distinction topology may contain:

```text
DistinctionVolume nodes
structural relation edges
SignatureGraph references
SalienceProfiles
DistinctionUpdates
AdmissionFrames
ProjectionEligibility
LedgerReceipt refs
```

Non-collapse:

```text
runtime distinction field ≠ truth
active topology ≠ semantic authority
salience profile ≠ attention
projection eligibility ≠ meaning
```

---

## 14. Attention, Salience, and Bandwidth

Attention should not be introduced as agency yet.

But structural admission may need attention-like capacity constraints.

### SaliencePotential

```text
SaliencePotential =
structural activation pressure derived from convergence across coordinate regimes.
```

### Attention

```text
Attention =
budgeted activation of supported distinction topology.
```

At this stage, attention may be implemented as simple runtime allocation:

```text
max active distinction candidates
max relation edges
max salience threshold
max retained updates
max projection candidates
```

### AttentionBandwidth

```text
AttentionBandwidth =
available activation capacity for integrating admitted distinction evidence into runtime topology.
```

AttentionBandwidth may be declared per AdmissionFrame or runtime cycle.

Non-collapse:

```text
salience potential ≠ attention
attention ≠ agency
attention ≠ meaning
attention ≠ authority
attention bandwidth ≠ consent
```

---

## 15. Field Projection and Probability

The root symbolic configuration is deterministic and discrete in v1.

Probability is not the root.

A probabilistic or vector-space field may be added later as a derived projection/metric regime.

### ProbabilityFieldChart

```text
ProbabilityFieldChart =
derived chart estimating distribution, recurrence likelihood, novelty,
or expected persistence across a configuration field.
```

This is optional and deferred.

### Embedding / Vector Projection

```text
EmbeddingMetricProjection =
projection-level metric regime over admitted distinction topology for retrieval,
similarity, and neighborhood support.
```

Non-collapse:

```text
probability field ≠ root configuration
embedding ≠ meaning
vector similarity ≠ proof
distance-as-likelihood ≠ provenance
```

---

## 16. Context Integration Ordering

When a new payload enters an existing distinction context, the order should be:

```text
New Payload
→ AdmissionFrame
→ Root Conservation Surfaces
→ Derived Coordinate Regimes
→ Structural Signatures
→ SignatureGraph
→ Convergence / Divergence Profile
→ DistinctionUpdate
→ RuntimeDistinctionField update
→ LedgerReceipt
→ Projection update if eligible
```

This avoids premature semantic decision-making.

Possible structural outcomes:

```text
seed initial distinction field
create new candidate volume
extend existing volume
strengthen existing volume
weaken existing volume
split volume
merge volumes
mark drift
mark rupture
quarantine evidence
release candidate
```

Core law:

```text
A new payload updates distinction space by applying structural convergence/divergence
pressure under provenance.
```

---

## 17. Generalized Source-Family Transfer

The coordinate mechanics should transfer beyond language.

The generalized derived identities are:

```text
locality
boundary
metric distance
density / recurrence
neighborhood / coupling
sequence / transition
transformation persistence / drift / rupture
salience potential
```

For language:

```text
symbol/span locality
lexical recurrence
heading/boundary pressure
co-occurrence neighborhood
cross-window persistence
term drift
operator-form rupture
```

For audio:

```text
frequency band locality
amplitude density
rhythmic recurrence
onset boundaries
spectral neighborhoods
motif persistence
signal drift
transient rupture
```

For OS events:

```text
event locality
action recurrence
context boundary
app/window neighborhood
workflow sequence
task drift
failure rupture
```

Cross-source identity:

```text
supported locality under recurrence, boundary, neighborhood, transformation,
and salience potential.
```

Core law:

```text
Source families differ in root configuration.
Derived coordinate regimes provide transferable structural identities.
```

---

## 18. Pre-Schema Object Set

The first schema should preserve the following object boundaries:

```text
AdmissionFrame
SymbolicConfigurationChart
ContainerStructureChart
ProvenanceBinding
NormalizationTransformReceipt

CoordinateRegime
ChartEntry
StructuralSpan
ContainerRegion

StructuralSignature
SignatureGraph

DistinctionOrigin
DistinctionLocality
DistinctionVolume
DistinctionUpdate
RuntimeDistinctionField

SalienceProfile
AttentionBandwidth

ProjectionView
ProjectionToken
SymbolicFeedbackRecord

LedgerReceipt
```

Core chain:

```text
AdmissionFrame
→ Root Conservation Surfaces
→ Derived Coordinate Regimes
→ StructuralSignatures
→ SignatureGraph
→ DistinctionUpdate
→ RuntimeDistinctionField
→ ProjectionView
→ LedgerReceipt
```

---

## 19. Non-Collapse Laws

```text
payload ≠ distinction
admission frame ≠ runtime topology
source file ≠ linguistic payload
raw content ≠ admitted structure
normalized text ≠ raw text
preprocessing ≠ neutral

coordinate space ≠ metric geometry
metric geometry ≠ graph topology
graph topology ≠ semantic meaning

symbol point ≠ lexical span
symbol sequence ≠ distinction
symbol field ≠ meaning
container structure ≠ semantic meaning

span ≠ signature
signature ≠ distinction
signature graph ≠ distinction topology
signature convergence ≠ semantic truth

distinction origin ≠ label
distinction origin ≠ meaning
distinction origin ≠ single character by default

source locality ≠ runtime locality
runtime locality ≠ projection locality
projection locality ≠ semantic meaning

distinction volume ≠ string label
distinction volume ≠ projection token
distinction volume ≠ meaning
distinction volume ≠ authority

distinction update ≠ agentic decision
update mode ≠ semantic judgment
merge ≠ semantic equivalence
split ≠ contradiction by itself

salience potential ≠ attention
attention ≠ agency
attention ≠ meaning
attention ≠ authority
attention bandwidth ≠ consent

probability field ≠ root configuration
embedding ≠ meaning
vector similarity ≠ proof
distance-as-likelihood ≠ provenance

projection ≠ source
projection token ≠ distinction
semantic feedback ≠ structural authority
ledger receipt ≠ proof
```

---

## 20. Final Compression

```text
Structural Admission Coordinate Mechanics defines how DME moves from source-local
configuration into runtime distinction topology without semantic collapse.

A payload creates an AdmissionFrame.

Root conservation surfaces preserve the symbolic and container configuration.

Derived coordinate regimes measure locality, boundary, metric distance, recurrence,
neighborhood coupling, sequence, transformation, and salience potential.

Structural signatures detect invariance across those regimes.

DistinctionUpdate applies convergence/divergence pressure to the RuntimeDistinctionField.

DistinctionVolume is the bounded locality where structural support, salience,
provenance, and topology converge.

Projection renders meaning later.

Semantic feedback may update topology only through provenance-preserved integration.
```

Final anchor:

```text
Configuration is conserved.
Measurements are derived.
Invariance becomes evidence.
Salience creates activation pressure.
Distinctions update runtime topology.
Projection gives meaning access.
Provenance preserves continuity.
```
