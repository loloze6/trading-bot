---
plan: 031-03.b1.b1.b2_up-streak-continuation-in-two-month-uptrend_1d
idea: 031-03.b1.b1.b2_up-streak-continuation-in-two-month-uptrend
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of forward 20-bar return minus the coin's mean 20-bar return on the forecast, trending-regime grid bars: -0.00358849; slope t, cases of one day clustered: -1.36245 (threshold: slope t >= 2 confirms (with mean unusual move > 0); slope t <= -2 rejects)
- Supporting check: mean unusual 20-bar move of the cases (forecast rises >= 2, one per grid cell): 0.0262195, passed: True
- Counts: grid cases in the regime with a forecast above 0: 305, distinct days: 73, trending grid bars in the slope: 545, supporting cases: 844
- Decided by: The slope t is between -2 and 2.
- Reading: Regime recomputed from prices as 30- and 60-bar close returns > 0 (recorded regime used on a window's first 60 bars), streak situation = raw streak value > 0, side long; the slope is an OLS with intercept on all trending grid bars (forecast 0 included) with day-clustered (CR1) standard errors; the coin's mean 20-bar return is over all its windows' grid; a case is a forecast rise of >= 2 from its lowest long level since the last bet (0 after flat), the first in each grid cell with a 20-bar forward return.
- Size: unusual move +2.62 % (t 1.64, the cases of one day together: 380 days) per case over 20 bars, 0.093 of the coin's usual move (23.14 %); normal drift in its direction +3.10 %, total +5.72 %; 844 cases
Plan: `steps_cards/03_test_plan/night6_streak_run/plans/031-03.b1.b1.b2_up-streak-continuation-in-two-month-uptrend_1d.md`
Record: `steps_cards/04_backtest/night6_streak_run/backtests/031-03.b1.b1.b2_up-streak-continuation-in-two-month-uptrend_1d`
Measure: `measure.py`
