# E-005 — Verify master on macOS and Linux

**State:** new
**Owner:** Dorian
**Updated:** 2026-08-03

## Why

Commit `c4feaf56` ported the research workflow to macOS by cherry-picking
(squashed) from Dorian's fork — interpreter resolution no longer hardcodes
Windows' path, Mac-only dependencies are declared, path/file-type guards were
added. This landed on master but has only been exercised on Windows since.
Nobody has run either test suite on macOS or Linux against current master to
confirm the port actually holds end to end.

## Done when

Both suites (`trading-bot/` and `strategy-research/`) run and pass on macOS
and on Linux, against commit `c4feaf56` or later, with the pass/fail counts
reported verbatim (matching or explaining any divergence from the Windows
baseline: 211 passed/2 skipped for `trading-bot/`, 472 passed/1 known failure
for `strategy-research/`).

## Stories

- [ ] S1 — Dorian runs both suites on macOS against current master, reports
      verbatim output.
- [ ] S2 — Run both suites on Linux (CI or a Linux box), report verbatim
      output.
- [ ] S3 — File any platform-specific failures found as their own bug cards
      or, if they need more than one dispatch, their own epics.

## Log

- 2026-08-03 — `new`. Written up in E-001 S4 (dispatch W24); seeded directly
  from `engineering/roadmap/EPICS.md`'s existing "Next step" note. Not
  started.
