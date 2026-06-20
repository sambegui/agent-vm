# Declassification Checklist

Use this checklist before publishing public docs, examples, scripts, release notes, or pull request
text from `BoundaryKit`.

## Required Result

The public diff must be explainable as a standalone reference architecture. It must not require, imply,
or reveal a private deployment.

## Content Checks

- [ ] All examples are marked `example_only`, `illustrative`, or clearly fake.
- [ ] No private source code, image layers, SBOMs, manifests, evidence logs, task ledgers, raw
      transcripts, screenshots, or operator approvals are copied into the public repo.
- [ ] No real hostnames, IP addresses, registry paths, source paths, service names, client names,
      topology, runtime paths, service units, tunnels, DNS settings, or deploy state appear.
- [ ] No credentials, private key material, token values, token ids, token hashes, signing key paths,
      `.env` file contents, or secret values appear.
- [ ] Secret examples use references only, such as `secret://demo/...`.
- [ ] Artifact examples use fake registries and fake digests.
- [ ] Tool examples use fake tool names and fake schema hashes.
- [ ] Evidence examples are fake receipts, not excerpts from real logs.
- [ ] Public text does not claim that a private system, client, or workload was validated.

## Governance Checks

- [ ] The diff frames agents as untrusted, tool-wielding workloads.
- [ ] Trust boundaries are explicit.
- [ ] Capability escalation is gated.
- [ ] Promotion requires evidence.
- [ ] Rollback is represented as a tested drill.
- [ ] Audit records omit secret values.
- [ ] Runtime mutation, public image publishing, and registry pushes remain separate approval gates.

## Scan And Review

Run:

```bash
scripts/public-safety-scan
git diff --check
```

Then review the diff manually. Treat scanner success as necessary but not sufficient: it does not
prove conceptual safety.

## Stop Conditions

Stop and rewrite before publication if any item is uncertain. Public examples should be regenerated
from fake values rather than edited down from private evidence.
