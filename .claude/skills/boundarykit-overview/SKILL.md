---
name: boundarykit-overview
description: Orientation to the BoundaryKit project and repository — what it is, how the public repo is laid out, and the public/private documentation boundary. Use when starting work in the BoundaryKit repo, onboarding, deciding where content belongs, or before publishing or sharing anything. Trigger keywords - what is boundarykit, boundarykit overview, repo layout, project structure, public vs private, where does this go, boundarykit docs, contribute to boundarykit, where should this live.
---

# BoundaryKit Overview

BoundaryKit governs untrusted agent workloads with promotion controls, sanitization, and evidence. This repository is the public-facing project: sanitized reference architecture, documentation, and evidence derived from private local testing and development.

## Repository layout (public tier)

- `docs/` — public documentation source, including `docs/evidence/` receipts, `docs/public-private-boundary.md`, and `docs/declassification-checklist.md`.
- `site/` — the built public site.
- `platform/`, `control-plane/`, `deploy/` — reference architecture and deployment material.
- `examples/` — illustrative examples (fictional values only).
- `scripts/` — tooling, including `scripts/public-safety-scan` (the leak scanner).
- `README.md`, `SECURITY.md` — project introduction and security policy.

## Public / private discipline

Knowledge flows outward through tiers; nothing crosses a boundary it isn't cleared for. **Default-deny: unsure means private.**

- **Public:** the git-tracked paths above. Newly written, illustrative, fictional values only.
- **Private:** `.local/` and `.superpowers/` are gitignored — the source of truth where real infrastructure and raw research live. Partner-specific and business/strategy material is also private.

**Recreate, don't sanitize in place.** To publish, write a fresh doc with placeholder values into the public tier; never move a private file down.

## Before publishing or sharing

1. Read `docs/public-private-boundary.md` and walk `docs/declassification-checklist.md`.
2. Run `scripts/public-safety-scan <path>` and `git diff --check`.
3. Manually review for what the scanner misses: raw IP addresses, messaging tokens or numeric IDs, custom SSH key names, host / VM / service names, NAS or mount paths, and image digests. A scanner PASS is necessary, not sufficient.
4. Unsure about any item → stop and keep it private.

## Development practice

Use the `context7-docs-lookup` skill to verify external library and API usage against current docs before changing code, and the `git-hygiene` skill to commit confirmed changes often and squash clean before publishing.
