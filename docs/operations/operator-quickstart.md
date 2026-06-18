# Operator quickstart

This repository is a public **reference implementation + acceptance suite**. It is safe to inspect on
any machine. The full substrate runbook needs an isolated Linux lab host with nested virtualization,
hardware KVM exposed at `/dev/kvm`, libvirt/QEMU, Podman, containerd, Kata Containers, Firecracker,
cosign, a local registry, and a configured SSH alias for the illustrative VM.

The defaults create an illustrative `agent-platform` VM, but the host, IP, user, and image paths are
parameterized. Override them with `AGENT_VM_*` variables instead of editing scripts.

**Prerequisite:** an SSH public key must exist before running the provisioning script. By default the
key is `~/.ssh/agent-platform.pub`; override it with `AGENT_VM_PUBKEY`. Generate a default key if
needed:

```bash
ssh-keygen -t ed25519 -f ~/.ssh/agent-platform -C "agent-platform-lab"
```

**SSH host configuration:** add the following to `~/.ssh/config` so `AGENT_VM_SSH=agent-platform`
resolves to the lab VM:

```ssh-config
Host agent-platform agent-runtime
  HostName 10.0.0.60
  User admin
  IdentityFile ~/.ssh/agent-platform
  StrictHostKeyChecking accept-new
```

The default posture is **review first, mutate only with explicit apply flags**.

Common provisioning overrides:

```bash
AGENT_VM_NAME=agent-platform
AGENT_VM_SSH=agent-platform
AGENT_VM_IP=10.0.0.60
AGENT_VM_USER=agent
AGENT_VM_PUBKEY="$HOME/.ssh/agent-platform.pub"
AGENT_VM_IMGDIR=/var/lib/libvirt/images/agent-platform
```

## 1. Static checks anyone can run

```bash
git status --short --branch
make ci
git diff --check
```

`make ci` performs:

- Bash syntax checks for repo-owned shell scripts.
- ShellCheck lint when `shellcheck` is installed.
- YAML parsing when Ruby/Psych is available.

The check is intentionally host-light. It does not create VMs, push images, call cloud APIs, or mutate
services.

## 2. Read the architecture in order

1. [`README.md`](../../README.md) — public summary and 90-second tour.
2. [`docs/architecture/00-overview.md`](../architecture/00-overview.md) — threat model and layers.
3. [`docs/architecture/01-isolation-substrate.md`](../architecture/01-isolation-substrate.md) — Tier-1/Tier-2 runtime boundary.
4. [`docs/architecture/02-promotion-control-plane.md`](../architecture/02-promotion-control-plane.md) — dry-run promotion and rollback.
5. [`docs/architecture/04-production-governance.md`](../architecture/04-production-governance.md) — governance gates and evidence requirements.

## 3. Host-dependent substrate checks

These commands are for an isolated lab host. They are expected to fail on a normal laptop or CI runner
without nested KVM and the illustrative SSH aliases.

```bash
# Host side: create or reconcile the illustrative golden VM and bootstrap the acceptance runtime.
make provision

# Host side: prove nested hardware-backed microVM boot.
platform/validate/nested-smoke

# Host side: run the walking-skeleton acceptance subset.
platform/validate/acceptance
```

Expected acceptance footer after a fully configured substrate run:

```text
PASS=6 FAIL=0
```

For a non-default lab VM, pass the same overrides to the acceptance runner:

```bash
AGENT_VM_SSH=agent-platform platform/validate/acceptance
```

## 4. In-VM Tier-1 flow

Inside the illustrative VM:

```bash
~/platform/images/build-sign-push <version>
# Copy the printed digest into platform/manifests/hello.service.yaml.
~/platform/control/reconcile ~/platform/manifests/hello.service.yaml
~/platform/control/align ~/platform/manifests/hello.service.yaml
```

The reconciler refuses non-digest-pinned images. `align` prints `ALIGNED` only when the running image
digest matches the manifest.

## 5. In-VM Tier-2 flow

```bash
~/platform/sandbox/sandbox-runner ~/platform/sandbox/jobspec.example.json
```

The important evidence is:

- the job boots in a Kata/containerd microVM;
- default-deny egress blocks an external network attempt;
- timeout handling tears the job down;
- residual containers/tasks are zero after teardown.

## 6. Promotion-control-plane safety

Promotion scripts are dry-run unless `--apply` is provided:

```bash
control-plane/promote-agent --sha <commit> --label <label> --worktree <path>
control-plane/rollback-agent --to <release-dirname-or-path>
```

Only after reviewing the printed plan should an operator add `--apply`.

```bash
control-plane/promote-agent --sha <commit> --label <label> --worktree <path> --apply
control-plane/smoke-agent
control-plane/status-agent
```

## 7. Evidence to capture before claiming success

Use [`docs/verification.md`](../verification.md) as the checklist and store the result in an evidence
receipt like [`docs/evidence/substrate-validation-receipt.md`](../evidence/substrate-validation-receipt.md).
A production claim requires live evidence; a design claim only requires docs and static checks.

## 8. Teardown

Use the same `AGENT_VM_*` identity and image-path overrides used for provisioning. Review the values
first, then destroy the illustrative lab VM and its generated disk/seed image:

```bash
platform/vm/destroy-vm --print-config
platform/vm/destroy-vm
```

This teardown is intentionally limited to the configured lab VM artifacts. It does not remove the base
cloud image, local registry contents, signing keys, or unrelated libvirt resources.
