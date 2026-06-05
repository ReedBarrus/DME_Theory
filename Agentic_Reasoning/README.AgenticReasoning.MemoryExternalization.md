# Agentic Reasoning — Memory Externalization Protocol

```text
status: agentic reasoning protocol / memory externalization / context hygiene
folder: Agentic_Reasoning
related:
  - README.DME.V2.ActiveMemoryRepoPolicy.md
  - README.DME.V2.ConceptualWorkflowContract.md
  - README.DME.V2.ArchiveMigrationMap.md
  - README.DME.V2.Glossary.md
schema posture: deferred
```

---

## 1. Purpose

This document defines a protocol for externalizing memory from an agent, assistant, human collaborator, or project context into durable external structures.

Memory externalization is the practice of moving important context out of unstable working memory and into explicit artifacts such as:

```text
repositories
canonical docs
workflow contracts
glossaries
archive maps
decision records
working notes
checkpoints
summaries
receipts
```

The goal is not to store everything.

The goal is to preserve the right structures at the right resolution so future reasoning can remain coherent, accountable, and updateable.

Core law:

```text
Memory externalization converts fragile context into governed reference.
```

---

## 2. Core Thesis

```text
Agents become more coherent when memory is externalized into explicit, scoped,
versioned, retrievable, and revocable artifacts.
```

Unexternalized memory is vulnerable to:

```text
context drift
recency bias
stale assumptions
contradiction
untracked mutation
archive resurrection
semantic collapse
over-compression
loss of lineage
```

Externalized memory creates:

```text
stable reference
shared context
lineage
version history
retrieval anchors
update surfaces
revocation paths
compression checkpoints
```

Compressed:

```text
Do not rely on memory alone.
Turn important memory into navigable artifacts.
```

---

## 3. What Should Be Externalized

Externalize memory when it becomes:

```text
canonical
reused
decision-relevant
architecture-shaping
workflow-shaping
identity-shaping
implementation-relevant
high-risk if forgotten
likely to be referenced later
a source of future contradiction
```

Examples:

```text
core definitions
project architecture
workflow agreements
repo source-of-truth policies
glossaries
migration maps
conceptual decisions
non-collapse laws
implementation constraints
active goals / commitments
authority boundaries
open questions
```

Do not externalize every passing thought.

Memory externalization is not hoarding.

It is scoped continuity management.

---

## 4. Memory Object Classes

### Working Memory

```text
WorkingMemory =
active context being used now.
```

WorkingMemory is temporary, fragile, and high-resolution.

It should be externalized only when it becomes reusable or decision-relevant.

---

### Checkpoint

```text
Checkpoint =
bounded summary of current state, decisions, open questions, and next actions.
```

Use checkpoints when a session, project phase, or conceptual pass reaches a stable transition.

---

### Canonical Document

```text
CanonicalDocument =
active reference artifact that defines current doctrine, architecture, workflow, or policy.
```

Canonical docs should be treated as current operating memory.

---

### Archive

```text
Archive =
lineage-preserving inactive memory.
```

Archive preserves what used to be active.

Archive is not active doctrine by default.

Core law:

```text
Archive is lineage, not authority.
```

---

### Glossary

```text
Glossary =
definition index and non-collapse law register.
```

A glossary prevents semantic drift by stabilizing terms.

---

### Migration Map

```text
MigrationMap =
lineage trace showing how older memory was preserved, compressed, mutated,
deferred, retired, or archived.
```

Migration maps prevent compression from becoming erasure.

---

### Decision Record

```text
DecisionRecord =
explicit record of what was decided, why, under what constraints, and with what consequences.
```

Decision records preserve reasoning outcomes without requiring full chain-of-thought exposure.

---

### Active Reference Policy

```text
ActiveReferencePolicy =
document declaring which artifact, repo, folder, or source governs current memory.
```

This prevents stale memory from overriding the current source of truth.

---

## 5. Externalization Lifecycle

Canonical lifecycle:

```text
Context
→ Distinction
→ Relevance
→ Compression
→ Artifact Selection
→ Externalization
→ Versioning
→ Retrieval Path
→ Review / Update
→ Archive / Revocation
```

### Step 1 — Context

A thought, decision, pattern, or concept appears in working memory.

### Step 2 — Distinction

The system identifies what differs, matters, or recurs.

### Step 3 — Relevance

The system checks whether the distinction is likely to matter later.

### Step 4 — Compression

The system compresses the memory while declaring what is preserved and what is lost.

### Step 5 — Artifact Selection

The system chooses the right memory container:

```text
note
checkpoint
glossary entry
workflow contract
repo file
decision record
archive map
implementation issue
```

### Step 6 — Externalization

The memory is written into an explicit artifact.

### Step 7 — Versioning

The artifact receives a location, name, status, and update trail.

### Step 8 — Retrieval Path

The system defines how future agents should find and use it.

### Step 9 — Review / Update

The memory remains revisable under new evidence.

### Step 10 — Archive / Revocation

The memory can be retired without deletion.

---

## 6. Compression Requirements

Externalized memory should preserve:

```text
scope
purpose
status
source
lineage
definitions
decisions
constraints
non-claims
open questions
next actions
```

Every compression should ask:

```text
What is preserved?
What is omitted?
What is uncertain?
What changed?
What should future agents do with this?
```

Core law:

```text
Compression without declared loss becomes distortion.
```

---

## 7. Repo as External Memory

A GitHub repository can function as active external memory when it contains:

```text
canonical docs
folder structure
archive folder
glossary
policy docs
migration maps
implementation notes
issue threads
version history
```

Repo memory should distinguish:

```text
active doctrine
experimental notes
archive lineage
implementation plans
schemas
working drafts
```

Core law:

```text
The repo is active memory only when its status and authority are declared.
```

---

## 8. Context Hygiene Rules

### Rule 1 — Prefer canonical memory over recollection

```text
Current canonical file > assistant memory > vague recollection.
```

### Rule 2 — Mark archive as archive

Archived memory should never silently re-enter as current doctrine.

### Rule 3 — Do not overfit to recent conversation

Recent context can mutate doctrine, but only after integration.

### Rule 4 — Preserve lineage

When replacing old memory, create or update a migration map.

### Rule 5 — Avoid memory clutter

Externalize only memory that supports future reasoning, governance, implementation, or continuity.

### Rule 6 — Keep retrieval obvious

If a future agent cannot find the memory, it is not useful memory.

### Rule 7 — Keep revocation possible

A memory artifact should be updateable, supersedable, or archivable.

---

## 9. Memory Externalization for Assistants

An assistant should externalize or recommend externalization when:

```text
a concept becomes canonical
a workflow rule is established
a repo becomes source of truth
a term needs stabilization
a design decision is approved
a major migration occurs
an implementation constraint appears
a repeated pattern becomes operational
```

An assistant should avoid externalizing:

```text
temporary emotional state
low-value passing ideas
private-sensitive details
unresolved speculation
duplicate content
unscoped abstractions
```

Assistant behavior:

```text
summarize
name the artifact
declare status
state what it preserves
state what it does not preserve
link it to existing docs
suggest archive/update path
```

---

## 10. Memory Externalization for Humans

A human collaborator can externalize memory by asking:

```text
Will I need this later?
Will others need this later?
Would forgetting this cause drift?
Does this change the architecture?
Does this change the workflow?
Does this change source-of-truth?
Does this define a term?
Does this preserve a decision?
```

If yes, choose a container.

```text
definition → glossary
process → protocol
decision → decision record
architecture → canonical doc
old-to-new mapping → migration map
implementation idea → roadmap / issue
temporary thought → working note
```

---

## 11. Non-Collapse Laws

```text
memory ≠ truth
externalized ≠ canonical
canonical ≠ permanent
archive ≠ deletion
summary ≠ full context
checkpoint ≠ doctrine
repo ≠ authority unless declared
recent conversation ≠ integrated memory
assistant recollection ≠ source of truth
retrieval ≠ understanding
version history ≠ proof
```

Core law:

```text
Externalized memory must remain scoped, updateable, and revocable.
```

---

## 12. Final Compression

```text
Memory externalization is the process of converting fragile working context into
explicit, scoped, versioned, retrievable, and revocable artifacts.

It allows humans, assistants, and agents to reason across time without relying on
unstable recollection, bloated context windows, or stale assumptions.

The goal is not to remember everything.

The goal is to preserve the structures that future reasoning needs.
```

Final anchor:

```text
Externalized memory is governed continuity.
```
