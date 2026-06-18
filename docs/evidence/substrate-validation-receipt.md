# Substrate validation receipt

This receipt summarizes the public, non-secret evidence recorded in
[`platform/state/substrate-validation.md`](../../platform/state/substrate-validation.md). It is a
sanitized portfolio evidence packet, not a live infrastructure log.

## Scope

| Item | Value |
|---|---|
| Repository area | `platform/` walking skeleton |
| Evidence type | Lab-host substrate validation |
| Mutating production systems | None |
| Secrets included | None |
| Claim supported | Host-validated substrate skeleton, not production service readiness |

## Recorded evidence

| Check | Evidence | Result |
|---|---|---|
| Nested microVM smoke | Firecracker microVM booted with KVM acceleration in the initial runtime guest. | PASS |
| Golden VM nested validation | Firecracker microVM booted with KVM acceleration inside the illustrative `agent-platform` VM. | PASS |
| Tier-2 Kata/containerd job | Kata runtime executed the example job and printed `hello-from-microvm`. | PASS |
| Default-deny egress (direct IP) | External HTTP attempt returned blocked / unreachable instead of succeeding. | PASS |
| Default-deny egress (DNS exfiltration) | DNS resolution attempt for external domain returned blocked. | PASS |
| Timeout and teardown | Timeout path returned the expected timeout code and reported zero residual runtime artifacts. | PASS |

## Acceptance subset

The expected final acceptance summary for the configured lab host is:

```text
PASS=6 FAIL=0
```

The six checks are:

1. Tier-1 health endpoint responds locally.
2. Tier-1 running digest matches the pinned manifest.
3. Tier-2 microVM boots.
4. Tier-2 default-deny egress blocks external network access (direct IP).
5. Tier-2 default-deny egress blocks DNS exfiltration attempts.
6. Tier-2 teardown leaves zero residual runtime artifacts.

## Non-claims

This receipt does **not** claim:

- that this repository is a turnkey production product;
- that every possible agent framework has been deployed;
- that a live customer or owner-facing workload has passed canary gates;
- that cloud-hosted infrastructure exists behind the example host names;
- that any private credential, token, or endpoint is present in the repository.

## Follow-up evidence needed for production readiness

Before any real workload is called production-ready, capture:

- exact source SHA and artifact digest;
- cosign verification output;
- SBOM/provenance reference;
- tool-policy hash and fail-closed test;
- auth allow/deny events without token values;
- egress deny audit event;
- rollback drill output and elapsed time;
- canary health/SLO comparison against a baseline.
