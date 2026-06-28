# Documentation Index

Start here if you are reading `BoundaryKit` as a public case study. All examples are illustrative
unless a page explicitly says it is a sanitized public evidence summary.

BoundaryKit Agent VM is a public security case study for governing untrusted AI-agent workloads with
explicit policy boundaries, rootless runtime isolation, managed provider-boundary controls, rollback
discipline, and evidence-backed validation.

The current public architecture centers this chain:

```text
public input / operator intent
  -> policy and promotion boundary
  -> OpenShell sandbox running Hermes Agent
  -> rootless Podman runtime posture + managed provider boundary
  -> NUC-class VM substrate
  -> evidence receipts and recovery discipline
```

Public diagrams are abstract reference models, not live deployment maps. They intentionally omit
hostnames, IP addresses, VM names, ports, routes, service names, key names, mount paths, incidents,
and recovery paths.

## Current Public Case Study

- [Overview](architecture/00-overview.md) - current public architecture, threat assumptions, and
  non-claims.
- [Verification model](verification.md) - vocabulary for static, reference-lab, boundary-measured,
  and production-ready claims.
- [Boundary receipt #1](evidence/boundary-receipt-01-inner-sandbox.md) - measured inner sandbox
  boundary.
- [Boundary receipt #2](evidence/boundary-receipt-02-inference-boundary.md) - managed inference
  credential boundary.
- [Governed workload case study](evidence/governed-agent-workload-case-study.md) - public walkthrough
  for treating an OpenShell/Hermes-style workload as untrusted.

## Architecture And Governance

- [Promotion control plane](architecture/02-promotion-control-plane.md) - dry-run-first promotion,
  rollback, and state-as-truth discipline at a public control-objective level.
- [Governance and claim discipline](architecture/04-production-governance.md) - risk tiers, tool allowlists,
  canaries, audit, rollback, and evidence requirements.
- [Gated preview access](architecture/05-secure-gated-agent-preview-access.md) - temporary, revocable
  preview exposure pattern.
- [Security methodology](security-methodology.md) - public-safe methodology and operating principles.
- [Threat model](threat-model.md) - assets, actors, trust boundaries, controls, limitations, and
  invariants.

## Reference Acceptance Suite

These pages are retained as generic, fictional lab fixtures. They are useful for understanding older
or portable acceptance checks, but they are not the current public runtime architecture for the
public case study.

- [Reference isolation substrate](architecture/01-isolation-substrate.md) - golden VM, signed-image,
  and microVM acceptance concepts.
- [Reference gateway runtime layout](architecture/03-gateway-runtime-layout.md) - legacy per-profile
  gateway fixture.
- [Reference acceptance receipt](evidence/substrate-validation-receipt.md) - sanitized receipt for the
  reference acceptance suite.

## Publication Boundary

- [Evidence model](evidence-model.md)
- [Public/private boundary](public-private-boundary.md)
- [Declassification checklist](declassification-checklist.md)

Nothing in these docs should be read as live deployment topology, a managed service claim, customer
evidence, or production-readiness proof.
