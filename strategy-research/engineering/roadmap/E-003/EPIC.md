# E-003 — Make the holdout seal gate enforceable in every clone

**State:** planned
**Owner:** Jeremy
**Updated:** 2026-08-18

**No longer provisional.** S1 ran 2026-08-18: the fix is NOT a single
dispatch (a real design decision blocks S2, see below), so this stays an
epic per amendment 7 rather than closing `withdrawn`.

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

- [x] S1 — **Investigation only. Write nothing.** Done 2026-08-18 (see Log)
      — conclusion: this is NOT a single dispatch, epic stays active, does
      NOT close `withdrawn`.
- [ ] S2 — Wire it up. Blocked on the prose-accrual design decision found by
      S1 (see Log) — CANNOT be "wire core.hooksPath + add a CI step" as
      originally scoped without also deciding how the gate treats narrative
      files that legitimately and repeatedly mention the sealed window
      (the ledger itself, `FORK_CHANGES.md`, `CLAUDE.fork.md`). Wiring it
      as a hard blocking gate today would redden CI on the very next commit
      to any of those files.
- [x] S3 — Dorian's tightened secret-scan hook. Landed 2026-08-15 (PR #26,
      `strategy-research/tools/hooks/pre-commit` Gate 0) — done independently
      of S2, no longer blocked on it.

## Design decision needed before S2 (found 2026-08-18)

Running `strategy-research/tools/holdout_date_gate.sh` against the current
tree (exactly what a CI step or a wired local hook would do) blocks TODAY,
on ordinary, harmless prose — not a false alarm, an actual measured gap in
the exemption model:

```
COMMIT BLOCKED — 7 file(s) carry dates inside the sealed holdout window.
  .gitignore                                   4 lines, EXCEEDS registered 3
  CLAUDE.fork.md                                1 line,  NOT REGISTERED
  FORK_CHANGES.md                               5 lines, NOT REGISTERED
  research/ledger/win.md                       10 lines, NOT REGISTERED
  trading-bot/tests/test_capture_krakenfutures_funding.py   1 line, NOT REGISTERED
  trading-bot/tests/test_model_funding_bit_identical.py     2 lines, NOT REGISTERED
  trading-bot/tests/test_no_sealed_date_literals.py        25 lines, EXCEEDS registered 9
```

This is the exact "prose-accrual" problem the 2026-08-08 ledger entry
already named as Branch 2's blocker (measured then: 3 files, registry
exempted 157/160) — now measured again at 7 files. It has grown, not
shrunk, and `research/ledger/win.md` is the clearest case why: every
session that appends a dated entry mentioning the holdout window (which is
this ledger's entire purpose) adds to a line-count exemption that then
needs bumping by hand, forever, or the very next ledger commit trips the
gate. A registry keyed on "exactly N lines, no more" is fundamentally the
wrong shape for a file whose job is to keep growing narrative mentions of
the seal.

Two real options, not decided here:
- **(A) Path-exempt known narrative files entirely** (ledger files,
  `FORK_CHANGES.md`, `CLAUDE.fork.md`) rather than capping their line
  count — matches how they're actually used, but weakens the deny-by-
  default property for exactly the files most likely to genuinely
  reference real dates in prose form, so it needs a human call, not an
  agent's.
- **(B) Keep the count-capped model, bump the registry to match current
  reality now**, and accept this as a recurring per-commit maintenance
  tax on ledger writers — safe today, but the same 2026-08-08 entry
  already predicted this leads to `--no-verify` becoming normal, which
  its own docstring calls worse than no gate.

Not implementing either without Jeremy's call — the wrong choice breaks CI
for both him and Dorian on the very next ordinary ledger commit.

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
- 2026-08-15 — S3 landed (PR #26): `strategy-research/tools/hooks/pre-commit`
  now carries both gates (secret-scan Gate 0 + holdout gate Gate 1 + test
  suite Gate 2), tracked and versioned. Confirms the tracked hook itself is
  current and correct — the gap is purely that nothing installs it
  automatically (`.git/hooks/pre-commit` still doesn't exist on a fresh
  clone; `core.hooksPath` still unset) and CI (`.github/workflows/tests.yml`)
  runs the fast test suites only, never either gate — so a PR merged
  through GitHub's UI is checked by neither gate regardless of any local
  config, which is the more fundamental version of "not enforced on merges"
  than the original framing.
- 2026-08-18 — S1 run for real (Jeremy, prompted by the Notion bug card
  needing a real next step). Findings: `core.hooksPath` unset on a fresh
  clone (verified), no CI enforcement of either gate (verified by reading
  `.github/workflows/tests.yml`), and — the part that changes the plan —
  actually running `holdout_date_gate.sh` against the live tree blocks
  today on 7 files of ordinary prose (`.gitignore`, `CLAUDE.fork.md`,
  `FORK_CHANGES.md`, `research/ledger/win.md`, three test files), not a
  hypothetical. This is the same prose-accrual problem the 2026-08-08
  ledger entry flagged (then 3 files, registry exempted 157/160) — grown,
  not resolved. Wiring this into CI or a real local hook today would
  redden the build on the next ordinary commit to the ledger. **Conclusion:
  not a single dispatch — stays an epic, S2 blocked on a design decision
  (two options recorded above), routed to Jeremy rather than picked
  unilaterally given the blast radius (breaks CI for both Jeremy and
  Dorian if wrong).** Also found and NOT fixed here, flagged only:
  `strategy-research/tools/hooks/pre-commit`'s test-suite gate hardcodes
  `venv/Scripts/python` (Windows-only path) — silently no-ops rather than
  running tests on Linux/macOS (the command-not-found exit code 127 falls
  through the hook's explicit 1/2/3 check and prints "Tests passed"),
  which matters for the epic's own "every clone" promise but is a separate,
  smaller bug from the prose-accrual blocker.
