# platform - reference acceptance suite

`platform/` is a generic, fictional lab fixture retained for reference validation. It is **not** the
current public runtime architecture for `agent-vm.sabe.dev`.

The current public case study centers an OpenShell sandbox running Hermes Agent, rootless Podman
runtime posture, a managed provider boundary, a NUC-class VM substrate, and evidence receipts. This
directory preserves older portable acceptance ideas: VM provisioning, signed/digest-pinned artifacts,
reconcile/align checks, default-deny egress, and teardown.

## Layout

| Path | Purpose |
|---|---|
| `vm/provision-vm`, `vm/destroy-vm` | fictional lab VM lifecycle with placeholder values |
| `vm/agent-platform.domain.xml`, `vm/cloud-init/`, `vm/systemd/` | reference VM definition and NoCloud seed |
| `images/build-sign-push` | build, sign, and print a digest for a reference image |
| `images/hello-agent/` | minimal reference service with health/run endpoints |
| `manifests/hello.service.yaml` | digest-pinned reference manifest |
| `control/reconcile`, `control/align` | render/restart from a pinned digest and assert running state |
| `sandbox/sandbox-runner`, `sandbox/jobspec.example.json` | higher-risk sandbox fixture with default-deny egress and teardown |
| `validate/nested-smoke` | reference microVM-style boot check |
| `validate/acceptance` | end-to-end reference acceptance subset |
| `state/substrate-validation.md` | sanitized reference validation notes |

## Public meaning

A passing `platform/` run supports only this claim:

> the generic reference acceptance suite passed in a configured lab.

It does not prove current private deployment state, production readiness, or the complete outer
containment story for the Agent VM case study.

## Reference runbook

```bash
# on a configured isolated lab host
make provision
platform/validate/nested-smoke
platform/validate/acceptance

# inside the fictional lab VM
platform/images/build-sign-push <version>
platform/control/reconcile platform/manifests/hello.service.yaml
platform/control/align platform/manifests/hello.service.yaml
platform/sandbox/sandbox-runner platform/sandbox/jobspec.example.json
```

## Notes

- All addresses, hosts, users, registries, and paths are illustrative.
- Nothing here points at real infrastructure.
- Keep current public architecture claims in `docs/architecture/00-overview.md`.
- Keep current measured-boundary claims in `docs/evidence/boundary-receipt-*.md`.
