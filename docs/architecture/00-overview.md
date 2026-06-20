# 00 — Architecture overview

## Shifting from chatbot tabs to governed, persistent agent workloads

Most enterprise AI usage still happens through isolated browser tabs or ad hoc automation. That model
fragments context, hides execution state, and gives reviewers little evidence about what ran, what
authority was available, or how recovery would work.

`BoundaryKit` presents a governed runtime architecture for autonomous AI-agent workloads that are
treated as untrusted. Agents can process approved messages, attached documents, external links,
transcripts, API responses, and structured outputs, but the platform does not trust the agent or the
inputs it receives.

The VM is one implementation substrate. The deeper architecture is about trust boundaries: every
workload may be **compromised or misdirected at runtime**, so the platform limits what that costs
with promotion controls, isolation, fail-closed policy, audit evidence, and rollback.

Traditional services are mostly deterministic and operator-controlled. AI agents are not. They:

- execute **tool calls** (shell, files, network, API calls, content-processing tools) under model control,
- may act through **credentials or secret references** on behalf of an organization,
- ingest **untrusted input** (including external documents, links, and transcripts) — and that input can *redirect their behavior* (prompt injection, tool poisoning, cross-agent shadowing, excessive agency).

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
6. `../evidence/governed-agent-workload-case-study.md` — a concrete vendor-neutral scenario that shows
   how prompt injection, secret access, egress, audit, and rollback expectations map to evidence.

Then `../reference-workloads/` for the two archetypes and `../decisions/` for key choices.
