# The Twelve-Factor App Snapshot

```text
source_label: twelve_factor_app
source_url: https://12factor.net/
scope: second foreign admission input / technical normative principles
instrument: v1_admission_wrapper
retrieval_note: canonical live source fetched locally for runtime recording
input_hash_sha256: 69230eae64071cc9ffcdfff6154c00dfb85c0c96d0710c63d189e20879a9dab9
```

## Introduction Slice

The Twelve-Factor App is a methodology for building software-as-a-service apps that use declarative formats, maintain a clean contract with the operating system, suit cloud deployment, minimize dev/prod divergence, and scale without major tooling or architecture change.

## The Twelve Factors

1. I. Codebase
   One codebase tracked in revision control, many deploys
2. II. Dependencies
   Explicitly declare and isolate dependencies
3. III. Config
   Store config in the environment
4. IV. Backing services
   Treat backing services as attached resources
5. V. Build, release, run
   Strictly separate build and run stages
6. VI. Processes
   Execute the app as one or more stateless processes
7. VII. Port binding
   Export services via port binding
8. VIII. Concurrency
   Scale out via the process model
9. IX. Disposability
   Maximize robustness with fast startup and graceful shutdown
10. X. Dev/prod parity
    Keep development, staging, and production as similar as possible
11. XI. Logs
    Treat logs as event streams
12. XII. Admin processes
    Run admin/management tasks as one-off processes
