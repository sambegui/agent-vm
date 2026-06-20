# Demo Build / Sign Receipt

Status: `example_only_pass`

This receipt is fake. It demonstrates the evidence shape for a public reference cell and does not
describe a real build, registry push, signature, SBOM, deployment, or private workload.

## Scope

Allowed in this example:

- local toy workload build;
- fake SBOM checksum;
- fake signature verification result;
- fake policy validation result.

Not authorized by this example:

- public registry push;
- demo image publication;
- production deploy;
- traffic shift;
- runtime mutation.

## Example Artifact

| Field | Example value |
|---|---|
| Workload | `boundarykit-reference-orchestrator` |
| Source revision | `0000000-example` |
| Image | `demo-registry.example/boundarykit-reference-orchestrator@sha256:0000000000000000000000000000000000000000000000000000000000000000` |
| SBOM | `examples/reference-cell/evidence/demo-sbom.spdx.json` |
| SBOM SHA256 | `0000000000000000000000000000000000000000000000000000000000000000` |
| Signature mode | `example-only local test key` |
| Verification result | `example_only: claims validated and signature verified` |

## Example Validation

```text
example_only$ validate-demo-tool-policy examples/reference-cell/policies/demo-tool-policy.yaml
PASS example_only: allowed=3 denied_absent=3 fail_closed=true

example_only$ validate-demo-egress examples/reference-cell/policies/demo-egress-policy.yaml
PASS example_only: default=deny audit_on_deny=true
```

## Boundary

No real registry, credential, signing key path, SBOM, log, service name, runtime path, deployment, or
operator approval is represented here.
