# 00 — Architecture overview

## Shifting from chatbot tabs to governed, persistent 'Agent Employees'

Most enterprise AI deployments suffer from isolated usage: employees run queries in individual, context-blind chatbot tabs. This setup has zero team visibility, fragmented context, and no secure path to access enterprise files. 

`agent-vm` introduces a governed, persistent **Agent Employee** substrate. Instead of solitary chatbot tabs, agents live directly inside group chats (Slack, Discord, ClickUp), collaborating alongside human employees. 

By executing repeatable workflows (or skills) securely on a dedicated, isolated VM with continuous access to on-disk project files, these digital workers deliver highly-polished assets (Excel models, PowerPoint presentations conforming to company templates) back to the team channel while driving extreme cost savings.

To achieve this securely, the platform treats every agent employee as a workload that may be **compromised or misdirected at runtime**, and limits what that costs. Defense is layered, and each layer assumes the one above it can fail.

Traditional services are mostly deterministic and operator-controlled. AI agents are not. They:

- execute **tool calls** (shell, files, network, Slack notifications, meeting integrations) under model control,
- hold **credentials** and act on behalf of the organization,
- ingest **untrusted input** (including external files, email, and meeting transcripts) — and that input can *redirect their behavior* (prompt injection, tool poisoning, cross-agent shadowing, excessive agency).

## Layered defense

| Layer | Assumes | Provides |
|---|---|---|
| **Substrate** (`01`) | an agent process can be exploited | VM boundary; Tier-2 jobs get an ephemeral microVM + default-deny egress + teardown; Tier-1 services run from signed, digest-pinned, reconciled images |
| **Control plane** (`02`) | live state drifts and operators fat-finger | immutable exact-commit releases; dry-run-by-default mutation; drift detection; recorded rollback target |
| **Gateway layout** (`03`) | many profiles share a runtime and get confused | one explicit service per profile; exactly one runtime source per profile; restart isolation |
| **Governance** (`04`) | capability grows over time | risk tiers gate controls; tool allowlists fail closed; secrets by reference; audit; tested rollback; canary before promotion |

## Agent-agnosticism, concretely

Nothing in the substrate, control plane, or governance names a specific agent framework. The two
reference archetypes exist only to prove generality across *opposite* deployment models:

- **Archetype A** — Python orchestrator, **immutable git-release** model (`control-plane/promote-agent`,
  `agent-gateway@core`).
- **Archetype B** — Node backend agent-pool, **versioned package-install** model
  (`control-plane/promote-pkg`, capture-first).

If a new agent arrives, it is classified into a **risk tier** and a **deployment archetype**, given a
**workload contract** and a **manifest**, and hosted — without changing the platform.

## How to read this directory

1. `01-isolation-substrate.md` — where workloads actually run, and the Tier-1/Tier-2 boundary.
2. `02-promotion-control-plane.md` — how code becomes a running release, safely and reversibly.
3. `03-gateway-runtime-layout.md` — how one runtime serves many profiles without ambiguity.
4. `04-production-governance.md` — the controls that gate a workload from lab to production.
5. `05-secure-gated-agent-preview-access.md` — how to expose agent/dev previews behind a temporary,
   revocable, auditable access gate without turning preview access into broad network access.

Then `../reference-workloads/` for the two archetypes and `../decisions/` for key choices.
