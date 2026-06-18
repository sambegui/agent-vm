# Substrate validation evidence

## Task 0 — in-guest nested microVM smoke (agent-runtime)
- Date: 2026-06-16
- Command: ssh agent-runtime 'bash /tmp/nested-smoke'
- Result: PASS — Firecracker v1.7.0 microVM booted HW-backed using /dev/kvm inside the current guest (Linux 4.14.174 on KVM; `Booting paravirtualized kernel on KVM` confirmed in Firecracker log).
- Note: the lab network blocked direct asset download during this smoke. Assets were staged into a
  temporary guest directory for that one run. The committed `platform/validate/nested-smoke` script is
  the canonical curl-based script. The guest operator account also needed membership in the `kvm`
  group for `/dev/kvm` access.

## Task 3 — in-new-VM nested validation (agent-platform)
- Date: 2026-06-16
- Command: scp platform/validate/nested-smoke agent-platform:/tmp/nested-smoke && ssh agent-platform 'bash /tmp/nested-smoke'
- Result: PASS — Firecracker v1.7.0 microVM booted HW-backed using /dev/kvm inside the new `agent-platform` VM.
- Evidence: output ended with `[smoke] HW-backed KVM boot confirmed via log` and `PASS: nested HW-backed microVM boots`.

## Task 8 — Kata/containerd Tier-2 validation (agent-platform)
- Date: 2026-06-16
- Runtime: Kata Containers static release `3.31.0` via containerd runtime `io.containerd.kata.v2`.
- Hypervisor evidence: `kata-runtime kata-env` reported QEMU at `/opt/kata/opt/kata/bin/qemu-system-x86_64`, Kata kernel `vmlinux-6.18.28-194`, and guest image `kata-ubuntu-noble.image`.
- Command: `~/platform/sandbox/sandbox-runner ~/platform/sandbox/jobspec.example.json`.
- Result: PASS — job printed `hello-from-microvm`, guest kernel `6.18.28`, `exit=0`, `teardown verified: 0 residual`, and an audit line.
- Egress evidence: egress job attempting `wget http://1.1.1.1` printed `BLOCKED` with `Network is unreachable`. DNS exfiltration test attempting `nslookup malicious-domain.com` also printed `BLOCKED`.
- Timeout evidence: timeout job returned `exit=124` after the hard timeout and `teardown verified: 0 residual`.

## Task 9 — Acceptance suite live validation (agent-platform)
- Date: 2026-06-18
- Preflight: Tier-1 health endpoint responded, the local registry responded, `containerd` reported a
  Server section, and no stale `job-*` containerd containers or tasks were present.
- Command: `bash platform/validate/acceptance`.
- Result: PASS — all six checks passed:
  - `tier1.health`
  - `alignment.aligned`
  - `tier2.microvm_boots`
  - `tier2.egress_deny`
  - `tier2.dns_exfiltrate_deny`
  - `tier2.teardown`
- Acceptance footer: `PASS=6 FAIL=0`.

## Task 10 — Acceptance suite after runner hardening (agent-platform)
- Date: 2026-06-18
- Scope: reran the full acceptance suite after adding per-run sandbox container IDs,
  stale-prefix pre-clean, trap-backed teardown, and a parameterized acceptance SSH target.
- Command: `bash platform/validate/acceptance`.
- Result: PASS — acceptance footer remained `PASS=6 FAIL=0`.

## Task 11 — Fresh provision/bootstrap acceptance validation (agent-platform)
- Date: 2026-06-18
- Scope: rebuilt the illustrative lab VM from the repo-controlled provisioning path, ran the
  repo-controlled runtime bootstrap, then reran the full acceptance suite.
- Commands:
  - `make provision` with local lab `AGENT_VM_*` overrides
  - `bash platform/validate/acceptance`
- Result: PASS — acceptance footer was `PASS=6 FAIL=0`.
