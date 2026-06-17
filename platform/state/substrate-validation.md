# Substrate validation evidence

## Task 0 — in-guest nested microVM smoke (agent-runtime)
- Date: 2026-06-16
- Command: ssh agent-runtime 'bash /tmp/nested-smoke'
- Result: PASS — Firecracker v1.7.0 microVM booted HW-backed using /dev/kvm inside the current guest (Linux 4.14.174 on KVM; `Booting paravirtualized kernel on KVM` confirmed in Firecracker log).
- Note: s3.amazonaws.com is blocked by egress proxy (squid ERR_ACCESS_DENIED). Assets were staged from host: firecracker binary + vmlinux.bin + bionic.rootfs.ext4 scp'd to guest /tmp/nested-smoke-assets/ and used in place of curl. The committed platform/validate/nested-smoke is the canonical curl-based script; the host-staging was a one-time workaround for this restricted environment. Also: admin user was added to the kvm group (sudo usermod -aG kvm admin) — required for /dev/kvm access.

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
- Egress evidence: egress job attempting `wget http://1.1.1.1` printed `BLOCKED` with `Network is unreachable`.
- Timeout evidence: timeout job returned `exit=124` after the hard timeout and `teardown verified: 0 residual`.
