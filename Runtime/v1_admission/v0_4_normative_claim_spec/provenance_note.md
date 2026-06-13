# Provenance Note

## Provenance Asymmetry

```text
IndieWeb run:
  source hash: observed prefix only
  local CLI retrieval returned 401 stub
  source is not fully re-derivable from local CLI artifact
  use as partial-provenance baseline

12-Factor run:
  source hash: full live source hash recorded
  stronger reconstruction basis

Consequence:
  Future validation must not treat the two foreign baselines as equally anchored.
```

## Interpretation Rule

The IndieWeb run is still valid as runtime evidence of instrument pressure, but it is not equally strong as a reconstruction anchor. Any comparison or validation report built later should preserve that asymmetry explicitly rather than averaging it away.
