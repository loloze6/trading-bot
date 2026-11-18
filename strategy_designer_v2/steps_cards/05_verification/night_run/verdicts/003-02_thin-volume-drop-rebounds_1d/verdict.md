---
plan: 003-02_thin-volume-drop-rebounds_1d
idea: 003-02_thin-volume-drop-rebounds
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of forecast/10 x excess 5-bar return, non-overlapping grid, forecast > 0, pooled: -0.00353709; t of the mean: -1.90802 (threshold: t >= 2 to confirm (with check difference > 0), t <= -2 to reject)
- Supporting check: mean excess 5-bar return above minus below the median positive forecast: -0.000843814, passed: False
- Counts: grid cases with forecast > 0: 1067
- Decided by: The main measure's t lies between -2 and 2.
- Reading: The coin's mean 5-bar return is taken over the same non-overlapping grid (positions 0, 5, 10, ... of each window, with t+5 inside the window) across all its windows; the supporting check compares cases strictly above and strictly below the median positive forecast, ties left out; fewer than 30 cases gives 'not observable'.
Plan: `steps_cards/03_test_plan/night_run/plans/003-02_thin-volume-drop-rebounds_1d.md`
Record: `steps_cards/04_backtest/night_run/backtests/003-02_thin-volume-drop-rebounds_1d`
Measure: `measure.py`
