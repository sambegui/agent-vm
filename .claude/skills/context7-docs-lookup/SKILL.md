---
name: context7-docs-lookup
description: Look up current, version-specific documentation and code examples for any library, framework, SDK, API, CLI, or cloud service using Context7 before writing or changing code. Use to close documentation gaps with verifiable information instead of relying on training memory. Trigger keywords - Context7, look up docs, library docs, API reference, SDK docs, framework docs, verify syntax, current API, check the docs, version-specific docs, documentation gap, how does this library work.
---

# Look Up Current Docs with Context7

Before you write, change, or debug code that touches an external library, framework, SDK, API, CLI, or cloud service, pull the current docs from Context7 and work from verified information instead of training memory that may be out of date. Context7 is an MCP server that returns current, version-specific documentation and code examples.

**Default to Context7 over recall and over generic web search for library and API docs** — even for well-known tools. Training data lags real releases; Context7 reflects the live docs.

## When to Use

- Before adding or changing code that calls an external library, SDK, API, CLI, or cloud service.
- Verifying current syntax, configuration keys, flags, or version-specific behavior.
- Library-specific debugging (a call that used to work now errors, or an option was deprecated).
- Setup, install, or CLI usage for a tool you are wiring in.
- Migration work, such as moving between major versions.

## When Not to Use

- Refactoring or writing a script from scratch where no external API is in question.
- Debugging your own business logic.
- Code review of pure application logic.
- General programming concepts unrelated to a specific library.

## How to Use

Two steps. Each tool caps at three calls per question, so pick the best result rather than looping.

1. **Resolve the library ID** (skip this step if you already have a `/org/project` or `/org/project/version` ID):
   - Call `resolve-library-id` with `libraryName` (the official name, properly punctuated, for example `Next.js`) and `query` (what you are trying to do, so results rank by relevance).
   - Choose the match with the best name fit, source reputation, snippet coverage, and benchmark score. Pin a version when you know it (`/org/project/version`).
2. **Query the docs**:
   - Call `query-docs` with `libraryId` (the ID from step 1, for example `/vercel/next.js`) and `query` (a specific question, not a keyword). Good: "How to register a Commander subcommand with options." Bad: "commander."

## Guardrail: Never Send Secrets

Context7 queries are sent to the Context7 API. Never include secrets, API keys, tokens, credentials, personal data, or proprietary source in `query` or `libraryName`. Describe the task generically and quote only public API surface.
