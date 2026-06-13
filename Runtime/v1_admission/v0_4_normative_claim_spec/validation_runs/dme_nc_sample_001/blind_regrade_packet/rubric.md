# Blind Regrade Rubric

```text
For each NC law, determine whether the following fields can be recovered without invention:

actor:
  recovered only if named, structurally implied, or locally licensed
  otherwise null / elided

polarity:
  SHOULD_NOT only if the surface clearly supports non-collapse / do-not-treat-as
  UNKNOWN if interpretive invention is required

action:
  may be "treat_as", "collapse_with", "confuse_with", or equivalent only if supported by source wording

object:
  left side of NC relation if recoverable

comparison_or_target:
  right side of NC relation if recoverable

scope:
  recovered only if present in source text or immediate local context
  otherwise null

rationale:
  recovered only if present in source text or immediate local context
  otherwise null

invented_fields:
  any field populated beyond source text or local context

projection_status:
  projected = polarity/action/object/target recover without invention
  partial = only some fields recover
  failed = projection requires invention or loses source distinction
```

## Falsification Note

```text
A result with many null actor/scope/rationale fields should not be rounded up to a rich bridge.
Empty fields are evidence.
```
