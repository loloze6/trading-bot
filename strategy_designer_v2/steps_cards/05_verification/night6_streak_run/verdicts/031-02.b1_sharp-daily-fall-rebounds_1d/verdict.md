---
plan: 031-02.b1_sharp-daily-fall-rebounds_1d
idea: 031-02.b1_sharp-daily-fall-rebounds
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of excess 2-day return on forecast (forecast > 0, non-overlapping grid): 0.000614936; OLS slope t, day-clustered (CR1): 2.27923 (threshold: slope t >= 2 confirms (with positive mean excess), t <= -2 rejects; day-clustered t)
- Supporting check: mean excess 2-day return on grid bars with forecast > 0 is above 0: 0.000729764, passed: True
- Counts: grid bars with forecast above 0: 4217, distinct days: 1125
- Decided by: The slope's t is 2 or more and the mean excess 2-day return is positive.
- Reading: Grid at positions 0,2,4,... of each window with a full 2-bar return inside it; normal drift = coin's mean 2-day return over all its grid bars in all windows; regression with intercept, slope t from day-clustered (UTC date of the bar) CR1 standard errors; the plan's 'fewer is inconclusive' minimum is reported as 'not observable' per the workflow rule.
- Size: unusual move +0.15 % (t 0.87, the cases of one day together: 1621 days) per case over 2 bars, 0.022 of the coin's usual move (6.58 %); normal drift in its direction +0.24 %, total +0.38 %; 5179 cases
Plan: `steps_cards/03_test_plan/night6_streak_run/plans/031-02.b1_sharp-daily-fall-rebounds_1d.md`
Record: `steps_cards/04_backtest/night6_streak_run/backtests/031-02.b1_sharp-daily-fall-rebounds_1d`
Measure: `measure.py`
