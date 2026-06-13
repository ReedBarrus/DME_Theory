# Instrument Gap Report

```text
status: instrument gap report / second foreign input feedback
gap: v0.3 lacks NormativeClaim chart basis
instrument: v1_admission_wrapper
```

## A. Finding

```text
The second foreign input confirms the NormativeClaim gap observed in the IndieWeb run.

The Twelve-Factor App expresses technical operational principles as directives, prohibitions, and scoped norms rather than DME-style distinction assertions.

Existing v0.3 classes DEF/NC/BL/OP/DEP do not adequately type the directive content of the factors.
```

## B. Candidate Receptor, Not Implemented

```text
NormativeClaim candidate shape:

actor:
  often explicit or implied, such as app, developer, service, deploy, process

polarity:
  SHOULD / SHOULD NOT / MUST / MUST NOT

action:
  the directive operation

scope:
  the envelope in which the directive applies

rationale:
  the reason or consequence basis, often explicit in 12-Factor and often elided in IndieWeb
```

## C. Polarity Bridge Finding

```text
The second source forces a polarity field.

Prohibitive directives such as "never store config in code" bridge directly toward DME-style non-collapse claims:

foreign directive face:
  actor SHOULD NOT store config in code

distinction face:
  config != code

shared latent form:
  actor SHOULD NOT treat A as B WITHIN scope BECAUSE rationale
```

## D. Reflexive Finding

```text
A non-collapse law is a NormativeClaim with elided actor, polarity, action, scope, or rationale.

"A != B" may unfold to:
"do not treat A as B, because they differ."

This does not make the two forms identical.
It identifies a candidate shared chart basis across distinction assertions and directive norms.
```

## E. Non-Collapse

```text
normative principle != DME doctrine
imperative text != admitted law
foreign value != DME canon
untyped norm != extraction failure
instrument gap != theory failure
thin wrapper finding != full v0.3 extractor capability
NormativeClaim receptor != doctrine mutation
shared chart basis != identity claim
polarity bridge != theorem transfer
```

## F. v0.4 Pressure

```text
v0.4 pressure confirmed:
Two foreign inputs, IndieWeb Principles and The Twelve-Factor App, both surface directive/normative content that v0.3 cannot type cleanly.

The evidence now supports authoring a v0.4 NormativeClaim chart-basis specification as an instrument capability candidate.

This does NOT authorize doctrine mutation, canon admission, or automatic activation.
```
