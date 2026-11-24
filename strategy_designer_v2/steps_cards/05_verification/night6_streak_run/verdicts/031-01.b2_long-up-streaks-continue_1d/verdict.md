---
plan: 031-01.b2_long-up-streaks-continue_1d
idea: 031-01.b2_long-up-streaks-continue
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of 3-bar forward return minus coin's normal drift on forecast, pooled non-overlapping grid: 3.24514e-05; OLS slope t: 0.238891 (threshold: confirm: slope > 0 with t >= 2 and check passes; reject: slope < 0 with t <= -2; else inconclusive; at least 300 grid bars with forecast > 0)
- Supporting check: mean 3-bar return minus normal drift on grid bars with forecast >= 10, above 0: -5.45596e-05, passed: False
- Counts: grid bars with forecast > 0: 2931, grid bars (all, in the regression): 5566, grid bars with forecast >= 10: 2306
- Decided by: The slope has |t| < 2.
- Reading: The slope is an ordinary least-squares regression with intercept of the excess return on the forecast over all pooled grid bars (forecast 0 included), the normal drift is each coin's mean 3-bar grid return over all its windows, a supporting check with no grid bar at forecast >= 10 counts as failed, and the plan's minimum of 300 yields 'not observable' as the workflow requires.
- Size: unusual move -0.29 % (t -1.51, the cases of one day together: 1547 days) per case over 3 bars, -0.038 of the coin's usual move (7.96 %); normal drift in its direction +0.39 %, total +0.10 %; 4610 cases
Plan: `steps_cards/03_test_plan/night6_streak_run/plans/031-01.b2_long-up-streaks-continue_1d.md`
Record: `steps_cards/04_backtest/night6_streak_run/backtests/031-01.b2_long-up-streaks-continue_1d`
Measure: `measure.py`
