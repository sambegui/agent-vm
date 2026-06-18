# Verification model

This repository separates **static validation**, **host-dependent substrate validation**, and
**production-readiness evidence**. Do not collapse those into one claim.

For a concrete, vendor-neutral scenario that keeps those boundaries separate, read
[`docs/evidence/governed-agent-workload-case-study.md`](evidence/governed-agent-workload-case-study.md).

## Verification levels

| Level | What it proves | Commands / evidence |
|---|---|---|
| Static | Repository scripts and manifests are syntactically reviewable. | `make ci`, `git diff --check`, GitHub Actions. |
| Host substrate | The illustrative lab host can boot nested microVMs and enforce Tier-1/Tier-2 controls. | `platform/validate/nested-smoke`, `platform/validate/acceptance`, substrate receipt. |
| Promotion control plane | A specific source commit can be dry-run, promoted, smoke-tested, status-checked, and rolled back. | `control-plane/promote-agent`, `smoke-agent`, `status-agent`, `rollback-agent`. |
| Production canary | A real workload meets auth, tool-policy, egress, audit, rollback, and SLO gates beside the legacy path. | Canary receipt, audit sink proof, rollback drill, baseline comparison. |

## Static validation

Run from the repository root:

```bash
make ci
git diff --check
```

`make ci` is intentionally safe for CI. It does not require VM access or secrets.

## Substrate validation

Run only on an isolated lab host with nested virtualization enabled:

```bash
platform/validate/nested-smoke
platform/validate/acceptance
```

A passing acceptance run should prove:

1. Tier-1 health responds locally.
2. Running image digest matches the pinned manifest.
3. Tier-2 microVM boots.
4. Tier-2 default-deny egress blocks external network access (both direct IP and external DNS resolution).
5. Tier-2 DNS exfiltration attempt is blocked.
6. Teardown leaves zero residual containers/tasks.

## Promotion and rollback validation

A valid promotion receipt should include:

- exact source commit;
- release label and release path;
- dry-run plan reviewed before apply;
- previous release target captured before flip;
- post-apply service state;
- live symlink target;
- live source SHA read back from the runtime;
- rollback command and result;
- post-rollback smoke/status output.

## Security gate validation

Before a workload is described as production-ready, the evidence packet must include:

- token/auth denial for missing or invalid credentials;
- valid-token attribution without exposing token values;
- denied tools absent from the tool listing;
- unknown tools failing closed;
- default-deny egress negative test;
- no raw secrets in logs, manifests, images, or receipts;
- audit events for auth, tool, egress, alignment, and rollback paths;
- rollback under the stated recovery target.

## Claim discipline

Use these terms precisely:

- **Implemented** — code or scripts exist in the repository.
- **Static-validated** — static checks ran and passed.
- **Host-validated** — a lab host executed the substrate checks and produced evidence.
- **Production-ready** — a real canary produced the security, rollback, audit, and SLO evidence.

If a command cannot be run in the current environment, record it as **not run** rather than implying it
passed.
