# Evidence Model

`BoundaryKit` uses evidence to keep production claims honest. A workload is not ready because a file
exists or a command was intended to run; it is ready only when current evidence proves the gate.

This document describes the public reference model. Example receipts in this repo are fake and marked
`example_only`.

## Evidence Principles

- Evidence is observed, not invented.
- A receipt records exact inputs, commands, outputs, and stop conditions.
- Secret values are never evidence; only secret references or redacted identifiers may appear.
- A failing receipt is still useful if it preserves the exact failure.
- Promotion gates advance only after evidence proves the gate.
- Rollback evidence must be captured before relying on promotion.

## Common Receipt Fields

| Field | Purpose |
|---|---|
| `status` | gate state, such as `example_only_pass`, `blocked`, or `failed` |
| `scope` | what the receipt does and does not authorize |
| `artifact` | digest-pinned fake or real artifact reference, depending on repo context |
| `source` | source revision or synthetic example revision |
| `policy` | policy file and hash, if applicable |
| `sbom` | SBOM path and checksum, if generated |
| `signature` | signing and verification result |
| `validation` | commands run and observed result |
| `audit` | audit sink or local example log result |
| `rollback` | rollback target and drill evidence |
| `boundary` | actions not performed, such as no push, no deploy, or no traffic shift |
| `risks` | unresolved issues and review questions |

## Gate Evidence

| Gate | Evidence required |
|---|---|
| Build | artifact digest, source revision, build command, checksum or image id |
| SBOM | generated SBOM path and checksum |
| Signature | signature command result and verification result |
| Policy | tool allowlist, denied tools absent, schema hash behavior, fail-closed behavior |
| Egress | default deny proof and audit event |
| Deploy-only canary | health, readiness, running digest matches manifest |
| Read-only canary | expected read behavior, denied write/tool behavior, audit trail |
| Rollback | target, command, elapsed time, post-rollback health |
| Promotion | evidence packet review and explicit decision |

## Fake Evidence In This Repo

Files under `examples/reference-cell/evidence/` demonstrate receipt shape only. They use fake
registries, fake digests, fake signatures, fake checksums, and synthetic command output.

Do not treat public example receipts as proof of any private deployment.
