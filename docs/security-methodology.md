# Security methodology

`agent-vm` shifts AI agents from isolated chatbot tabs into governed, persistent **Agent Employees** that live in team workspaces (Slack, Discord, ClickUp) collaborating alongside human employees. While this cooperative model unlocks massive productivity gains and cost savings, it exposes the runtime to a variety of untrusted inputs (files, chat history, meeting transcripts). 

Therefore, the platform treats these persistent digital workers as untrusted, tool-wielding workloads. The security model is aligned with common practices used by mature infrastructure teams: layered controls, least privilege, explicit promotion, auditable operations, and rollback evidence. It is a public reference architecture, not a certification, vendor endorsement, or provider-approved deployment pattern.

This document intentionally avoids deployment-specific hostnames, addresses, identities, keys, firewall handles, private URLs, and operational paths. A real deployment should bind these principles to its own threat model, policies, and evidence trail.

## 1. Defense in depth

Guest workloads (agent employees) are not trusted because their behavior can be influenced by prompts, tools, dependencies, retrieved project files, Google Meet/Zoom transcripts, and operator mistakes. The platform therefore avoids relying on a single boundary.

Controls are layered across:

- **runtime boundaries** — separate workload runtime from the host control plane;
- **network boundaries** — deny by default, then allow only required paths;
- **release boundaries** — promote known commits or artifacts instead of editing live runtime state;
- **operational workflows** — dry-run first, record evidence, and require rollback paths for
  higher-risk changes.

A control is useful only if the next layer still limits blast radius when it fails.

## 2. Least privilege and fail-closed defaults

Agents should receive only the permissions, tools, files, and network paths needed for their role.
Access should be explicit, narrow, auditable, and revocable.

Preferred defaults:

- deny-by-default firewalling and explicit allowlists;
- tool discovery that exposes only approved tools;
- missing or invalid policy treated as a hard failure;
- short-lived or scoped credentials where possible;
- human approval gates for sensitive writes or irreversible actions.

A denied capability should be absent from the agent's available surface, not merely discouraged in
documentation.

## 3. Isolation substrate

Runtime environments should be separated from the host control plane. The control plane decides what
should run; isolated runtimes execute it with constrained authority.

Operating principles:

- long-running services run from immutable promoted releases, not writable development directories;
- release symlinks or equivalent promotion targets are deployment pointers, not edit locations;
- promoted artifacts are identified by commit, digest, or package version;
- higher-risk or short-lived jobs use stronger isolation and explicit teardown;
- live runtime identity is verified before making claims about what is running.

The goal is to make deployment state observable and reproducible instead of dependent on local shell
history.

## 4. Egress and exfiltration resistance

Agents can leak data through network calls, logs, browser pages, generated artifacts, and tool
outputs. External access should therefore be mediated through narrow policy gates.

Public-safe design principles:

- outbound network access is allowlisted or routed through a policy-aware proxy where practical;
- negative egress tests are part of validation, not an afterthought;
- sensitive data is passed by reference where possible, not copied into prompts, logs, pages, or
  generated artifacts;
- receipts and audit logs record decisions and identifiers without storing raw secrets;
- public preview flows expose only intended development ports and do not grant broad network
  reachability.

Secret-by-reference is a design constraint: the agent may be allowed to request a capability, but
the raw secret should not become normal prompt or artifact content.

## 5. Temporary access for previews

Preview and review access should be explicit, time-bounded, and easy to revoke. The safest preview
is the narrowest one that still lets a reviewer inspect the intended surface.

Preferred patterns:

- ephemeral or on-demand access for demos and review;
- explicit preview ports rather than broad network access;
- no subnet routing, exit nodes, broad SSH access, or persistent remote identities unless a specific
  review requires them;
- clear shutdown and revocation steps after the review window ends;
- no reuse of preview credentials as production credentials.

A preview path should not silently become a standing management path.

See [`docs/architecture/05-secure-gated-agent-preview-access.md`](architecture/05-secure-gated-agent-preview-access.md)
for a standards-oriented reference pattern and sanitized Tailscale implementation example.

## 6. Auditability and rollback

A platform should be able to prove what is running before claiming it is fixed, deployed, or
validated.

Before promotion claims, verify:

- runtime state and process command;
- promoted commit, digest, package version, or equivalent source identity;
- import path or runtime source path;
- active policy and tool allowlist;
- expected network posture;
- rollback target and rollback command path.

Operational changes should be reproducible, reviewable, and ideally represented as code. Promotions
should record the previous known-good target so rollback is a tested operation rather than a hope.

## 7. Governance overlay

Governance sits across all layers. It does not replace isolation; it decides which controls are
required for each blast radius.

Target operating principles:

- risk tiers for workloads and tool classes;
- SLO or canary checks before promotion;
- explicit tool allowlists with fail-closed loading;
- signed or digest-pinned supply chain artifacts where possible;
- audit trails for promotions, tool grants, policy decisions, and rollbacks;
- secret-by-reference practices for credentials and sensitive data;
- rollback proof for changes that can affect durable state.

The point is not to make agents appear safe by policy alone. The point is to make each step
observable, bounded, and reversible enough that failures can be contained.

## Non-goals

`agent-vm` is a reference architecture and validated skeleton. It does not claim to be a turnkey
production platform, a managed security product, or a deployment endorsed by any company. A
production adoption needs its own environment-specific threat model, control mapping, incident
process, monitoring, and evidence retention policy.
