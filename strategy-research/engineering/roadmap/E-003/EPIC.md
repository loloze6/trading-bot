# E-003 — Make the holdout seal gate enforceable in every clone

**State:** new
**Owner:** Jeremy
**Updated:** 2026-08-03

## Why

Verified this dispatch: `git config --get core.hooksPath` returns empty on
this clone. The active gate lives only at `.git/hooks/pre-commit` — a path
Git never tracks or clones — while the repo-tracked copy sits at
`strategy-research/tools/hooks/pre-commit`. Today the gate runs only because
someone manually copied that file into `.git/hooks/` on this machine. A fresh
clone (Dorian's fork, a new machine, CI) gets **no gate at all** and can
commit sealed-window market data with nobody stopping it — the exact failure
this whole gate exists to prevent.

## Done when

`git config core.hooksPath` is set to a repo-tracked directory (e.g.
`tools/hooks`, committed as part of the repo's own setup, not a local-only
copy), **and** a fresh clone of the repo — with no manual setup beyond
`git clone` — blocks a commit that introduces an unregistered sealed-window
date. Verify: clone the repo to a new directory, attempt a commit adding a
sealed-window date to a non-exempted file, confirm the gate fires without
having copied anything into `.git/hooks/` by hand.

## Stories

- [ ] S1 — Investigate whether `core.hooksPath` can point directly at
      `tools/hooks/` (multiple hooks, naming conventions, Windows/macOS/Linux
      path handling) or whether a thin dispatching hook is needed.
- [ ] S2 — Wire it up, document the one-time `git config` step (or a setup
      script that runs it) in `RUNBOOK.md`, verify on a fresh clone.

## Log

- 2026-08-03 — `new`. Identified and `core.hooksPath` gap verified during
  E-001 S4 (dispatch W24). Not started.
