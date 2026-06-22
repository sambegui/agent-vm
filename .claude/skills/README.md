# BoundaryKit Agent Skills

Agent skills committed to the BoundaryKit repo so they load when a Claude session is rooted at the BoundaryKit repo.

## Authored for BoundaryKit

- `context7-docs-lookup` — verify library/API usage against current docs via Context7 before changing code.
- `git-hygiene` — commit confirmed changes often as a cheap undo stack; squash clean before publishing.

## Vendored from NemoClaw (NVIDIA, Apache-2.0)

The `nemoclaw-user-*` skills are operational guides for running the NemoClaw / NemoHermes / OpenShell stack that BoundaryKit deploys. They are copied from the upstream NemoClaw repo (generated from its docs) and keep their `license: Apache-2.0` frontmatter and NVIDIA attribution.

- **Snapshot.** They do not auto-update with NemoClaw releases; refresh by re-copying from upstream.
- **Trimmed.** The upstream `evals/` test fixtures were omitted; each `SKILL.md` and its `references/` are intact.
- **CLI note.** These describe the generic NemoClaw CLI surface. When operating the Hermes orchestrator, the host CLI is `nemohermes` rather than `nemoclaw`.

Vendored: `nemoclaw-user-overview`, `-get-started`, `-configure-inference`, `-manage-policy`, `-monitor-sandbox`, `-deploy-remote`, `-configure-security`, `-manage-sandboxes`, `-reference`.
