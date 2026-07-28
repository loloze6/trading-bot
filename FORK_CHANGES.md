# Deliberate divergences from upstream (loloze6/trading-bot)

One line each — keeps the eventual merge with Jeremy a checklist, not archaeology.

**Reset 2026-07-28.** This file was emptied when the fork was returned to Jeremy's `70dab378`. The tree is currently **byte-identical to upstream**; there are zero divergences. Every line added below from here on is a deliberate, reviewed decision.

Pre-reset divergences are recorded in the archive tags (`git show archive/2026-07-28/mac-bootstrap`), not here — they are history, not current state.

## Current divergences

_(none yet)_

## Decisions deferred to the first sessions

- **`.claude/commands/`** — the fork's 4 slash commands (`/red-team`, `/new-hypothesis`, `/run-baseline`, `/sync-upstream`) are restored on disk but Jeremy's `.gitignore` excludes `.claude/`, so they are currently untracked and would be lost on a clone. Tracking them requires a `.gitignore` divergence. Dorian's call.
- **`CLAUDE.md`** — Jeremy's version has no `@CLAUDE.fork.md` include, so the fork's guardrails do not auto-load into an agent session. Two lines would fix it, and it is arguably the highest-value divergence available. Dorian's call.
- **`venv/`** — upstream tracks 449 files of a Windows venv. The Mac venv lives at `.venv/`. Untracking upstream's is a separate, PR-worthy change; not done.
