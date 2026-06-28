# Reference substrate validation state

> **Status:** Public example state for the reference acceptance suite. This file is not a raw evidence
> receipt, not a live lab transcript, and not the current Agent VM runtime map.

The `platform/` tree keeps a generic acceptance-suite fixture for VM, image, reconcile/align, and
microVM-style checks. Use this file only as a compact example of the claim shape that a fictional lab
could record after running the suite.

## Example scope

| Area | Example result | Public interpretation |
|---|---|---|
| Reference VM smoke | `example_only_pass` | The fictional `agent-platform` fixture exposed `/dev/kvm` to a nested smoke test. |
| Tier-1 service | `example_only_pass` | The demo health endpoint responded and matched the pinned manifest. |
| Tier-2 microVM job | `example_only_pass` | The demo job booted, exited cleanly, and reported zero residual runtime artifacts. |
| Default-deny egress | `example_only_pass` | Direct outbound and DNS-style exfiltration attempts were blocked in the fixture. |
| Timeout and teardown | `example_only_pass` | A long-running demo job hit its timeout and cleanup check. |

## Example commands

These commands are illustrative and host-dependent:

```bash
platform/validate/nested-smoke
platform/validate/acceptance
```

They require a configured reference lab with virtualization support, locally available tooling, and
fictional values such as `agent-platform`, `10.0.0.60`, and `demo-registry.example`.

## Non-claims

This state file does not claim:

- that the current public Agent VM runtime is implemented with this reference fixture;
- that a private deployment, client workload, or production service passed these checks;
- that raw command transcripts, hostnames, VM names, registry paths, key names, or incident details are
  present;
- that reference-lab validation is the same as production-ready evidence.
