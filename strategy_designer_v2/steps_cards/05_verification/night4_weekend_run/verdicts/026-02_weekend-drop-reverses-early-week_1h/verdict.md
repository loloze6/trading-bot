---
plan: 026-02_weekend-drop-reverses-early-week_1h
idea: 026-02_weekend-drop-reverses-early-week
fit: adapted
status: rejected
---
Situation check: 99 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean over weeks of the cross-coin average unusual 48-bar move after a weekend-loss signal: -0.00843489; t of the mean over weeks: -2.18275 (threshold: confirm: mean > 0 with t >= 2 and slope > 0; reject: mean < 0 with t <= -2)
- Supporting check: slope of unusual move on signal-bar forecast: 0.000637659, passed: True
- Counts: weeks that hold a case: 312, cases: 1106
- Decided by: The mean unusual move is negative with t <= -2.
- Reading: The signal bar is the bar whose close (timestamp + 1h) is Monday 00:00 UTC and the situation is a negative 48-bar raw return on it; a week is identified by that Monday's date; drift is the coin's mean 48-bar return on a non-overlapping grid from each window's first row; fewer than 100 weeks with a case is treated as the minimum count not reached (not observable).
- Size: unusual move -0.50 % per case over 48 bars, -0.070 of the coin's usual move (6.56 %); normal drift in its direction +0.28 %, total -0.22 %; 935 cases
Plan: `steps_cards/03_test_plan/night4_weekend_run/plans/026-02_weekend-drop-reverses-early-week_1h.md`
Record: `steps_cards/04_backtest/night4_weekend_run/backtests/026-02_weekend-drop-reverses-early-week_1h`
Measure: `measure.py`
