<!-- This file is git-tracked and world-readable (Public tier). Keep it sanitized; use fictional/placeholder values in any example. -->

# BoundaryKit — Agent Instructions

BoundaryKit governs untrusted agent workloads with promotion controls, sanitization, and evidence. This repository is the **public-facing** project: sanitized reference architecture, documentation, and evidence derived from private local testing and development.

## Public / private boundary — read this first

Knowledge flows outward through tiers, and nothing crosses a boundary it isn't cleared for. **Default-deny: if you cannot prove a file is public, treat it as private.**

- **Public (git-tracked):** `docs/`, `site/`, `platform/`, `control-plane/`, `deploy/`, `examples/`, `README.md`, `SECURITY.md`. Newly written, illustrative, fictional values only.
- **Private (gitignored):** `.local/` and `.superpowers/` are the source of truth where real infrastructure and raw research live. They never leave the host. Partner-specific and business/strategy material is also private and default-deny.

**Never publish from a private file in place.** To make something public, recreate it from scratch with fictional/placeholder values into the public tier — do not sanitize a private file and move it.

## Before moving any content toward `docs/`, `site/`, or a partner

1. Read `docs/public-private-boundary.md` and walk `docs/declassification-checklist.md`.
2. Run `scripts/public-safety-scan <path>` and `git diff --check`.
3. Manually review for what the scanner does not catch: raw IP addresses, messaging tokens or numeric IDs, custom SSH key names, host / VM / service names, NAS or mount paths, and image digests.
4. Unsure about any item → stop and keep it private.

The `boundarykit-overview` skill expands on the repo layout and this discipline.

## Development practice

- Verify external library, API, SDK, or CLI usage against current docs with the `context7-docs-lookup` skill before changing code — default to it over memory and generic web search.
- Commit confirmed changes often as cheap local checkpoints and squash into clean commits before publishing, per the `git-hygiene` skill. Branch first; never commit secrets.
