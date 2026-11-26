---
plan: 031-03.g1.b1.d2.e2_volume-swell-predicts-rise_1d
idea: 031-03.g1.b1.d2.e2_volume-swell-predicts-rise
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of forward 14-bar return minus normal 14-bar drift on the forecast, grid bars: 0.00170427; OLS t, standard errors clustered by day: 2.37878 (threshold: confirm: slope > 0 with t >= 2 (and timing gain > 0); reject: slope < 0 with t <= -2)
- Supporting check: timing gain (book mean daily return minus market-rise gain): 0.000433524, passed: True
- Counts: grid cases: 2448, distinct days: 207
- Decided by: Confirm: the slope is positive with t >= 2 and the timing gain is above 0.
- Reading: Slope is an OLS with intercept of (forward 14-bar return minus the coin's mean non-overlapping 14-bar return over all its windows) on the grid-bar forecast, all grid bars with a full 14-bar forward return included, t from day-clustered standard errors; the market-rise gain uses the position held from the previous day's close times the coin's mean daily close return; and the plan's 'fewer cases' rule is reported as 'not observable' per the workflow.
- Size: unusual move +0.66 % (t 1.02, the cases of one day together: 1056 days) per case over 14 bars, 0.026 of the coin's usual move (20.98 %); normal drift in its direction -0.19 %, total +0.47 %; 2274 cases
Plan: `steps_cards/03_test_plan/night6_longreversal_run/plans/031-03.g1.b1.d2.e2_volume-swell-predicts-rise_1d.md`
Record: `steps_cards/04_backtest/night6_longreversal_run/backtests/031-03.g1.b1.d2.e2_volume-swell-predicts-rise_1d`
Measure: `measure.py`
