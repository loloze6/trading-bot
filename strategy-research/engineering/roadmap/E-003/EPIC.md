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

**2026-08-14, Dorian (Slack):** a second, independent local-only hook exists
on his machine — a secret-scanner (blocks committing API keys), living
*only* at his own untracked `.git/hooks/pre-commit`, with no tracked source
anywhere in the repo (its own header cites a non-existent
`scripts/pre-commit`). It has a real bug too: `grep -E` matches the bare
*name* `GEMINI_API_KEY` with no value present, so a diff that only removes a
line mentioning that env-var name gets blocked with nothing actually
secret in it. He supplied a tightened pattern (value-required, plus added
coverage for raw key formats: `AKIA...`, `AIza...`, PEM headers,
`api_secret=...`) and positive/negative-controlled it. He's offered to PR a
versioned copy into `tools/hooks/` alongside the holdout gate, so wiring
`core.hooksPath` for this epic hands a fresh clone **both** gates in one
shot instead of leaving the secret-scanner exactly as un-shared as the
holdout gate currently is. Offer accepted (Jérémy, 2026-08-14) — see
Stories.

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
- [ ] S3 — Dorian to PR his tightened secret-scan hook into `tools/hooks/`
      (versioned, value-required pattern — see Why for the exact bug it
      fixes), landing alongside S2 so `core.hooksPath` wiring covers both
      gates for every clone in one shot, not just the holdout gate.

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
- 2026-08-14 — Scope widened (still `new`, S1 not yet run): Dorian's
  secret-scan hook finding added to Why, S3 added to track his offered PR.
  Not a second epic — same root cause (`core.hooksPath` unwired everywhere
  but one machine), same fix shape, bundling is cheaper than splitting.
