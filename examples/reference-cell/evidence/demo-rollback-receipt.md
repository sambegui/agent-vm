# Demo Rollback Receipt

Status: `example_only_pass`

This receipt is fake. It demonstrates the public evidence shape for rollback and does not describe a
real service, host, endpoint, client, runtime, or deployment.

## Example Rollback Target

| Field | Example value |
|---|---|
| Workload | `boundarykit-reference-orchestrator` |
| Previous artifact | `demo-registry.example/boundarykit-reference-orchestrator@sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa` |
| Candidate artifact | `demo-registry.example/boundarykit-reference-orchestrator@sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb` |
| Rollback command | `example_only rollback-reference-cell --target previous` |
| Elapsed time | `42s example_only` |
| Health after rollback | `healthy example_only` |
| Audit event | `rollback.executed example_only` |

## Example Observations

```text
example_only 00:00 rollback requested by demo-operator
example_only 00:10 previous digest selected
example_only 00:28 health check passed
example_only 00:42 rollback receipt closed
```

## Boundary

No live endpoint, service unit, client configuration, traffic shift, production incident, or private
runtime state is represented here.
