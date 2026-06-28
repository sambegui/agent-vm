# Security methodology

This document describes the public-safe methodology used to design and review the BoundaryKit Agent VM
case study. It applies to the public architecture, static site, sanitized receipts, and reference
acceptance fixtures.

## Guiding principles

1. **Agents as untrusted workloads** - The agent process, dependencies, tool descriptions, retrieved
   content, and model output can be subverted.
2. **Default-deny posture** - Network, filesystem, provider, capability, and tool policies start
   closed and require explicit allowance.
3. **Rootless runtime preference** - The public case study favors rootless Podman and avoids presenting
   a privileged Docker daemon as the runtime foundation.
4. **Secrets by reference** - Public examples use `secret://demo/...` references or placeholders, never
   raw values.
5. **Evidence over assertions** - Claims require receipts, negative tests, digest/version identifiers,
   audit events, or configuration state.
6. **Review before mutation** - Promotion and rollback are dry-run/review-first concepts; host-dependent
   lab commands are clearly separated from safe public docs review.
7. **Rollback as a first-class operation** - Recovery evidence is part of the definition of done.

## Current architecture layers

| Layer | What it protects | Representative controls |
|---|---|---|
| Policy and promotion boundary | Operator intent, approved mutation, rollback | dry-run plans, fail-closed policy, exact revision/artifact identifiers |
| OpenShell sandbox + Hermes Agent | Untrusted agent execution | tool/data gates, filesystem/network negative tests, non-root posture |
| Rootless Podman runtime | Host privilege boundary | no privileged Docker socket, capability drop, no-new-privileges posture |
| Managed provider boundary | Model/tool-provider credentials | placeholders in sandbox, outside-boundary credential resolution, fail-closed misroutes |
| NUC-class VM substrate | Backstop around sandbox runtime | public summaries only, no live topology |
| Evidence and recovery overlay | Claim discipline | sanitized receipts, non-claims, rollback expectations, manual declassification review |

## Reference acceptance suite

`platform/` retains older/generic lab fixtures for VM, image, reconcile/align, and microVM-style
acceptance checks. These are useful for testing portable design ideas, but they are not the primary
public architecture for the current Agent VM case study.

## STRIDE mapping

| STRIDE | Mitigations in this architecture |
|---|---|
| Spoofing | explicit source/artifact identifiers; provider boundary; auth-deny evidence for production claims |
| Tampering | immutable revisions, digest-pinned examples, state re-derivation, receipt review |
| Repudiation | public receipts, audit-event expectations, rollback records |
| Information disclosure | default-deny egress, secrets by reference, no raw values in public artifacts |
| Denial of service | timeout/recovery expectations, canary/SLO requirements before production claims |
| Elevation of privilege | rootless runtime posture, capability drop, no privileged Docker socket, sandbox boundary |

## PASTA alignment

This methodology aligns with **PASTA Stage 1** through **Stage 7**:

1. Define objectives: governed sandboxing for untrusted agent workloads.
2. Define technical scope: policy boundary, sandbox runtime, provider boundary, VM substrate, evidence.
3. Decompose application: public input, policy gate, sandbox, provider path, receipts.
4. Threat analysis: prompt injection, credential exposure, egress, lateral movement, runtime drift.
5. Vulnerability analysis: hardening baseline, supply chain, provider routing, public/private boundary.
6. Attack modeling: boundary negative tests and fail-closed provider behavior.
7. Risk mitigation: controls, receipts, rollback drills, and manual declassification review.

## Public review gates

Run these checks before publishing:

```bash
make ci
scripts/public-safety-scan
git diff --check
```

Then manually review for:

- real hostnames, IPs, VM names, service names, routes, ports, SSH aliases, and key names;
- NAS/mount paths, private repo paths, raw logs, transcripts, and incident details;
- token values, token ids, key material, provider credentials, and secret shapes;
- architecture drift that makes reference acceptance fixtures sound like the current live design.

Scanner success is necessary but not sufficient.
