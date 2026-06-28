# Threat model

This public case study treats AI agents as untrusted, tool-wielding workloads. The platform assumes an
agent can be misdirected by untrusted input or compromised through its tools, dependencies, runtime, or
operator workflow.

## Assets

| Asset | Why it matters |
|---|---|
| Operator intent and policy | The system must distinguish approved authority from prompt-driven behavior. |
| Sandbox state | Files, sessions, task state, and local caches may contain sensitive or integrity-critical data. |
| Provider credentials | Model/tool-provider credentials must not be copied into the sandbox or public receipts. |
| Runtime boundary | A compromised agent should not become a compromised host or sibling workload. |
| Tool surface | Shell, file, browser, network, messaging, and orchestration tools can create real-world effects. |
| Evidence receipts | Operators need reliable proof for denied crossings, provider routing, rollback, and non-claims. |

## Actors

| Actor | Capability |
|---|---|
| Prompt-injection attacker | Supplies content that tries to steer the agent into unsafe tool use or data exfiltration. |
| Compromised agent workload | Executes unexpected tool calls or attempts lateral movement. |
| Malicious dependency or artifact | Enters through package install, image build, or copied runtime assets. |
| Mistaken operator | Runs the wrong command, deploys the wrong revision, or skips rollback proof. |
| Network attacker | Attempts unauthorized access to exposed endpoints or relies on unexpected outbound reachability. |
| Repository attacker | Attempts to alter workflows, scripts, manifests, or docs to weaken validation. |

## Trust boundaries

```text
public input / operator intent
        |
        v
policy and promotion boundary
        |
        v
OpenShell sandbox running Hermes Agent
        |                         |
        v                         v
rootless Podman runtime      managed provider boundary
        \                         /
         v                       v
       NUC-class VM substrate and evidence receipts
```

Boundary rules:

- The repository contains examples, manifests, docs, and scripts, not live secrets.
- Public diagrams are reference models, not live deployment maps.
- The sandbox is treated as a lower-trust execution boundary.
- Provider credentials are represented by references or placeholders inside the sandbox.
- Rootless runtime posture is preferred over a privileged Docker daemon.
- Tool allowlists fail closed; denied or unknown tools should not silently become available.
- Public receipts state what was measured and what remains pending.

## Primary threats and controls

| Threat | Control |
|---|---|
| Prompt injection triggers unsafe tools | Explicit tool/data gates, risk tiers, human approval for sensitive writes, audit events. |
| Agent exfiltrates data over the network | Default-deny egress, SSRF/lateral/DNS negative tests, managed provider path. |
| Provider credential lands in sandbox | Secrets by reference, placeholder-in-sandbox configuration, host/provider-side resolution. |
| Agent escapes into host or sibling workload | OpenShell sandboxing, rootless Podman posture, NUC-class VM substrate, bounded mounts. |
| Runtime drift or stale claims | Status checks, exact revision/artifact identifiers, receipts, and non-claim sections. |
| Secret exposure in git/logs/images | `.gitignore`, public-safety scan, manual declassification review, no raw values in receipts. |
| Broken rollback | Rollback target and recovery evidence required before production-ready language. |
| CI or docs drift preserves stale architecture | Docs contract tests and architecture-language lint should enforce current public terminology. |

## Current limitations

- The public case study has measured specific inner sandbox and provider-boundary behavior, not every
  outer containment layer.
- The reference acceptance suite in `platform/` is generic lab material, not the current public runtime
  map.
- Example host names, addresses, paths, registries, and secret references are fictional.
- This repository does not include a real secret manager, audit backend, customer deployment, or
  external monitoring stack.

## Security invariants

These requirements should not be waived for production use:

- missing or invalid auth is denied;
- denied tools are absent or fail closed;
- unknown tools fail closed;
- raw secrets never appear in git, logs, manifests, images, or receipts;
- egress is denied by default and has a negative test;
- provider credentials stay outside the sandbox boundary;
- rollback is tested and timed;
- runtime identity is proven before smoke-test claims;
- production promotion is based on evidence, not on unit creation alone.
