# Archetype B — package-install agent (Node backend agent-pool)

A representative agent whose runtime is a **globally installed package** (versioned by package
version), run as **multiple instances** of the same binary differentiated by home directory and port.
A deliberately different deployment model from Archetype A — that contrast is what proves the platform
is agent-agnostic.

## Shape

- Source: a published package; a "release" is an exact package version.
- Runtime selection: the installed binary version (`/usr/local/bin/agent-pool`), pinned.
- Services: `agent-pool.service` — one instance per `HOME` + port (e.g. a primary instance and a
  worker instance), all running the same binary.

## How the platform hosts it

- **Capture-first:** `control-plane/status-pkg` records the installed version, the running instances,
  and a rollback target (prior version) into the state-as-truth files.
- **Promote / rollback:** `control-plane/promote-pkg` and `rollback-pkg` are **documented stubs** that
  describe the version-pin plan; they are implemented only once the package distribution is confirmed —
  the platform *audits* Archetype B before it *automates* it.

The two archetypes share one control-plane discipline (immutable selection, dry-run, drift detection,
recorded rollback) over two different runtime mechanics.
