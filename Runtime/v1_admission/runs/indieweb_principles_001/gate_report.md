# Runtime v1 Admission Gate Report

```text
status: runtime v1 admission gate report
input: IndieWeb Principles
scope: instrument-binding only
instrument: v1_admission_wrapper
doctrine_mutation: none
authority_grant: none
```

## Summary

```text
claims_processed: 11
admission_status_distribution:
  candidate: 11
  partially_admitted: 0
  fully_admitted: 0
typed_projection_count:
  NORM_CANDIDATE_UNTYPED: 9
  BL: 2
```

## Gates Applied

```text
unverified != satisfied
candidate != invariant
hypothetical != admitted
projection != source
omitted != preserved
```

## Omitted Axes

```text
authority
authorization
feedback
perturbation
cross_basis_convergence
```

## Boundary Verdict

```text
boundary_held: yes
foreign claims remained candidate / partially_admitted at best
governance axes omitted
no authority grant
no doctrine mutation
```

## Notes

The run used a thin runtime admission wrapper rather than the full v0.3 extractor pipeline wired to foreign input.

The healthiest signal in this run is not promotion. It is containment: all 11 extracted principles remained at candidate, none reached fully_admitted, and the omitted governance axes stayed explicit rather than silently filled.

The main pressure surfaced by the run is typing pressure. Nine of the eleven principles are imperative or directive enough that the current DEF/NC/BL/OP/DEP surface does not type them cleanly.
