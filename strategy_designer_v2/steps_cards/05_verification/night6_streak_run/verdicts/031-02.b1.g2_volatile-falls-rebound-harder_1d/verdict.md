---
plan: 031-02.b1.g2_volatile-falls-rebound-harder_1d
idea: 031-02.b1.g2_volatile-falls-rebound-harder
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled slope of excess 2-bar return on forecast (non-overlapping grid): 0.000243674; slope t, SE clustered by day: 1.47322 (threshold: confirm if slope t >= 2 with supporting difference > 0; reject if slope t <= -2)
- Supporting check: mean excess 2-bar return, high minus low 60-day volatility (per-coin median), forecast > 0: -0.000841169, passed: False
- Counts: grid points with a forecast above 0: 4217, distinct days of those grid points: 1125, grid points in regression: 8650, distinct days in regression: 1509
- Decided by: The slope's t lies between -2 and 2.
- Reading: Grid points are rows 0, 2, 4, ... of each window with the 2-bar return inside the window, the coin's mean is over all its grid points of all windows, the slope SE is the day-clustered sandwich without small-sample correction, the fall % for the volatility is the bar's own close-to-close fall from the previous close in the same window (points without it left out), the split puts volatility above the coin's median in the high group and at or below it in the low group, and the plan's minimum counts give 'not observable' as the workflow requires.
- Size: unusual move +0.09 % (t 0.53, the cases of one day together: 1681 days) per case over 2 bars, 0.014 of the coin's usual move (6.58 %); normal drift in its direction +0.24 %, total +0.32 %; 5357 cases
Plan: `steps_cards/03_test_plan/night6_streak_run/plans/031-02.b1.g2_volatile-falls-rebound-harder_1d.md`
Record: `steps_cards/04_backtest/night6_streak_run/backtests/031-02.b1.g2_volatile-falls-rebound-harder_1d`
Measure: `measure.py`
