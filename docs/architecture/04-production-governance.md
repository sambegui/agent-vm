# 04 — Production governance

The substrate makes workloads *isolatable*; governance decides **what a given workload is allowed to
be**, and gates it from lab to production with controls proportional to its blast radius. The unit of
governance is a **production cell**: one workload, with a contract, a signed artifact, a manifest,
isolation, auth, observability, progressive delivery, and proven rollback.

## Risk tiers (controls scale with autonomy/blast radius)

| Tier | Example | Required controls |
|---|---|---|
| **L0** Lab | synthetic job | digest pinning, teardown, no secrets, local logs |
| **L1** Internal read-only | read-only awareness endpoint | auth, **tool allowlist**, isolated state, **default-deny egress**, audit |
| **L2** Internal limited action | approved read/send tools | human approval for writes, stronger audit, tested rollback, scoped tokens |
| **L3** Owner-facing prod | a primary service | high SLO, full incident loop, backup/restore, live runtime proof |
| **L4** Client-facing | external surface | tenant isolation, data policy, external-audit-ready evidence, stronger identity |
| **L5** Regulated | high-autonomy/sensitive | compliance review, strict retention, dedicated environment |

A workload may not deploy with controls below its tier; raising autonomy raises the bar.

## Tool-agency security (the AI-specific danger surface)

For agents that expose tools (e.g. via MCP), the tool surface *is* the attack surface:

- tools are an **explicit allowlist**, not "whatever is convenient";
- **denied tools are absent from `tools/list`**, not merely rejected on call;
- an **unknown allowed tool fails closed**; a tool **schema-hash drift blocks** the workload;
- policy that cannot be loaded → **refuse to serve** (never fall back to a permissive default);
- tool *descriptions/schemas* are treated as injection surfaces; sensitive actions require approval.

```
examples/manifests/tool-policy.example.yaml   # allowed/denied tools + schema hashes + fail-closed flags
```

## Secrets, egress, supply chain

- **Secrets by reference only** — manifests carry `secret://…` refs; never values. No secret in image
  layers, manifests, logs, SBOM, or git. Token *ids/hashes* may be recorded; values never.
- **Default-deny egress** — internet, arbitrary DNS, work-plane APIs, model/messaging APIs all denied
  unless explicitly allowed; a denied egress emits an audit event.
- **Signed supply chain** — exact source SHA → digest-pinned image → cosign signature → SBOM/provenance
  ref → **deploy-time** verification (see `01`).

## Progressive delivery (measured exposure, not blind cutover)

A workload is promoted through canary stages **beside** the existing one, never replacing it in one
motion:

```
Stage 0  deploy-only dry canary   — health, auth-deny, egress-deny, alignment, audit; no clients
Stage 1  read-only canary         — one trusted client, read calls only, observe
Stage 2  limited production canary — one/two clients, narrow approved actions, old service still live
Promotion decision                — only if SLO met, rollback proven, no tool/egress/secret surprises
```

SLO/error-budget thinking, synthetic probes with baseline/control comparison, and **rollback proven
before promotion** are required — and you do not claim stronger reliability than your probe volume
supports.

## Audit & rollback

Minimum audit events — `service.start/stop`, `auth.accepted/denied`, `tool.allowed/denied`,
`egress.denied`, `secret.loaded`, `alignment.checked`, `rollback.executed` — shipped **off-box**,
append-only, no secret values. **Rollback is a tested drill** (endpoint and manifest-digest), with a
recorded receipt, not an assumption.

This overlay is how a new agent crosses from "runs in the lab" to "trusted in production" without the
platform having to trust the agent.
