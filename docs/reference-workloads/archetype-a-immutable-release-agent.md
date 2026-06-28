# Archetype A - reference immutable-release agent

This is a reference acceptance-suite workload, not the current public Agent VM runtime story. It
models a Python application versioned by **git commit** and deployed as an **immutable release**
selected by a `current` symlink.

## Shape

- Source: a git repository; a release is an exact commit.
- Runtime selection: `/srv/demo-agent/current -> /srv/demo-agent/releases/<sha>-<label>`.
- Services: `agentd.service` runs the orchestrator; additional surfaces run as gateway profiles —
  `agent-gateway@core` (`cli` mode), `agent-gateway@mcp` (`script` mode).

## How the platform hosts it

- **Promote** an exact commit:
  `control-plane/promote-agent --sha <sha> --label <l> --worktree <p>` → `git archive` ship →
	  `.release.json` provenance -> atomic symlink flip -> restart -> verify (active, symlink, source SHA).
- **Status / drift:** `control-plane/status-agent` re-derives the live source SHA (3-tier) and flags
  drift against the recorded truth.
- **Rollback:** `control-plane/rollback-agent --to <prev-release>` (the previous `current` target is
  recorded before every promote).
- **Multi-profile:** per-profile `current` symlinks give each surface its own runtime version, so a
  smoke profile can run a test build while the core profile stays stable.
