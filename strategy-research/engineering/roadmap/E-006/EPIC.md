# E-006 — Stop shipping a committed Windows venv

**State:** new
**Owner:** Jeremy (coordinate with Dorian before executing)
**Updated:** 2026-08-03

## Why

Verified this dispatch: `git ls-files | grep -c "^venv/"` returns **449** —
a Windows Python virtualenv is tracked in git, and `venv/` is not in
`.gitignore` (`git check-ignore venv/` exits 1, not ignored). This is
platform-specific binary bloat committed to a repo two people now work from
different OSes (E-005) — a Windows venv is actively wrong on Dorian's macOS
checkout and on Linux CI, and every commit that touches it (or fails to,
while its files drift from `pip freeze`) is noise in every diff.

## Done when

`git ls-files | grep -c "^venv/"` returns **0**, `.gitignore` excludes
`venv/`, and dependency reproduction goes through a committed
`requirements.txt` (or equivalent) instead — verified by creating a fresh
venv from that file and running both suites against it.

## Stories

- [ ] S1 — Agree with Dorian on the replacement (requirements.txt / lockfile)
      before removing anything — a committed venv may be the only thing
      currently pinning versions for someone.
- [ ] S2 — `git rm -r --cached venv/`, add `.gitignore` entry, commit
      `requirements.txt`, verify both suites still pass from a freshly
      created venv on at least Windows (and macOS/Linux once E-005 gives a
      way to check).

## Log

- 2026-08-03 — `new`. Tracked-file count and gitignore status verified
  directly during E-001 S4 (dispatch W24). Not started; explicitly gated on
  agreement with Dorian first, per `engineering/roadmap/EPICS.md`'s
  existing next-step note.
