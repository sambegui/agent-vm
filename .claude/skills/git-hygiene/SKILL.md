---
name: git-hygiene
description: Commit confirmed changes early and often so Git acts as a cheap undo stack during development, then squash into clean, repo-compliant commits before publishing. Use to checkpoint work during test-driven development, recover from a bad change, or decide when and how to commit. Trigger keywords - git hygiene, commit, checkpoint, commit often, undo change, revert, git reset, git stash, git restore, WIP commit, squash before PR, when to commit.
---

# Commit Hygiene: Checkpoint Often, Publish Clean

Treat Git as your undo stack. Commit early and often once a change is confirmed working, so a bad next step is a cheap reset rather than redone work. Leaning on commits as checkpoints saves time, effort, and tokens when changes must be undone.

## Two Tiers of Commits

Keep local safety separate from what you publish.

- **Working checkpoints** — frequent, small, local commits made as soon as a change is verified (a test goes green, a step is confirmed). These are your undo net. Keep them tight and labeled so you can find the one to return to.
- **Publishable commits** — what ends up on a pushed branch or in a PR. Make these follow the repo's commit conventions and any sign-off, verification, or hook requirements. Squash or rebase your working checkpoints into clean, compliant commits before pushing.

Do not push a string of raw WIP checkpoints to a published branch. Clean the history first.

## Checkpoint Rhythm (the TDD Fallback)

1. Make the smallest change that moves you forward.
2. Confirm it by running the narrowest test or verification that covers it.
3. Commit the confirmed change before starting the next step or a refactor.
4. If the next step goes wrong, return to the last good checkpoint instead of untangling it by hand.

This pairs naturally with test-driven development: commit on green, then refactor against a known-good point.

## Undo and Recover

- Discard unstaged edits to a file: `git restore <path>`
- Unstage without losing work: `git restore --staged <path>`
- Keep changes but undo the last commit: `git reset --soft HEAD~1`
- Discard everything back to the last commit: `git reset --hard HEAD`
- Set work aside: `git stash` (restore with `git stash pop`)
- Recover a commit you thought you lost: `git reflog`

## Guardrails

- **Branch first.** Avoid committing directly to a default or protected branch; create a feature branch.
- **Never commit secrets**, API keys, credentials, or `.env` files. If one slips into a checkpoint, remove it before publishing rather than only deleting it in a later commit.
- **Let hooks verify by default.** If the repo runs pre-commit, commit-msg, or pre-push hooks, let them run. If you make a throwaway WIP checkpoint with `--no-verify`, re-run the full gate before publishing.
- **Watch for auto-staged files.** Some hooks restage generated files; unstage anything you did not intend before committing.
