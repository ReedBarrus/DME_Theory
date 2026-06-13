# Runtime v1 Admission

```text
status: runtime scaffold / non-doctrine admission planning layer / instrument-binding only
scope: scaffold only; no product deployment; no external deployment
schema posture: deferred
```

v1 runtime admission is not the DME engine.
It is the first live admission loop:
foreign input -> source anchor -> extraction/admission -> gate checks -> event trace -> maintainer review.

Hard boundaries:

```text
runtime output != doctrine
admission != canon
foreign input != source truth
instrument-binding != constitutional standing
event trace != proof
review != authority grant
```

v1 minimum loop:

```text
1. ANCHOR external input
2. EXTRACT or project claims
3. APPLY instrument-binding gates
4. EMIT event trace
5. REVIEW admission outcome
6. RECORD failures, blocked claims, and instrument gaps
```

Instrument-binding gates for v1:

```text
unverified != satisfied
candidate != invariant
hypothetical != admitted
projection != source
omitted != preserved
```

Gate profile note:

```text
The v1 instrument-binding gates are the ADMISSION-BOUNDARY laws,
not the governance laws.
Foreign input makes no authority claims; governance gates
do not grip it.
The admission boundary is what foreign input tests.
```

Expected healthy result:

```text
foreign claims admit at candidate / partially_admitted at best,
with most axes omitted - NOT at fully_admitted.
If foreign input reaches high admission status easily,
the boundary is not holding.
```

FCL-005 pressure:

```text
Runtime admission will create event traces.
Ledger reconstruction / observability should be opened after first runtime traces exist.
FCL-005 should precede FCL-004 because identity-invariance correspondence requires reconstructable traces from actual runtime transformation.
```
