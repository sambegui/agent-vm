# Verification model

This repository separates **architecture narrative**, **static validation**, **reference-lab
validation**, **boundary measurement**, and **production-readiness evidence**. Do not collapse those
into one claim.

## Verification levels

| Level | What it supports | What it does not support |
|---|---|---|
| Architecture narrative | The public trust-boundary model is understandable. | Runtime behavior, production readiness, or live topology. |
| Static validation | Public docs, scripts, examples, and generated site files are reviewable. | That a VM, sandbox, provider path, or workload actually ran. |
| Reference-lab validation | The generic `platform/` acceptance fixtures can run in a configured lab. | That the current Agent VM case-study runtime uses those exact fixtures. |
| Boundary measurement | One named boundary refused a defined set of adversarial crossing attempts. | That neighboring or deeper boundaries are proven. |
| Production-ready | A real workload produced canary, auth, egress, audit, rollback, and SLO evidence. | General safety for all future workloads. |

## Static validation

Run from the repository root:

```bash
make ci
scripts/public-safety-scan
git diff --check
```

`make ci` is intentionally safe for CI. It does not require VM access or secrets. The public safety
scan is necessary but not sufficient; manual declassification review is still required.

## Current public boundary measurements

- [Governed workload case study](evidence/governed-agent-workload-case-study.md) explains how the
  current OpenShell/Hermes workload is treated as untrusted before reading individual receipts.
- [Boundary receipt #1 - inner sandbox](evidence/boundary-receipt-01-inner-sandbox.md) summarizes
  egress, SSRF, lateral movement, external DNS, read-only filesystem, and non-root execution checks
  against the inner sandbox boundary.
- [Boundary receipt #2 - inference boundary](evidence/boundary-receipt-02-inference-boundary.md)
  summarizes placeholder-in-sandbox credential handling and fail-closed behavior on the governed model
  path.

Each receipt covers one boundary. Deeper containment claims, such as an escaped sandbox being confined
by an outer virtualization or host-management-plane boundary, require their own public summary before
they are described as measured here.

## Reference-lab validation

The `platform/` directory contains a generic reference acceptance suite. Its host-dependent commands
are illustrative and require a configured lab environment:

```bash
platform/validate/nested-smoke
platform/validate/acceptance
```

A passing reference-lab run supports the claim that the generic lab fixture passed. It does not prove
the current private system, a public managed service, or production readiness.

## Boundary receipt requirements

A valid public boundary receipt should include:

- the exact boundary under test, named precisely;
- a negative-test matrix where each row is a crossing attempt;
- the observed refusal or fail-closed behavior;
- an explicit "what this does not prove" section;
- no raw command transcripts, private addresses, private hostnames, token material, live VM names, or
  incident-specific details.

## Promotion and rollback evidence

A promotion or recovery receipt should include:

- exact source revision, artifact digest, policy version, or equivalent identifier;
- dry-run/review record before apply;
- rollback target captured before apply;
- post-change boundary checks;
- recovery or rollback result;
- remaining non-claims.

## Claim discipline

Use these terms precisely:

- **Implemented** - code, docs, or scripts exist in the repository.
- **Static-validated** - safe local checks ran and passed.
- **Reference-lab validated** - a configured lab host executed the generic acceptance suite.
- **Boundary-measured** - an adversarial behavior test confirmed one named boundary.
- **Production-ready** - a real workload produced canary, auth, egress, audit, rollback, and SLO
  evidence.

If a command cannot be run in the current environment, record it as **not run** rather than implying it
passed.
