# Runtimes — live truth (ILLUSTRATIVE EXAMPLE)

> Example of the control plane's state-as-truth file. **All values are fictional.** A real deployment
> regenerates the markers with `control-plane/status-agent --update` (which re-derives live truth and
> rewrites this host-local file only — never the runtime).

## archetype-a (immutable-release agent)
- service: agentd.service
- current_link: /opt/agent/current
- current_release: 1a2b3c4d5-feature-x
- current_sha: 1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b
- rollback_target: 0f9e8d7c6-prev-stable
- last_verified: 2026-01-01T00:00:00Z (status-agent --update)

## archetype-b (package-install agent pool)
- services: agent-pool.service (:18789), agent-pool-worker.service (:19001)
- version: 1.4.2
- rollback_target: 1.4.1
- model: package version pin (capture-first)
