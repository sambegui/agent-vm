# platform — the isolation substrate (as code)

A defined-as-code golden VM (`agent-platform`) on a nested-virtualization host, hosting Tier-1
long-running agent services and a Tier-2 microVM sandbox runner. Design:
[`../docs/architecture/01-isolation-substrate.md`](../docs/architecture/01-isolation-substrate.md).

## Layout

| Path | Purpose |
|---|---|
| `vm/provision-vm`, `vm/destroy-vm` | idempotent golden-VM lifecycle (libvirt + cloud-init) |
| `vm/agent-platform.domain.xml`, `vm/cloud-init/`, `vm/systemd/` | VM definition, NoCloud seed, static networking |
| `images/build-sign-push` | build → cosign sign → push → print digest |
| `images/hello-agent/` | a minimal Tier-1 demo agent (health + run endpoints) |
| `manifests/hello.service.yaml` | digest-pinned Tier-1 manifest |
| `control/reconcile`, `control/align` | render+restart from a pinned digest; assert running == manifest digest |
| `sandbox/sandbox-runner`, `sandbox/jobspec.example.json` | Tier-2 Kata microVM job: default-deny egress, timeout, teardown |
| `validate/nested-smoke` | prove a HW-backed microVM boots (nested-virt gate) |
| `validate/acceptance` | end-to-end acceptance subset |
| `state/substrate-validation.md` | validation evidence |

## Runbook

```bash
# on the host
platform/vm/provision-vm            # create the golden VM (idempotent); then: ssh agent-platform
platform/validate/nested-smoke      # nested HW-backed microVM boot check
platform/validate/acceptance        # expected final line: PASS=5 FAIL=0

# inside the VM
~/platform/images/build-sign-push <ver>           # -> DIGEST=<registry>/hello-agent@sha256:...
# pin that digest into platform/manifests/hello.service.yaml, then:
~/platform/control/reconcile <manifest>           # deploy from the pinned digest
~/platform/control/align <manifest>               # -> ALIGNED
~/platform/sandbox/sandbox-runner <jobspec.json>  # Tier-2 microVM job (default-deny, timeout, teardown)
```

## Notes

- Tier-2 uses Kata (containerd `io.containerd.kata.v2`) for a per-job kernel boundary.
- The reconciler renders a Quadlet `.container` unit, with an equivalent systemd user-service fallback
  where the Quadlet generator is unavailable.
- All addresses, hosts, and registries are illustrative; nothing here points at real infrastructure.
