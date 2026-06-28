# Boundary receipt #1 — inner sandbox, measured

This is a sanitized public summary of a privately held boundary receipt. It records the first
**adversarially measured** isolation boundary in the `BoundaryKit` reference architecture: the
**inner sandbox** that wraps an agent runtime. It is a generalized lesson, not a live infrastructure
log — no private hosts, addresses, image digests, or command transcripts appear here.

The narrative it advances is deliberately small: one inner runtime boundary moved from *designed* to
*measured*. The honest frame is a **sequence**, not a completion. Neighboring boundaries, including
credential mediation and outer containment, require their own receipts.

## Scope

| Item | Value |
|---|---|
| Boundary measured | Inner sandbox around an agent runtime (container + kernel filesystem policy + application-layer egress proxy + network namespace) |
| Method | Adversarial negative-test matrix run from inside the sandbox |
| Runtime identity | Non-root process |
| Default policy | Read-write workspace only; system paths read-only; **deny-by-default egress** |
| Mutating production systems | None |
| Secrets included | None |
| Claim supported | The inner sandbox boundary holds under the tested probes — **not** credential mediation, outer containment, or production readiness |

## Negative-test matrix

Each row is an attempt to cross the boundary. The boundary holds when the attempt is **refused**.

| Probe | Observed | Verdict |
|---|---|---|
| External HTTPS egress | Connection refused by the application-layer proxy (403 CONNECT-tunnel failure) | Blocked |
| External HTTP egress | Request refused (403) | Blocked |
| Cloud-metadata SSRF (link-local `169.254.0.0/16` range), HTTP and HTTPS | Refused with an explicit policy-denied response | Blocked |
| LAN lateral movement to an internal service | Refused | Blocked |
| **Raw-socket bypass of the proxy** | Refused even with a direct socket — the denial is **structural, not merely policy** | Blocked |
| External DNS resolution | No external resolver available | Blocked |
| Write to a read-only system path | Permission denied by kernel filesystem policy | Denied |
| Write to the designated workspace | Allowed | Expected |
| Provider credentials in process environment | None present | See non-claims |

**Headline:** deny-by-default egress was confirmed at the application-layer proxy *and* held when an
attacker bypassed the proxy with a raw socket — so egress denial does not depend on a single
cooperating control. Cloud-metadata SSRF, LAN lateral movement, external egress, and external DNS
were all refused; the filesystem is read-only outside the workspace; the process runs non-root.

## What this receipt does NOT claim

This is the part that matters most, and the part almost nobody publishes. The discipline of the
architecture is that unproven boundaries are named, not implied.

- **This is the inner sandbox boundary, not an outer containment boundary.** It does not prove that a
  sandbox escape is contained by a VM, hypervisor, or host-management boundary.
- **The credential-non-leakage check is scoped.** The original check confirmed no provider credential
  was present in this sandbox, but it did not by itself prove the governed model path. That follow-on
  is covered separately by [boundary receipt #2](boundary-receipt-02-inference-boundary.md).
- **No formal proof yet.** The matrix is empirical. A formal "deny-except-allowlist" proof that
  searches for counterexamples is a separate, complementary step.

## Next boundary classes

The immediate credential follow-on is now public as
[boundary receipt #2](boundary-receipt-02-inference-boundary.md). Deeper containment claims, such as
whether an escaped sandbox is confined by an outer virtualization or host-management-plane boundary,
remain separately scoped. Until a public summary exists for that boundary, language such as "hard
boundary," "proven isolation," or "unescapable" is intentionally withheld.

## Evidence level

Read this against the [verification model](../verification.md). This receipt is a **boundary
measurement**: stronger than a lab smoke test because the boundary was attacked, weaker than a
production canary because no real workload, credential, or SLO is in scope. It sits between
host-substrate validation and production-readiness evidence, and it covers exactly one boundary.

Read alongside [boundary receipt #2 — inference boundary](boundary-receipt-02-inference-boundary.md),
the [governed-agent-workload case study](governed-agent-workload-case-study.md), and the
[substrate validation receipt](substrate-validation-receipt.md).
