# Reference acceptance-suite receipt

This receipt summarizes public, non-secret evidence recorded for the generic `platform/` reference
acceptance suite. It is a sanitized public evidence packet for a fictional lab fixture, not a live
infrastructure log and not the current Agent VM runtime map.

## Scope

| Item | Value |
|---|---|
| Repository area | `platform/` reference acceptance suite |
| Evidence type | Reference-lab validation |
| Mutating production systems | None |
| Secrets included | None |
| Claim supported | Generic lab fixture passed its acceptance checks |
| Claim not supported | Current private deployment state, production readiness, or complete outer containment proof |

## Recorded evidence

| Check | Evidence | Result |
|---|---|---|
| Nested microVM smoke | Reference lab showed a hardware-backed microVM-style boot check. | PASS |
| Reference VM validation | Fictional `agent-platform` lab fixture completed the substrate check. | PASS |
| Higher-risk job fixture | Example job printed the expected reference output. | PASS |
| Default-deny egress (direct IP) | External HTTP attempt returned blocked / unreachable instead of succeeding. | PASS |
| Default-deny egress (DNS exfiltration) | DNS resolution attempt for external domain returned blocked. | PASS |
| Timeout and teardown | Timeout path returned the expected timeout code and reported zero residual runtime artifacts. | PASS |

## Acceptance subset

The expected final acceptance summary for the configured reference lab is:

```text
PASS=6 FAIL=0
```

The six checks are:

1. reference service health responds locally;
2. running image digest matches the pinned manifest;
3. higher-risk sandbox fixture boots;
4. default-deny egress blocks external network access;
5. default-deny egress blocks DNS exfiltration attempts;
6. teardown leaves zero residual runtime artifacts.

## Relationship to current public evidence

This receipt is useful background for the reference acceptance suite. The current public case-study
evidence starts with narrower measured boundaries:

- [Boundary receipt #1 - inner sandbox](boundary-receipt-01-inner-sandbox.md)
- [Boundary receipt #2 - inference boundary](boundary-receipt-02-inference-boundary.md)

Those receipts answer "does this named boundary refuse a crossing?" or "does this credential boundary
hold?" This reference receipt answers "did the generic lab fixture pass its acceptance checks?"

## Non-claims

This receipt does **not** claim:

- that this repository is a turnkey production product;
- that every possible agent framework has been deployed;
- that a live customer or owner-facing workload passed canary gates;
- that cloud-hosted infrastructure exists behind example host names;
- that any private credential, token, endpoint, VM name, host path, or incident detail is present;
- that the current Agent VM runtime is the same as the reference acceptance suite.

## Follow-up evidence needed for production readiness

Before any real workload is called production-ready, capture:

- exact source SHA or artifact digest;
- policy version and fail-closed test;
- auth allow/deny events without token values;
- provider-boundary proof without printing credential material;
- egress-deny audit event;
- rollback drill output and elapsed time;
- canary health/SLO comparison against a baseline.
