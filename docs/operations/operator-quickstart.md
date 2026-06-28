# Operator quickstart

This repository is a public case study plus reference acceptance suite. It is safe to inspect on any
machine. The default public workflow is documentation review, static checks, safety scanning, and
manual declassification review.

Host-dependent reference-lab commands are optional, illustrative, and expected to fail on ordinary
laptops or CI runners without a configured virtualization lab. They are not required to preview the
static site.

## 1. Safe public checks

Run from the repository root:

```bash
git status --short --branch
make ci
scripts/public-safety-scan
git diff --check
```

`make ci` performs shell syntax checks, optional ShellCheck lint, optional YAML parsing, and repository
tests. It does not create VMs, push images, call cloud APIs, or mutate services.

## 2. Read the current public architecture

1. [`README.md`](../../README.md) - public summary and repository map.
2. [`docs/index.md`](../index.md) - reading order.
3. [`docs/architecture/00-overview.md`](../architecture/00-overview.md) - current public case-study
   architecture.
4. [`docs/verification.md`](../verification.md) - claim vocabulary and verification levels.
5. [`docs/evidence/boundary-receipt-01-inner-sandbox.md`](../evidence/boundary-receipt-01-inner-sandbox.md)
   - inner sandbox boundary.
6. [`docs/evidence/boundary-receipt-02-inference-boundary.md`](../evidence/boundary-receipt-02-inference-boundary.md)
   - managed inference boundary.

## 3. Preview the static site locally

The public site is static. If a local server is already running from `site/`, use it. Otherwise:

```bash
cd site
python3 -m http.server 3000 --bind 127.0.0.1
```

Then open:

```text
http://127.0.0.1:3000/
```

## 4. Public/private blind-spot review

Before publishing, manually scan the public diff for:

- raw IPs outside documented placeholders;
- host aliases, VM names, service names, routes, ports, and recovery paths;
- SSH key names and key paths;
- NAS or mount paths;
- Telegram/user IDs/handles/tokens or messaging identifiers;
- provider keys, token shapes, `.env` contents, and secret values;
- private repo paths;
- raw transcripts, logs, screenshots, operator approvals, or incident details.

The public safety scanner is necessary but not sufficient.

## 5. Reference acceptance-suite lab commands

The `platform/` directory keeps a generic reference acceptance suite. These commands are illustrative
lab fixtures, not the current public Agent VM runtime story.

They require an isolated Linux lab host with virtualization support and locally installed tooling. Use
the example defaults only as placeholders; replace them for your own lab.

Depending on the reference fixture under test, the lab may require nested virtualization, `/dev/kvm`,
Kata/containerd or Firecracker-style microVM support, a local registry, and cosign-style artifact
signing. These are reference-lab requirements, not requirements for previewing the static site.

```bash
AGENT_VM_NAME=agent-platform
AGENT_VM_IP=10.0.0.60
AGENT_VM_USER=agent
AGENT_VM_SSH=agent-platform
AGENT_VM_PUBKEY="$HOME/.ssh/agent-platform.pub"
```

Reference-lab commands:

```bash
make provision
platform/validate/nested-smoke
platform/validate/acceptance
```

Inside the fictional lab VM, the reference suite may exercise:

```bash
platform/images/build-sign-push <version>
platform/control/reconcile platform/manifests/hello.service.yaml
platform/control/align platform/manifests/hello.service.yaml
platform/sandbox/sandbox-runner platform/sandbox/jobspec.example.json
```

Treat any result as reference-lab validation only. Production-ready language requires a separate
workload-specific evidence packet with auth, egress, audit, rollback, and SLO evidence.

## 6. Teardown for the reference lab

Use the same `AGENT_VM_*` identity and image-path overrides used for provisioning. Review the values
first, then destroy only the illustrative lab VM artifacts:

```bash
platform/vm/destroy-vm --print-config
platform/vm/destroy-vm
```

This teardown is intentionally limited to the configured lab VM artifacts. It does not remove unrelated
libvirt resources, private infrastructure, or local secrets.
