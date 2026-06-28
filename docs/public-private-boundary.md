# Public / Private Boundary

`BoundaryKit` is a public case study plus reference acceptance suite for governed, untrusted AI-agent
workloads. It is meant to show the control pattern: trust boundaries, explicit capability contracts,
promotion gates, rollback, auditability, and evidence-backed operations.

It is not a copy of any private operational deployment. Public material must be newly written,
illustrative, and safe to inspect without access to private infrastructure.

## Public Reference Material

Public material may include:

- current architecture docs for the OpenShell/Hermes case study;
- reference acceptance-suite docs for older or portable isolation and gateway fixtures;
- toy workloads that run with fake tools and local-only behavior;
- fake policies with placeholder tools, fake schema hashes, and example-only secret references;
- fake evidence receipts that show the shape of build/sign/verify, rollback, and audit records;
- sanitized public summaries of privately held evidence, when they are newly written from the
  generalizable lesson and contain no raw logs, private values, live topology, or operator details;
- scripts that scan public diffs for common leak classes;
- diagrams with placeholder hosts, clients, registries, and audit sinks.

Public examples should use obviously fictional values, such as:

- `demo-client`
- `demo-registry.example`
- `audit.demo.invalid`
- `secret://demo/...`
- all-zero or clearly fake `sha256:` digests
- synthetic commit ids such as `0000000`

## Private Operational Material

Private operational repos remain the place for:

- real source code for private services;
- real container images, SBOMs, signatures, logs, manifests, receipts, and task ledgers;
- real hostnames, IP addresses, registry paths, source paths, service names, client names, and
  topology;
- real runtime configuration, service units, tunnels, DNS details, and deploy state;
- real credentials, key paths, token ids, token hashes, signing details, and secret references tied
  to actual systems;
- raw transcripts, operator approvals, runtime truth, incident notes, and audit data.

Do not sanitize these artifacts in place and publish them. Recreate public examples and public
evidence summaries from scratch with fake values, scoped claims, and no raw transcripts or command
logs.

## Trust Boundaries

The public architecture treats every agent as an untrusted, tool-wielding workload. The host-side
operator and promotion control plane are higher-trust domains; agent runtimes are lower-trust domains;
high-risk work moves to stronger isolation.

The public examples should preserve that shape:

- operators approve mutations;
- control-plane scripts are dry-run by default;
- manifests pin immutable artifacts;
- tool access is an allowlist;
- denied tools are absent from discovery;
- egress defaults to deny;
- secrets are references, not values;
- audit records are evidence, not decoration;
- rollback is proven before promotion.

## Promotion Boundary

The public repo may document a promotion flow, but it must not imply that example files are production
evidence. A public example can show the receipt format; it cannot claim that a private deployment was
validated. A public sanitized summary can say that a named class of boundary was measured only when
the summary is regenerated from the lesson, strips private values, and clearly states what the
measurement does not prove.

Allowed public progression:

```text
example_only lab -> deploy-only example -> read-only canary example -> rollback example -> promotion decision example
```

Real deployment, registry publication, traffic movement, or production promotion belong outside this
public reference repo unless a separate public release gate explicitly approves them.

## Release Rule

Before publishing a branch, run the public safety scan and perform a human declassification review.
The scan catches common string and secret classes. Human review decides whether the concepts,
examples, and claims are safe.
