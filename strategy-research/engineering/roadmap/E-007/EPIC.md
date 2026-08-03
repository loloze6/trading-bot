# E-007 — Recorder storage and host migration

**State:** parked
**Owner:** Jeremy
**Updated:** 2026-08-03

## Why

The forward recorder (`recorder/`) was built and run, then stopped on two
findings from ledger items R3/R3a (`engineering/sessions_archive/HANDOFF_20260724.md`):
**R3** — measured 12-month storage projection is 360GB compressed vs. a 64GB
spec estimate (5.63×) against a pre-registered 100GB budget; the miss is
decomposed and measured (book message rate, bytes/frame, compression ratio),
not guessed, but the 100GB budget still needs an operator decision (scope
down, raise the budget, or migrate host). **R3a** — separately, the recording
host had 0.18GB free on C: at measurement time, an unrelated pre-existing
condition, not caused by the recorder (which wrote 59MB total). The recorder
cannot restart, at any scope, until disk is freed.

**S2-audit finding (this dispatch):** the R3a disk crisis no longer holds as
measured — `df -h` on this machine now shows 8.7GB free on the same drive.
Whether that was a deliberate fix or incidental drift, and whether the
recorder was ever restarted, is **unverified** — nothing in the repo records
either.

## Done when

An operator decision on the R3 storage budget is recorded in writing (reduce
scope / raise the 100GB budget / migrate to a host with more capacity), **and**
the recorder's current running state (running, deliberately stopped, or
restarted) is confirmed and matches that decision. Verify: `recorder/`'s own
liveness/coverage tooling (`recorder/coverage_report.py`,
`recorder/liveness.py`) reports a state consistent with the recorded decision.

## Stories

- [ ] S1 — Confirm current disk state and whether the recorder is running;
      reconcile against R3a's stale 0.18GB figure.
- [ ] S2 — Operator decision on the R3 storage budget; record it here with
      reasoning.
- [ ] S3 — Execute the decision (scope reduction, budget change, or host
      migration) and restart/confirm the recorder under it.

## Log

- 2026-08-03 — `new` → `parked`. Written up in E-001 S4 (dispatch W24) from
  HANDOFF ledger items R3/R3a. Unblock condition: an operator decision on the
  storage budget (S2), which this epic cannot make for itself.
