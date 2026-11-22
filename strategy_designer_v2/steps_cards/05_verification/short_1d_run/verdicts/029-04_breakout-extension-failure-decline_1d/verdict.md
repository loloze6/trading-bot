---
plan: 029-04_breakout-extension-failure-decline_1d
idea: 029-04_breakout-extension-failure-decline
fit: adapted
status: rejected
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean short-signed unusual 5-bar move of the short bets: -0.0019115; t of the mean: -0.441315 (threshold: confirm: > 0 with t >= 2 over at least 30 cases; reject: < 0 with t <= -2 over at least 30 cases)
- Supporting check: slope of raw 5-bar forward return on raw excursion among cases: 0.00221452, passed: False
- Counts: cases: 605, regression cases: 605
- Decided by: The excursion slope is positive with t >= 2.
- Reading: A case is the first short bet in each 5-bar grid cell of a window counted from its first row; the excursion regressor is the raw value on that bet bar; the drift is the coin's mean 5-bar return on the same non-overlapping grid over all its windows; the situation is the raw excursion > 0, recomputed from closes where the raw value is missing.
- Size: unusual move -0.19 % per case over 5 bars, -0.014 of the coin's usual move (10.60 %); normal drift in its direction -0.58 %, total -0.77 %; 605 cases
Plan: `steps_cards/03_test_plan/short_1d_run/plans/029-04_breakout-extension-failure-decline_1d.md`
Record: `steps_cards/04_backtest/short_1d_run/backtests/029-04_breakout-extension-failure-decline_1d`
Measure: `measure.py`
