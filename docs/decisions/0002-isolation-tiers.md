# ADR 0002 — Workload tiers and risk tiers

## Status
Accepted for reference acceptance-suite vocabulary. The current public Agent VM case study uses
OpenShell/Hermes, rootless Podman, managed provider boundary, NUC-class substrate, and receipt language
as the primary public architecture.

## Context
Not every reference-lab workload needs the same controls. Over-controlling the lab wastes effort;
under-controlling a production, client-facing, or money-touching workload is dangerous.

## Decision
Separate **runtime tiers** (where a workload runs) from **risk tiers** (what controls it must carry):

- **Runtime:** Tier-0 lab (process), Tier-1 long-running service (signed, digest-pinned, reconciled),
  Tier-2 ephemeral job (microVM, default-deny egress, verified teardown).
- **Risk:** L0–L5, with controls escalating by autonomy / external access / data sensitivity / blast
  radius. A workload may not deploy with controls below its risk tier.

## Consequences
- Clear, auditable promotion gates from lab to production.
- New agents are *classified* into a tier, not special-cased.
- Governance scales with capability instead of being all-or-nothing.
