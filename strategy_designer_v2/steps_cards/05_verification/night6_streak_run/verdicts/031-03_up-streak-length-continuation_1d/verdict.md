---
plan: 031-03_up-streak-length-continuation_1d
idea: 031-03_up-streak-length-continuation
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of 5-bar forward excess return on forecast (non-overlapping grid): 0.000488953; OLS slope t, clustered by day: 1.42674 (threshold: confirm: slope > 0 with t >= 2 and supporting check passes; reject: slope < 0 with t <= -2; else inconclusive)
- Supporting check: mean excess 5-bar return, top third of positive forecasts minus forecast 0: 0.0112093, passed: True
- Counts: grid bars with a positive forecast: 1612, distinct days of grid bars with a positive forecast: 456, grid bars in the sample: 3326, distinct days in the sample: 617
- Decided by: |t| < 2, which the plan rules inconclusive
- Reading: excess return = 5-bar return minus the coin's mean 5-bar return on the non-overlapping grid of all its windows; slope from OLS with intercept and CR1 standard error clustered by UTC day; top third = positive-forecast grid bars at or above their 2/3 quantile; the plan's minimum counts, when not reached, give 'not observable'.
- Size: unusual move -0.29 % (t -0.97, the cases of one day together: 1188 days) per case over 5 bars, -0.032 of the coin's usual move (10.60 %); normal drift in its direction +0.66 %, total +0.37 %; 3153 cases
Plan: `steps_cards/03_test_plan/night6_streak_run/plans/031-03_up-streak-length-continuation_1d.md`
Record: `steps_cards/04_backtest/night6_streak_run/backtests/031-03_up-streak-length-continuation_1d`
Measure: `measure.py`
