---
plan: 022-01_learned-combined-signal-score_1d
idea: 022-01_learned-combined-signal-score
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of forecast/10 x (5-day return - coin's mean 5-day return), non-overlapping grid: -0.00402298; t of the mean: -1.82511 (threshold: confirm: mean > 0 with t >= 2; reject: mean < 0 with t <= -2; otherwise inconclusive; at least 100 cases)
- Supporting check: none
- Counts: cases with a non-zero forecast: 3278
- Decided by: t = -1.83 lies between -2 and 2 over 3278 cases (inconclusive rule).
- Reading: Situation read as long when the raw composite score is positive and short when negative; grid positions 0, 5, 10, ... of each window with a full 5-bar return inside the window; the coin's mean 5-day return is the mean over all its windows' grid returns (all grid bars, active or not); the 100-case minimum is applied as 'not observable'.
- Size: unusual move -0.31 % per case over 5 bars, -0.026 of the coin's usual move (10.60 %); normal drift in its direction -0.03 %, total -0.34 %; 2637 cases
Plan: `steps_cards/03_test_plan/night3_learned_run/plans/022-01_learned-combined-signal-score_1d.md`
Record: `steps_cards/04_backtest/night3_learned_run/backtests/022-01_learned-combined-signal-score_1d`
Measure: `measure.py`
