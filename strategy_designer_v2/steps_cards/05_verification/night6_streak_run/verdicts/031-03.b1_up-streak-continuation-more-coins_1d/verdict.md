---
plan: 031-03.b1_up-streak-continuation-more-coins_1d
idea: 031-03.b1_up-streak-continuation-more-coins
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of demeaned 5-bar forward return on forecast (non-overlapping grid): 0.000184432; slope t, cases of one day pooled (day-clustered): 0.538864 (threshold: confirm if t ≥ +2 (with the supporting check), reject if t ≤ −2, else inconclusive)
- Supporting check: mean unusual 5-bar move over bets on the grid, long direction: -0.00269177, passed: False
- Counts: grid bars with forecast > 0: 3035, distinct days of grid bars with forecast > 0: 478, grid bars in regression: 6157, cases (bets on the 5-bar grid): 5838, days in regression (clusters): 617
- Decided by: The slope's t is between −2 and +2, which the plan calls inconclusive.
- Reading: The regression uses every grid bar with a 5-bar forward return (forecast 0 included), demeaned by the coin's mean grid 5-bar return over all its windows, with the slope's t from standard errors clustered by day (residual deviations summed per day); the supporting check's cases are the first forecast rise of at least 2 points in each 5-bar grid cell, and the plan's 'else inconclusive' for too few cases is reported as 'not observable' as the workflow requires.
- Size: unusual move -0.27 % (t -0.87, the cases of one day together: 1362 days) per case over 5 bars, -0.028 of the coin's usual move (11.58 %); normal drift in its direction +0.74 %, total +0.47 %; 5838 cases
Plan: `steps_cards/03_test_plan/night6_streak_run/plans/031-03.b1_up-streak-continuation-more-coins_1d.md`
Record: `steps_cards/04_backtest/night6_streak_run/backtests/031-03.b1_up-streak-continuation-more-coins_1d`
Measure: `measure.py`
