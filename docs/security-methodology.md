# Security methodology

This document describes the security methodology used to design and review the reference architecture.
It applies to the walking-skeleton code in `platform/` and `control-plane/`.

## Guiding principles

1. **Agents as untrusted workloads** — Every AI agent runs as a sandboxed workload. The platform assumes
   the agent process, its dependencies, and its tool descriptions can be subverted.
2. **Default-deny at every layer** — Network, filesystem, capabilities, and tool policies all default to
   deny. Explicit allowlists with digest pinning are required for every capability.
3. **Evidence over assertions** — Security claims require receipts: command output, signatures, digests,
   audit events, or configuration state. This repository records evidence in `docs/evidence/`.
4. **Dry-run by default** — Mutating operations print a plan and require an explicit `--apply` flag.
5. **Rollback as a first-class operation** — Every promotion captures a rollback target and documents
   the rollback command.

## Architecture layers

| Layer | What it protects | Representative controls |
|---|---|---|
| Host control plane | Scripts, manifests, promotion logic, registry | ShellCheck, GitHub Actions, cosign, digest pinning |
| Golden VM / Tier-1 | Persistent agent runtime, control APIs | MicroVM (Firecracker/Kata), systemd, digest-pinned images, `align` verification |
| Tier-2 sandbox | Transient agent jobs, tool execution | Kata/containerd microVM, default-deny egress, seccomp, capability drop, timeout reap |
| Tool policy | Which tools an agent may invoke | Explicit allowlist, risk tiers, parameter schemas, human approval gate for sensitive writes |
| Audit sink | Auth, tool, egress, alignment, rollback events | Structured JSON lines, tamper-evident storage, retention policy |

## Hardening baseline

- Kernel: lockdown mode when available; module signing enforced.
- Init: minimal systemd unit set; no unnecessary services.
- Userspace: distroless or minimal container base images; static linking where practical.
- Runtime: seccomp default-deny; capability drop (CAP_DAC_OVERRIDE, CAP_SYS_ADMIN, etc.).
- Network: default-deny egress; explicit allowlists for registry, control plane, approved services.
- Storage: bounded mounts; no host filesystem exposure; digest verification on mount.
- Secrets: never in images, manifests, or logs; fetched at runtime from a secret store with audit.
- Supply chain: cosign signatures; SLSA provenance; SBOM generation; reproducible builds where practical.

## STRIDE mapping

| STRIDE | Mitigations in this architecture |
|---|---|
| Spoofing | SSH host keys; cosign image signatures; mTLS for control-plane APIs; digest pinning. |
| Tampering | Git-signed commits; digest-pinned images; immutable manifests; `align` verification. |
| Repudiation | Append-only audit sink; signed audit events; rollback drill records. |
| Information Disclosure | Default-deny egress; secret store with audit; no secrets in images/logs/manifests. |
| Denial of Service | Per-job resource quotas; timeout reap; microVM isolation; host control plane read-only CI. |
| Elevation of Privilege | Capability drop; seccomp; user namespaces; microVM boundary; no host docker socket. |

## PASTA alignment

This methodology aligns with **PASTA Stage 1 (Define Objectives)** through **Stage 7 (Risk Mitigation)**:
1. Define business/security objectives (sandboxed agent workloads).
2. Define technical scope (host control plane, golden VM, Tier-2 sandbox).
3. Application decomposition (layers above).
4. Threat analysis (STRIDE mapping above).
5. Vulnerability analysis (hardening baseline, supply chain).
6. Attack modeling (agent escape, tool misuse, promotion drift).
7. Risk mitigation (controls above, evidence requirements, rollback drills).

## Preflight and post-session gates

Operators should run these checks before and after a preview or canary session:

### Preflight
- `make ci` — static validation passes.
- `platform/validate/nested-smoke` — host can boot nested microVMs.
- `platform/validate/acceptance` — acceptance subset passes (PASS=6 FAIL=0).
- Digest alignment check — `~/platform/control/align` reports `ALIGNED`.
- Tool policy hash — recorded and match expected value.
- Secret scan — `gitleaks detect --no-git` and `trufflehog filesystem .` report no findings.

### Post-session
- Audit sink integrity — events appended, tamper-evident seal intact.
- Rollback drill — `control-plane/rollback-agent` completes within recovery target.
- Secret rescan — no new secrets introduced in receipts or logs.
- Digest alignment re-check — running image still matches manifest.