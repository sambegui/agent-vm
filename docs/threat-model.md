# Threat model

`agent-vm` treats AI agents as untrusted, tool-wielding workloads. The platform assumes an agent can be
misdirected by untrusted input or compromised through its tools, dependencies, runtime, or operator
workflow.

## Assets

| Asset | Why it matters |
|---|---|
| Credentials and secret references | Agents often act through API tokens, SSH keys, model keys, messaging tokens, or service accounts. |
| Workload state | Files, queues, transcripts, task state, and local caches may contain sensitive or integrity-critical data. |
| Host and runtime boundary | A compromised agent should not become a compromised host or another compromised agent. |
| Tool surface | Shell, file, browser, network, payment, messaging, and orchestration tools can create real-world effects. |
| Promotion state | The platform must know exactly what code/artifact is running and how to roll it back. |
| Audit evidence | Operators need reliable evidence for auth, tools, egress, deployment, rollback, and incidents. |

## Actors

| Actor | Capability |
|---|---|
| Prompt-injection attacker | Supplies content that tries to steer the agent into unsafe tool use or data exfiltration. |
| Compromised agent workload | Executes unexpected tool calls or attempts lateral movement. |
| Malicious dependency or artifact | Enters through package install, image build, or copied runtime assets. |
| Mistaken operator | Runs the wrong command, deploys the wrong revision, or skips rollback proof. |
| Network attacker | Attempts unauthorized access to exposed endpoints or relies on unexpected outbound reachability. |
| CI / repository attacker | Attempts to alter workflows, scripts, manifests, or docs to weaken validation. |

## Trust boundaries

```text
operator laptop / CI
        |
        v
host-side control plane  --ssh-->  golden VM / Tier-1 service
        |                              |
        |                              v
        |                        Tier-2 ephemeral microVM jobs
        |
        v
repository state, manifests, receipts, and audit evidence
```

Boundary rules:

- The repository contains examples, manifests, and scripts — not live secrets.
- Host-side promotion scripts are dry-run unless `--apply` is provided.
- Tier-1 services run from signed, digest-pinned artifacts reconciled to a manifest.
- Tier-2 higher-risk jobs run in ephemeral microVM sandboxes with timeout, teardown, and default-deny egress.
- Tool allowlists fail closed; denied tools should be absent from discovery, not merely rejected at call time.

## Primary threats and controls

| Threat | Control |
|---|---|
| Prompt injection triggers unsafe tools | Explicit tool allowlists, risk tiers, human approval for sensitive writes, audit events. |
| Agent escapes into host or sibling workload | VM boundary, per-profile runtime layout, Tier-2 microVM sandbox, bounded mounts. |
| Drift between recorded and live runtime | Status scripts re-derive live symlink/source SHA and flag drift. |
| Mutable or unsigned deployment | Exact source commit, digest-pinned image, cosign signature, provenance/SBOM references. |
| Operator accidentally mutates live state | Dry-run default, printed plan, `--apply` gate, rollback target capture. |
| Outbound data exfiltration | Default-deny egress and negative egress tests. |
| Secret exposure in git/logs/images | Secret references only; no raw values in manifests, images, receipts, or audit logs. |
| Broken rollback | Rollback command and receipt required before production promotion. |
| CI workflow abuse | Read-only workflow permissions and no untrusted event data interpolated into shell commands. |

## Current limitations

- Package-install archetype automation is intentionally capture-first until package distribution and rollback mechanics are fully implemented.
- The repository demonstrates a lab-host substrate skeleton; production readiness requires a separate canary evidence packet.
- Example host names, addresses, and paths are illustrative and must be replaced for a real deployment.
- This repository does not include a real secret manager, audit backend, or external monitoring stack.

## Security invariants

These requirements should not be waived for production use:

- missing or invalid auth is denied;
- denied tools are absent from tool discovery;
- unknown tools fail closed;
- raw secrets never appear in git, logs, manifests, images, or receipts;
- egress is denied by default and has a negative test;
- rollback is tested and timed;
- live runtime identity is proven before smoke-test claims;
- production promotion is based on evidence, not on unit creation alone.
