# Evidence Model

`BoundaryKit` uses evidence to keep production claims honest. A workload is not ready because a file
exists or a command was intended to run; it is ready only when current evidence proves the gate.

This document describes the public case-study evidence model. Public evidence in this repository has
three allowed forms:

- **Example receipts** are fake and marked `example_only`.
- **Reference acceptance receipts** are sanitized summaries for generic lab fixtures and do not prove
  the current Agent VM runtime.
- **Sanitized public summaries** describe a boundary class or validation result that was measured
  elsewhere, but they are newly written, stripped of raw logs and private values, and scoped to what
  the public text can safely claim.

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

## Public Evidence In This Repo

Files under `examples/reference-cell/evidence/` demonstrate receipt shape only. They use fake
registries, fake digests, fake signatures, fake checksums, and synthetic command output.

Files under `docs/evidence/` may include sanitized public summaries. They are not raw evidence logs,
do not expose private topology, and do not authorize production-readiness claims.

Do not treat public example receipts or sanitized summaries as proof of any private deployment.
