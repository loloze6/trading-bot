---
plan: 031-02.b2_graded-deep-and-recent-fall_1d
idea: 031-02.b2_graded-deep-and-recent-fall
fit: adapted
status: not observable
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean excess 30-bar return (minus coin's normal 30-bar drift) on grid bars with forecast > 0: 0.000222316; t of the mean, cases of one day summed together: 0.00555516 (threshold: confirm: mean > 0 with t >= 2 and slope on forecast > 0; reject: mean < 0 with t <= -2; else inconclusive; fewer than 30 cases on distinct days: not enough)
- Supporting check: OLS slope of excess 30-bar return on forecast across cases: 0.0153885, passed: True
- Counts: cases: 52, cases on distinct days: 29
- Decided by: Fewer than 30 cases on distinct days (29), the plan's minimum count.
- Reading: Grid bars at positions 0, 30, 60, ... of each window with a full 30-bar forward return inside the window; normal drift is each coin's mean 30-bar return over all its windows' grid bars; t uses day-clustered deviations (summed per UTC day) with a D/(D-1) correction; the plan's 'fewer than 30 cases on distinct days' is applied as the minimum count giving 'not observable'.
- Size: unusual move +9.05 % (t 1.71, the cases of one day together: 70 days) per case over 30 bars, 0.223 of the coin's usual move (25.51 %); normal drift in its direction +5.03 %, total +14.08 %; 90 cases
Plan: `steps_cards/03_test_plan/night6_longreversal_run/plans/031-02.b2_graded-deep-and-recent-fall_1d.md`
Record: `steps_cards/04_backtest/night6_longreversal_run/backtests/031-02.b2_graded-deep-and-recent-fall_1d`
Measure: `measure.py`
