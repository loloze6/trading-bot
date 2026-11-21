---
plan: 022-04_signal-weights-carry-forward_1d
idea: 022-04_signal-weights-carry-forward
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of (forecast/10) x (5-day return minus coin's normal 5-day drift), pooled: -0.00227641; t of the mean: -1.96667 (threshold: confirm: mean > 0 with t >= 2; reject: mean < 0 with t <= -2; at least 300 independent cases)
- Supporting check: none
- Counts: non-overlapping cases with a non-zero forecast: 3250
- Decided by: The t of the mean lies between -2 and 2 on at least 300 cases.
- Reading: Cases are the bars at positions 0, 5, 10, ... of each window with a full 5-bar return inside the window and a non-zero forecast; the normal drift is each coin's mean 5-day return over all its grid cells in all windows; the situation is the sign of the equal-weight mean of the components' standardised values, checked sign-consistent with their raw values.
- Size: unusual move -0.48 % per case over 5 bars, -0.048 of the coin's usual move (10.60 %); normal drift in its direction -0.03 %, total -0.51 %; 2802 cases
Plan: `steps_cards/03_test_plan/night3_learned_run/plans/022-04_signal-weights-carry-forward_1d.md`
Record: `steps_cards/04_backtest/night3_learned_run/backtests/022-04_signal-weights-carry-forward_1d`
Measure: `measure.py`
