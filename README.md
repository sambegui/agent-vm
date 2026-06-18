# agent-vm

**A framework-agnostic sandbox skeleton for governed AI-agent workloads that are treated as untrusted.**

This public **reference implementation + acceptance suite** demonstrates how to host AI-agent workloads inside governed, persistent runtime layers without coupling the substrate to any single agent framework or collaboration product. It demonstrates reference patterns for strict runtime isolation and exact-commit promotion, with audit logging and default-deny egress treated as evidence-gated controls; the evidence is split between static checks, host-validated lab receipts, and workload-specific canary packets.

The architecture models an operator-controlled sandbox skeleton where approved queues, collaboration surfaces, transcripts, external files, API responses, and structured outputs are handled through auditable containment boundaries.

## What this demonstrates

This repository shows a platform/security architecture pattern: autonomous agents are treated as untrusted workloads, their authority is mediated by promotion controls and runtime boundaries, and claims are tied to validation evidence. The pattern maps to enterprise AI automation, workspace collaboration, platform engineering, and IT governance where agents process external files, approved transcripts, API responses, and structured outputs inside auditable containment boundaries.

## What this proves

- workload isolation for tool-using agents
- dry-run-first promotion and rollback workflows
- signed / digest-pinned deployment patterns
- runtime drift detection and state-as-truth checks
- tiered controls for higher-blast-radius execution
- human/operator governance around automation
- practical shell, Python, systemd, virtualization, and CI hygiene

## 90-second tour

1. Start with the architecture diagram below to see the control-plane/substrate boundary.
2. Read [`platform/state/substrate-validation.md`](platform/state/substrate-validation.md) for the
   run-backed substrate evidence.
3. Read the vendor-neutral
   [governed workload case study](docs/evidence/governed-agent-workload-case-study.md) for the
   threat model, control path, and claim boundaries in one concrete scenario.
4. Skim [`docs/operations/operator-quickstart.md`](docs/operations/operator-quickstart.md) for safe
   local checks versus host-dependent and mutating commands.
5. Review [`docs/verification.md`](docs/verification.md) and
   [`docs/evidence/substrate-validation-receipt.md`](docs/evidence/substrate-validation-receipt.md)
   for the evidence model.
6. Read [`docs/security-methodology.md`](docs/security-methodology.md), [`SECURITY.md`](SECURITY.md),
   and [`docs/threat-model.md`](docs/threat-model.md) for methodology, trust boundaries, current gaps,
   and non-goals.

## Implementation status

| Area | Status | Notes |
|---|---|---|
| **Archetype A — immutable release** | exercised | Python orchestrator-style agent promoted by exact commit with dry-run/apply and rollback flow. |
| **Archetype B — package install** | captured/design | Node package-install workflows are documented with explicit stubs until package distribution and rollback mechanics are implemented. |
| **Tier-1 signed service** | host-validated | Local registry, cosign signing, digest-pinned manifest, reconcile/align flow; deploy-time cosign verification remains a hardening item. |
| **Tier-2 microVM sandbox** | host-validated | Runner validates `egress.default=deny`; lab receipts show denied direct-IP/DNS probes, timeout, and teardown. |
| **Production platform** | not claimed | This is a reference architecture and validated skeleton, not a turnkey managed platform. |

> **Reference implementation + acceptance suite.** Every host, network, account, and identifier here
> is illustrative (`example-network`, `platform-host`, `agent-runtime`). Nothing points at real
> infrastructure, and no secrets are present — secret *references* only. The repository proves a
> reproducible lab skeleton and executable validation checks, not a hosted managed product.

## Architecture at a glance

```mermaid
flowchart TB
    classDef gov fill:#fde68a,stroke:#b45309,stroke-width:2px,color:#111827;
    classDef plane fill:#dbeafe,stroke:#1d4ed8,color:#0b1324;

    subgraph HOST["Host — operator trust domain"]
        direction TB
        OP["Operator<br/>dry-run by default"]
        A["Archetype A<br/>Python orchestrator<br/>immutable git-release"]
        B["Archetype B<br/>Node agent-pool<br/>versioned package"]
        CP["Promotion control plane<br/>exact-commit releases · drift detection · state-as-truth"]:::plane
        OP --> CP
        A --> CP
        B --> CP
    end

    GOV["Governance overlay<br/>risk&nbsp;tiers&nbsp;L0–L5&nbsp;·&nbsp;SLO/canary&nbsp;·&nbsp;fail-closed&nbsp;tool&nbsp;allowlist<br/>secret&nbsp;refs&nbsp;·&nbsp;signed&nbsp;supply&nbsp;chain&nbsp;·&nbsp;audit&nbsp;·&nbsp;rollback&nbsp;proof"]:::gov

    subgraph VM["Golden VM substrate"]
        direction TB
        subgraph T1["Tier-1 service"]
            T1S["cosign-signed · digest-pinned<br/>reconcile → align"]
        end
        subgraph T2["Tier-2 · ephemeral Kata microVM"]
            T2J["default-deny egress · hard timeout<br/>verified teardown"]
        end
        GW["agent-gateway@<profile><br/>one runtime source per profile · restart isolation"]
        T1S --> GW
        T1S -.->|"escalate higher-risk work"| T2J
    end

    CP -->|"promote exact commit (ssh, verified)"| T1S
    GOV -.->|gates| CP
    GOV -.->|gates| VM
```

*Vertical flow is the trust boundary (operator → control plane → substrate). **Solid** = verified promotion flow; **dotted** = governance/policy & risk escalation; the highlighted node is the cross-cutting governance overlay.*

## Why this matters

Most organizations use AI through isolated browser tabs or ad hoc automation. This model lacks team visibility, fragments context, and relies on manual copying and pasting. Moving agent workloads into persistent collaboration paths is more powerful, but it introduces execution, credential, and data-boundary risks.

AI agent workloads execute tool calls, touch external data, invoke APIs, and can be steered by untrusted input. This reference skeleton addresses those concerns by treating agent workloads as governed and untrusted:

1. **Persistent bounded context:** Agent workloads can process approved queues, transcripts, external files, API responses, and structured outputs inside the isolated substrate.
2. **Auditable containment boundaries:** File, network, credential, and tool access are routed through default-deny controls with explicit evidence for what ran.
3. **Repeatable workflow execution:** Operators can route durable workflows through the promotion control plane, isolation substrate, and governance overlay instead of relying on one-off local state.
4. **Predictable operating model:** Reproducible environments make agent automation easier to review, rerun, roll back, and verify without overclaiming turnkey production readiness.

Running several autonomous digital workers safely on shared infrastructure aligns with common security practices used by mature infrastructure teams: SLOs and canaries, explicit release promotion, supply-chain integrity, tool allowlists, egress controls, evidence-backed rollback, and governance proportional to blast radius.

## Security methodology

This reference architecture is not a company-endorsed deployment pattern or a vendor certification. It is a public,
vendor-neutral reference architecture for applying practical infrastructure security to AI-agent
workloads:

- **Defense in depth** — runtime, network, release, and operator-workflow controls reinforce each
  other instead of relying on prompts or one sandbox.
- **Least privilege, fail closed** — agents receive only the tools, permissions, files, and network
  paths needed for their role; missing policy denies access rather than falling back to broad defaults.
- **Isolated, immutable runtime state** — long-running services run from promoted releases; release
  symlinks or equivalent targets are deployment pointers, not edit locations.
- **Egress and exfiltration resistance** — outbound access is mediated through allowlists or narrow
  policy gates, and sensitive data is passed by reference instead of copied into prompts, logs, browser
  pages, or generated artifacts.
- **Temporary preview access** — demos and review paths should be explicit, time-bounded, narrow, and
  easy to revoke; broad routing or persistent remote identities are avoided unless specifically needed.
  See the [secure gated agent preview access](docs/architecture/05-secure-gated-agent-preview-access.md)
  reference pattern.
- **Auditability and rollback** — runtime state, process command, import/source path, promoted commit,
  and rollback target are verifiable before claiming what is running.
- **Governance overlay** — risk tiers, canary checks, tool allowlists, signed or digest-pinned supply
  chain artifacts, audit trails, rollback proof, and secret-by-reference practices sit across the
  architecture.

See [`docs/security-methodology.md`](docs/security-methodology.md) for the public-safe methodology.

## The three layers

```
   operator (host)        ┌────────────────────────────────────────────────┐
   dry-run by default ───►│  PROMOTION CONTROL PLANE                       │
                          │  immutable releases · drift detection ·        │
                          │  state-as-truth · 2 deployment models          │
                          └───────────────┬────────────────────────────────┘
                                          │ promote exact commit (ssh, verified)
                          ┌───────────────▼────────────────────────────────┐
                          │  ISOLATION SUBSTRATE  (golden VM, as code)     │
                          │  Tier-1 long-running service                   │
                          │    cosign-signed · digest-pinned · reconciled  │
                          │  Tier-2 ephemeral microVM sandbox (Kata)       │
                          │    default-deny egress · timeout · teardown    │
                          └───────────────┬────────────────────────────────┘
                                          │ per-profile, isolated
                          ┌───────────────▼────────────────────────────────┐
                          │  GATEWAY RUNTIME LAYOUT                        │
                          │  agent-gateway@<profile> · one runtime source  │
                          │  per profile · restart isolation               │
                          └────────────────────────────────────────────────┘
   governance overlay:  risk tiers L0–L5 · SLO/canary · MCP tool allowlist (fail-closed)
                        · secrets-by-reference · signed supply chain · audit · rollback proof
```

1. **Isolation substrate** — a nested-virt golden VM defined as code, hosting tiered workloads:
   **Tier-1** long-running services (cosign-**signed**, **digest-pinned**, reconciled to a manifest)
   and **Tier-2** ephemeral **microVM sandboxes** (Kata + containerd, **default-deny egress**, hard
   timeout, verified teardown). → [`docs/architecture/01-isolation-substrate.md`](docs/architecture/01-isolation-substrate.md), [`platform/`](platform/)
2. **Promotion control plane** — immutable, exact-commit releases shipped with provenance; mutations
   are **dry-run by default**; status tools **re-derive live truth and flag drift**. Exercised for
   the immutable-release archetype and captured for the package-install archetype. → [`docs/architecture/02-promotion-control-plane.md`](docs/architecture/02-promotion-control-plane.md), [`control-plane/`](control-plane/)
3. **Gateway runtime layout** — one systemd **template** per agent runtime; each profile is an
   explicit, independently-restartable service with **exactly one** declared runtime source. →
   [`docs/architecture/03-gateway-runtime-layout.md`](docs/architecture/03-gateway-runtime-layout.md), [`deploy/agent-gateway/`](deploy/agent-gateway/)

A **production-governance** overlay sits across all three: workload risk tiers, SLO/canary delivery,
MCP tool-agency security, secrets-by-reference, signed artifacts, audit, and tested rollback. →
[`docs/architecture/04-production-governance.md`](docs/architecture/04-production-governance.md)

The same governance posture applies to previews: agent/dev preview services should sit behind a
temporary, revocable, least-privilege, auditable access gate rather than a public or standing tunnel.
→ [`docs/architecture/05-secure-gated-agent-preview-access.md`](docs/architecture/05-secure-gated-agent-preview-access.md)

## What's been validated

A working "walking skeleton" exercises the substrate end-to-end: nested-KVM golden VM provisioned as
code; a Tier-1 signed, digest-pinned service with reconcile/align and proven promote+rollback; a
Tier-2 Kata microVM that boots, is denied egress by default, honors a hard timeout, and tears down;
acceptance suite green. See [`platform/`](platform/), [`docs/verification.md`](docs/verification.md),
and [`docs/evidence/substrate-validation-receipt.md`](docs/evidence/substrate-validation-receipt.md).

## Repository map

| Path | What it is |
|---|---|
| `docs/architecture/` | The design, layer by layer (agnostic). Start at `00-overview.md`. |
| `docs/reference-workloads/` | The two abstract agent archetypes (A immutable-release, B package-install). |
| `docs/decisions/` | Architecture decision records. |
| `docs/operations/` | Operator quickstart and safe runbook entry points. |
| `docs/evidence/` | Sanitized validation receipts, evidence packets, and the governed workload case study. |
| `docs/security-methodology.md` | Public-safe security methodology and operating principles. |
| `docs/architecture/05-secure-gated-agent-preview-access.md` | Reference pattern for temporary, revocable, least-privilege preview access. |
| `docs/verification.md` | Claim discipline and verification gates. |
| `docs/threat-model.md` | Threat model, trust boundaries, and current limitations. |
| `SECURITY.md` | Public security policy and reporting guidance. |
| `platform/` | The substrate as code: VM provisioning, signed image pipeline, reconcile/align, sandbox runner, acceptance. |
| `control-plane/` | Promotion / status / rollback scripts — **dry-run by default**, `--apply` to act. |
| `deploy/agent-gateway/` | The templated multi-profile gateway (unit + launcher + example envs). |
| `examples/` | Illustrative manifests and state-as-truth files (not live). |

## Design principles

- **Agent-agnostic** — agents are workloads, not the architecture.
- **Immutable & verifiable** — exact commits, signed digests, explicit verification gates, no editing live; deploy-time cosign verification remains a hardening item.
- **Dry-run by default** — every mutation previews before it acts; `--apply` is explicit.
- **Least authority, fail-closed** — default-deny egress, explicit tool allowlists, refuse to serve on policy-load failure.
- **Evidence over assertion** — status re-derives ground truth; deploys carry provenance; rollback is proven, not assumed.

## Status & license

Reference architecture plus a validated substrate skeleton — a demonstration of secure multi-agent
platform design, not a turnkey product. Licensed under **MIT** (see `LICENSE`).
