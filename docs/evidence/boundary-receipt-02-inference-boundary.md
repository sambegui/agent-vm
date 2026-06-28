# Boundary receipt #2 — inference boundary, measured

This is a sanitized public summary of a privately held boundary receipt. It records the second
**adversarially relevant** boundary in the `BoundaryKit` reference architecture: the **inference
boundary**, the governed path an agent runtime uses to reach a model provider. As with the first
receipt, no private hosts, addresses, image digests, credentials, or command transcripts appear here.

Receipt #1 measured the inner sandbox and was deliberately honest about one gap: its
credential-non-leakage check ran *without* a real provider credential attached, so the meaningful
claim — "a real credential resolves only at the boundary and never lands inside the sandbox" — was
named as a follow-on. **This receipt is that follow-on.** It is partial and narrowly scoped, and it
upgrades exactly one previously-weak claim by one notch: from *designed* to *measured*.

## Scope

| Item | Value |
|---|---|
| Boundary measured | The inference path: an agent runtime's access to a model provider |
| Mediation | Model calls traverse a managed inference boundary; the sandbox has no direct upstream route |
| Credential handling | The provider credential inside the sandbox is a non-functional **placeholder**; the real credential is resolved only at the boundary, at request time |
| Method | Configuration inspection inside the sandbox + a negative behavior test (deliberately misroute the inference API mode and observe the failure shape) |
| Mutating production systems | None |
| Secrets included | None |
| Claim supported | Inside the sandbox the agent holds no working provider credential and has no ungoverned path to the model — **not** that the mediating proxy is itself unbreakable |

## What was measured

Two properties, both observed directly rather than assumed from design.

1. **Credential placeholder, resolved at the boundary.** The agent's model configuration *inside* the
   sandbox carries a non-functional placeholder and points at the governed inference route, not the
   upstream provider directly. The real credential is resolved at the boundary at request time; it is
   absent from the sandbox's configuration file and from the agent process environment. This is the
   credential-placement test Receipt #1 could not make by itself.

2. **Fail-closed on misroute.** When the governed route is deliberately misconfigured — the inference
   API mode set to a value the upstream path cannot satisfy — the agent does **not** silently fall back
   to an ungoverned connection, and does **not** proceed on a partial result. It fails closed: the run
   stops rather than emitting an unverified success. The security-relevant reading is that a *broken*
   governed path produces a *stopped* agent,
   not one that quietly finds another way out.

**Headline:** the model credential the agent depends on is not present in the agent's own trust zone.
The agent reaches the model only by traversing a boundary that holds the credential and applies policy,
and when that boundary is disrupted the agent stops instead of degrading to an ungoverned path.

## What this receipt does NOT claim

This remains the most important section, and the discipline is unchanged from Receipt #1: unproven
boundaries are named, not implied.

- **It does not prove the mediating proxy is unbreakable.** The pattern *moves* trust from "every
  sandbox" to "one audited boundary component" — a real and useful reduction in attack surface — but it
  does not prove that component is non-bypassable against a determined in-sandbox attacker who can
  reach it. That is a separate, harder receipt.
- **It does not prove the upstream credential is unrecoverable.** The credential is shown absent from
  the sandbox config and environment; a stronger test would attempt *active* extraction at the boundary
  under load, not merely confirm static absence.
- **This is configuration + behavior evidence, not a formal proof.** The fail-closed behavior was
  observed for one class of misroute; it is a strong signal, not an exhaustive guarantee that no
  misconfiguration can ever yield an ungoverned success.
- **This is the inference boundary, not an outer containment boundary.** A VM, hypervisor, or
  host-management-plane boundary needs its own public summary before it is described as measured here.

## Why this matters — the design choice it records

The generalizable lesson, stated so others can adopt it without any of our coordinates:

> **Secrets live outside the sandbox, not inside it.** An agent should hold a placeholder, not a key.
> Put the real credential behind a single mediating boundary that injects it at egress, pair it with
> deny-by-default egress, and prefer designs where disrupting the governed path *stops* the agent
> rather than letting it find an ungoverned one.

This is the property a multi-profile agent substrate wants: workloads traverse a mediating boundary
instead of holding each other's credentials, and a compromised agent cannot simply read a working key
from its own sandbox because it never held one.

## Evidence level

Read this against the [verification model](../verification.md). This receipt is a **boundary
measurement**: stronger than a design assertion because both properties were observed inside a running
sandbox, weaker than a production canary because no real workload, SLO, or active-extraction adversary
is in scope. It sits alongside Receipt #1 and covers exactly one additional boundary — the credential
and inference path — and it explicitly retires one of Receipt #1's named gaps to *measured*.

Read alongside [boundary receipt #1 — inner sandbox](boundary-receipt-01-inner-sandbox.md), the
[governed-agent-workload case study](governed-agent-workload-case-study.md), and the
[substrate validation receipt](substrate-validation-receipt.md).
