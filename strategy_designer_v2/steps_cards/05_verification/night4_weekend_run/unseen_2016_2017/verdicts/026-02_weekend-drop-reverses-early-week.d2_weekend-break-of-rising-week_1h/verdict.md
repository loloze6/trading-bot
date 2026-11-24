---
plan: 026-02_weekend-drop-reverses-early-week.d2_weekend-break-of-rising-week_1h
idea: 026-02_weekend-drop-reverses-early-week.d2_weekend-break-of-rising-week
fit: exact
status: not observable
---
Situation check: 98 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean short-side unusual 48-bar move per Sunday-close case: 0.00155998; t of the mean: 0.168431 (threshold: mean > 0 with t >= 2 confirms (with slope > 0); t <= -2 rejects; at least 100 cases)
- Supporting check: slope of short-side unusual move on |forecast|: -0.00165817, passed: False
- Counts: cases: 70
- Decided by: Only 70 cases across all coins and windows, fewer than the plan's minimum of 100.
- Reading: A case is every bar with forecast <= -2, at most one per 48-bar grid cell of its window, with its 48-bar return taken in bar positions inside the window; the drift is the coin's mean non-overlapping 48-bar return over all its windows; Sunday's last close is the bar starting Sunday 23:00 UTC; fewer than 100 cases is reported as not observable.
- Size: unusual move +0.16 % (t 0.12, the cases of one day together: 49 days) per case over 48 bars, -0.008 of the coin's usual move (13.44 %); normal drift in its direction -2.10 %, total -1.95 %; 70 cases
Plan: `steps_cards/03_test_plan/night4_weekend_run/plans/026-02_weekend-drop-reverses-early-week.d2_weekend-break-of-rising-week_1h.md`
Record: `steps_cards/04_backtest/night4_weekend_run/unseen_2016_2017/backtests/026-02_weekend-drop-reverses-early-week.d2_weekend-break-of-rising-week_1h`
Measure: `measure.py`
