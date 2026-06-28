# ADR 0001 — Nested-virtualization substrate with microVM sandboxing

## Status
Accepted for the reference acceptance suite. Superseded as the current public Agent VM runtime story by
the OpenShell/Hermes, rootless Podman, managed-provider-boundary case study in
[`../architecture/00-overview.md`](../architecture/00-overview.md).

## Context
The reference acceptance suite hosts AI-agent fixtures that execute tool calls under model control and may be misdirected by
untrusted input. Shared-kernel containers alone are a weak boundary for an agent job that might be
compromised or coerced at runtime.

## Decision
For the reference fixture, run workloads inside a golden VM defined as code (KVM), and run higher-risk **Tier-2** jobs in
**Kata microVMs** (via containerd `io.containerd.kata.v2`) rather than plain containers — a real
kernel boundary per job — with default-deny egress, a hard timeout, and verified teardown. This
requires **nested virtualization**, validated by a boot smoke test before anything depends on it.

## Consequences
- Strong isolation for untrusted agent jobs: a compromised job is bounded by a microVM, not a shared
  kernel.
- Requires hardware virtualization (`vmx`/`svm`) exposed into the VM and `/dev/kvm` access.
- Heavier than containers, but bounded by tiering — only Tier-2 pays the microVM cost; Tier-1 stays on
  reconciled, signed containers.
