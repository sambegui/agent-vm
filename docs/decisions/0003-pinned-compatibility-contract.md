# ADR 0003 — Pinned compatibility contract for coupled agent stacks

## Status
Accepted.

## Context
An agent runtime is rarely one component. A typical stack couples a sandbox runtime, an agent
framework, and an orchestrator — often several still on pre-1.0 (`0.0.x`) versions, where minor
releases change interfaces without warning. Building such a stack by "take the latest of each" is how
you ship a runtime that *starts* healthy but is quietly broken: a gateway that reports ready while the
agent's brain cannot complete a single request, because one layer baked an inference mode the upstream
path can't satisfy.

Two failure shapes recur:
- **Silent drift.** A convenience shortcut (an unpinned tarball, a floating `latest` base image) pulls
  a different version than intended, reverting a fix or changing a default. The build succeeds; the
  behavior regresses.
- **Coupled defaults.** A setting chosen by one layer's auto-selection (e.g. an inference API mode
  probed at onboard time) is incompatible with another layer's runtime, and the mismatch only surfaces
  at first real use.

## Decision
Treat the stack as a **pinned compatibility contract**, not a set of independently-latest parts:

- **Pin by digest / SHA, verify on fetch.** Every externally-fetched component — base images, source
  tarballs — is pinned to an exact version and integrity-checked (digest or `SHA256`) at build time. A
  build must fetch the bytes you reviewed, or fail.
- **No floating bases in a production image.** `latest` tags and unpinned `install`s are prohibited in
  the release path; they are the mechanism of silent drift.
- **Optional components are tolerant; the core is not.** A non-essential add-on (a dashboard, an
  optional adapter) may warn-and-skip, but it may never hard-fail the core runtime — and the core must
  fail loudly rather than ship subtly broken.
- **Make the coupled defaults explicit.** Where one layer auto-selects a value another layer depends on
  (inference API mode, transport, credential shape), set it explicitly and reproducibly in provisioning
  rather than relying on a probe that can pick an incompatible default.
- **Validate the contract before the long rebuild.** Prove the pin and the wiring with a fast check
  (test suite, config inspection, a single end-to-end request) before committing to an expensive image
  build.

## Consequences
- Builds are **reproducible**: the same inputs produce the same runtime, and a regression points at a
  pin change rather than the weather.
- "Healthy" means *functional*, not merely *started* — a broken brain fails the build, not the user.
- The provisioning artifact, not a live hand-edit, is the source of truth; a fix that a rebuild would
  wipe is not considered done.
- The cost is up-front rigor: every bump is a deliberate, reviewed change to the contract. That is the
  intended trade — durability over convenience for anything that touches production.
