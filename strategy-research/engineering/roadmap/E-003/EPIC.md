# E-003 — Make the holdout seal gate enforceable in every clone

**State:** new
**Owner:** Jeremy
**Updated:** 2026-08-03

**Provisional:** filed as an epic before S1 has run. S1 is investigation-only;
if it shows the fix is a single dispatch, this epic closes `withdrawn`
(amendment 7, `PROCESS.md`) and the work continues as the Bugs & Tasks card
noted below, not as an epic.

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

- [ ] S1 — **Investigation only. Write nothing.** Report: what `tools/hooks/`
      contains; whether `core.hooksPath` should point there (multiple hooks,
      naming conventions, Windows/macOS/Linux path handling); whether the
      live `pre-commit` hook has a tracked twin (compare by content hash, not
      filename); whether any installer writes `.git/hooks/`; whether CI
      exists.
- [ ] S2 — Wire it up, document the one-time `git config` step (or a setup
      script that runs it) in `RUNBOOK.md`, verify on a fresh clone.

## Duplicate tracking

A Bugs & Tasks card already exists for this same finding: "Holdout seal gate
is not enforced on merges, and not present in any clone but Jeremy's"
(Area: Security, Priority: High, Notion). Per amendment 6 (`PROCESS.md`),
that card is reduced to a pointer at this epic — not maintained as a parallel
record.

## Log

- 2026-08-03 — `new`. Identified and `core.hooksPath` gap verified during
  E-001 S4 (dispatch W24). Not started.
- 2026-08-03 — Marked provisional; S1 scoped as investigation-only (write
  nothing); duplicate Bugs & Tasks card noted for pointer reduction
  (dispatch W27).
