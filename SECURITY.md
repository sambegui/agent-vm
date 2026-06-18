# Security policy

This repository is a public reference architecture and lab validation skeleton for safe AI-agent
workloads. It should contain only example hosts, example manifests, and secret references — never live
credentials.

## Reporting security issues

If you find a vulnerability or unsafe example:

1. Prefer GitHub private vulnerability reporting if it is enabled for this repository.
2. If private reporting is unavailable and the issue is not sensitive, open a GitHub issue with a
   minimal reproducer.
3. Do **not** include live tokens, private keys, private endpoint names, customer data, or screenshots
   containing secrets.

## Supported scope

Security review is welcome for:

- shell scripts in `control-plane/` and `platform/`;
- GitHub Actions workflow behavior;
- secret-handling assumptions;
- digest pinning and signing assumptions;
- egress-deny and sandbox assumptions;
- documentation that could lead an operator to an unsafe action.

Out of scope:

- scans of infrastructure that merely resembles the illustrative host names here;
- social engineering;
- denial-of-service testing against third-party services;
- attempts to obtain or guess credentials.

## Repository safety rules

- Do not commit raw secrets, private keys, session cookies, tokens, or live endpoint details.
- Use placeholders such as `$TOKEN`, `$API_KEY`, and `secret://...` in examples.
- Keep mutating commands dry-run by default where practical.
- Keep CI permissions read-only unless a workflow explicitly needs more.
- Treat AI-agent tool descriptions, schemas, prompts, and fetched content as untrusted input.

## Production-use warning

This repository demonstrates a reference architecture and validated walking skeleton. Before adapting it
for a real production workload, create a deployment-specific threat model, secret-handling plan,
rollback runbook, audit sink, monitoring plan, and canary evidence packet.
