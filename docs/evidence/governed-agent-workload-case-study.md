# Case Study: Treating an Agent as an Untrusted Workload

This case study is an illustrative, vendor-neutral walkthrough for reading the `BoundaryKit`
architecture. It is not a product claim, customer deployment claim, or proof that a production
workload is ready. Its purpose is to show how the repository's trust boundaries, operational
controls, and evidence model apply when an autonomous AI-agent workload handles untrusted input.

## Scenario

An AI agent receives three inputs from an approved collaboration surface:

1. a team message asking for a summary and follow-up plan;
2. an attached document with task details and embedded instructions;
3. an external link that may contain supporting context.

The agent is a probabilistic actor. It may misread the request, follow malicious instructions in the
document, invoke the wrong tool, or attempt to reach data beyond the approved scope. The message,
document, link, model output, tool arguments, and retrieved content are all treated as untrusted.

The workload objective is narrow: process approved inputs, produce a structured output, and leave an
audit trail that can be reviewed without exposing secrets.

## Risk

The architecture assumes the agent can be compromised, misdirected, or confused. The relevant risks
include:

- **Prompt injection:** the attached document or linked content instructs the agent to ignore policy,
  reveal hidden context, or call unauthorized tools.
- **Secret access attempts:** the agent asks for credentials, environment variables, local key
  material, or raw token values instead of using secrets-by-reference.
- **File exfiltration attempts:** the agent tries to read or copy files outside the approved input
  set.
- **Lateral movement attempts:** the agent tries to reach host services, internal networks, adjacent
  runtimes, or other workload state.
- **Dependency or tool misuse:** generated code, package downloads, shell commands, or parser tools
  behave differently than intended.

These are workload-governance risks, not chatbot UX problems. The architecture is designed around
blast-radius control when the workload behaves badly.

## Control path

The request moves through explicit controls before any high-blast-radius action is allowed.

1. **Promotion control plane**
   - Runtime code is promoted by exact source revision or equivalent immutable artifact.
   - Mutations are dry-run first.
   - The previous release target is recorded so rollback remains available.
   - Drift checks re-derive what is running instead of trusting a deployment note.

2. **Isolation substrate**
   - Long-running services run in a bounded runtime layer.
   - Higher-risk execution can be escalated to an ephemeral sandbox.
   - The VM is an implementation substrate; the deeper boundary is between operator intent,
     governed runtime state, and untrusted agent execution.

3. **Default-deny egress**
   - Network access starts closed.
   - External reachability must be explicitly allowed.
   - Direct IP and DNS exfiltration attempts are negative-test candidates.

4. **Fail-closed tool and data gates**
   - Tool policy is allowlist-based.
   - Missing policy denies access instead of falling back to broad permissions.
   - Unknown tools, denied files, and denied network paths should leave audit evidence.

5. **Secrets-by-reference**
   - The agent receives references, handles, or scoped capabilities rather than raw secret values.
   - Receipts and logs must prove denial or use without printing token material.

6. **Audit trail**
   - The system records source identity, artifact or image digest, policy decision, egress denial,
     alignment result, and rollback target.
   - The audit trail is useful only if it separates what was requested, what was allowed, what was
     denied, and what actually ran.

7. **Rollback target**
   - The rollback target is part of the control path, not an afterthought.
   - Recovery evidence matters as much as deployment evidence because autonomous workloads can fail
     in surprising ways.

## Expected result

For this scenario, a governed run should end with these outcomes:

- unauthorized file, tool, credential, and network access is denied;
- default-deny egress blocks unapproved outbound connections;
- each boundary hit is auditable without exposing secret values;
- host/runtime spillover is prevented by isolation and least-authority policy;
- the promoted runtime can be compared against its expected source or digest;
- rollback remains available if the workload, policy, or deployment proves unsafe.

The result is not "the agent is trusted." The result is that the agent can be useful while still
being governed as an untrusted workload.

## Evidence level

Do not collapse architecture narrative, static checks, lab validation, and production proof into one
claim.

| Evidence level | What it supports | What it does not support |
|---|---|---|
| Illustrative narrative | The threat model and control path are understandable. | No runtime behavior is proven. |
| Static repo checks | Scripts, manifests, links, and public docs are reviewable. | A VM or sandbox actually ran. |
| Lab validation | The host substrate can run the acceptance checks in an isolated lab. | A real workload is production-ready. |
| Promotion validation | Delivery controls, status checks, and rollback mechanics work for a promoted revision. | Policy coverage for every workload. |
| Production proof | A specific real workload passed canary, auth, egress, audit, rollback, and SLO gates. | General safety for all future workloads. |

This case study is an illustrative narrative. The repository also contains static repo checks and
lab validation receipts. Production proof requires a separate workload-specific canary packet with
auth, tool-policy, egress, audit, rollback, and SLO evidence.

## Reviewer takeaway

Read this as an operating model, not as a claim that a sandbox alone is sufficient:

> autonomous agent workloads are treated as untrusted, their authority is mediated by policy, their
> claims are tied to evidence, and rollback remains part of the definition of done.

Read this alongside [`../verification.md`](../verification.md), [`../threat-model.md`](../threat-model.md),
and [`substrate-validation-receipt.md`](substrate-validation-receipt.md).
