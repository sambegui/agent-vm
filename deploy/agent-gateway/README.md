# deploy/agent-gateway — templated multi-profile gateway layout

A single systemd **template unit** hosts every gateway profile of an agent runtime, so each
channel/profile is an explicit, independently-restartable service with **one** unambiguous runtime
source. This eliminates the "which runtime is this profile actually importing, and did I restart the
right service?" failure mode that arises when many profiles share one mutable runtime symlink and set
the runtime via conflicting `Environment=` lines across fragment + drop-ins.

## How it maps onto a host

| This repo | Host target (deploy time) |
|---|---|
| `systemd/agent-gateway@.service` | `/etc/systemd/system/agent-gateway@.service` |
| `_lib/launch` | `/opt/agent/_lib/launch` (0755) |
| `gateways/<p>/env` | `/opt/agent/gateways/<p>/env` (0640) |

Created on the host at deploy time (state/secrets-bearing, not versioned): `gateways/<p>/current`
(symlink → `/opt/agent/releases/<sha>-<label>`), `gateways/<p>/home/` (`AGENT_HOME`), `gateways/<p>/logs/`.

## The invariant

The runtime source (`AGENT_ROOT` / `PYTHONPATH`) is declared **exactly once**, in the profile's `env`,
pointing at that profile's **own** `current` symlink. The unit sets no `PYTHONPATH`; no drop-in may.
Promoting a new runtime to one profile never touches the others.

## Two entrypoint modes (one template)

- `AGENT_GATEWAY_MODE=cli` → launcher runs `python -m agent_cli.main gateway run --replace`
  (standard CLI gateway; `core` profile).
- `AGENT_GATEWAY_MODE=script` → launcher runs `python $AGENT_PROFILE_EXEC` (bespoke per-profile
  entrypoint; `api`, `mcp` profiles).

## Lifecycle (per profile, fully isolated)

```bash
systemctl start|stop|restart|status agent-gateway@<p>   # p = core | api | mcp
systemctl list-units 'agent-gateway@*'                  # every gateway, nothing else
```

## Validate locally (no host, no root)

```bash
bash -n _lib/launch
systemd-analyze verify systemd/agent-gateway@.service || true   # /opt/agent path warnings are expected
# prove per-profile command/runtime/SHA resolution without running anything:
tmp=$(mktemp -d); printf '{"sha":"deadbeef1234","label":"local-test"}' > "$tmp/.release.json"
for p in core api mcp; do
  ( set -a; . "gateways/$p/env"; set +a
    AGENT_ROOT="$tmp" AGENT_LAUNCH_DRYRUN=1 bash _lib/launch )
done; rm -rf "$tmp"
```
