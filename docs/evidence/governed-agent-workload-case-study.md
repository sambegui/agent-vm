# Case Study: Governing an OpenShell/Hermes Agent Workload

This case study is a sanitized public walkthrough for reading the `BoundaryKit Agent VM`
architecture. It is not a product claim, customer deployment claim, live topology map, or proof that a
production workload is ready.

## Scenario

An AI-agent workload receives approved input from an operator-facing workflow:

1. a message or task request;
2. attached or retrieved context that may contain hostile instructions;
3. a need to call tools or a model provider to complete the task.

The workload is treated as a probabilistic actor. It may misread the request, follow malicious
instructions in content, invoke the wrong tool, attempt credential access, or try to reach data beyond
the approved scope.

The public architecture places that workload inside an OpenShell sandbox running Hermes Agent, with
rootless Podman runtime posture, a managed provider boundary, and evidence receipts for measured
behavior.

## Control path

```text
operator intent
  -> policy and promotion boundary
  -> OpenShell sandbox running Hermes Agent
  -> rootless Podman runtime posture
  -> managed provider boundary
  -> NUC-class VM substrate
  -> public receipts and recovery expectations
```

## Risks addressed

- **Prompt injection:** task content instructs the agent to ignore policy or reveal hidden context.
- **Credential access attempts:** the agent asks for environment variables, key material, provider
  tokens, or raw secret values.
- **Network exfiltration:** the agent tries direct outbound access, DNS exfiltration, SSRF, or lateral
  movement.
- **Filesystem escape:** the agent attempts to read or write outside the approved sandbox scope.
- **Provider misroute:** model/tool-provider access breaks or points to an unapproved path.
- **Runtime drift:** public claims no longer match what was measured.

## Expected controls

1. **Policy and promotion boundary**
   - Changes are reviewed before stronger claims are made.
   - Missing policy follows a fail-closed posture.
   - Rollback and recovery expectations include a named rollback target before stronger claims are made.

2. **OpenShell sandbox boundary**
   - Agent execution is treated as lower trust.
   - Tool, file, and network behavior are constrained.
   - Default-deny egress is the starting posture; allowed provider paths are explicit exceptions.
   - Negative tests record denied crossing attempts.

3. **Rootless runtime posture**
   - The public case study favors rootless Podman.
   - A privileged Docker daemon or broad host socket is not part of the public runtime claim.

4. **Managed provider boundary**
   - The sandbox sees a placeholder or reference, not raw provider credentials.
   - Secrets-by-reference is the public rule; raw provider tokens never enter public examples or receipts.
   - Credentials resolve outside the sandbox boundary.
   - Broken provider routing fails closed.

5. **Evidence receipts**
   - Each measured boundary has a public-safe summary.
   - Each receipt includes non-claims.
   - Private logs, hostnames, IPs, VM names, ports, routes, key names, and incident details stay out of
     public docs.

## Public evidence level

| Evidence level | What it supports | What it does not support |
|---|---|---|
| Architecture narrative | The public control path is understandable. | Runtime behavior is proven. |
| Static repo checks | Public docs and scripts are reviewable. | A sandbox or provider path actually ran. |
| Reference-lab validation | Generic `platform/` fixtures passed in a lab. | Current Agent VM runtime uses those exact fixtures. |
| Boundary measurement | One named boundary refused a negative-test matrix. | Neighboring or deeper boundaries are proven. |
| Production proof | A real workload passed canary, auth, egress, audit, rollback, and SLO gates. | General safety for all future workloads. |

## Current public receipts

- [Boundary receipt #1 - inner sandbox](boundary-receipt-01-inner-sandbox.md) summarizes refused
  egress, SSRF, lateral movement, external DNS, read-only filesystem, and non-root checks.
- [Boundary receipt #2 - inference boundary](boundary-receipt-02-inference-boundary.md) summarizes
  placeholder-in-sandbox credentials and fail-closed behavior on the governed model path.

## Reviewer takeaway

Read this as an operating model:

> autonomous agent workloads are treated as untrusted, their authority is mediated by policy, provider
> access is kept outside the sandbox boundary, claims are tied to evidence, and rollback remains part
> of the definition of done.

Read this alongside [`../verification.md`](../verification.md), [`../threat-model.md`](../threat-model.md),
[`boundary-receipt-01-inner-sandbox.md`](boundary-receipt-01-inner-sandbox.md), and
[`boundary-receipt-02-inference-boundary.md`](boundary-receipt-02-inference-boundary.md).
