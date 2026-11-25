---
plan: 046-01_calm-scaled-rise-second-day-continues_1d
idea: 046-01_calm-scaled-rise-second-day-continues
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: clustered-by-day t of the slope of excess next-bar return on the forecast, forecast > 0 bars: 0.000205239; slope t, day-clustered: 1.88055 (threshold: confirm if t >= 2 and forecast-weighted mean excess return > 0; reject if t <= -2)
- Supporting check: forecast-weighted mean excess next-bar return > 0: 0.0013348, passed: True
- Counts: bars with a forecast above 0: 4720, distinct days: 1642
- Decided by: Inconclusive: the slope's t lies between -2 and 2.
- Reading: Calm is read from the recorded regime ('unknown', i.e. not vetoed to 'chop') and the rise from last_history_value > 0; the slope's t uses an OLS with intercept and standard errors clustered by UTC calendar day (scores summed per day, small-sample corrected); the coin's mean daily return is the mean of all its within-window one-bar returns; the minimum counts are on bars with a forecast above 0 and a next-bar return inside the window, and a shortfall is reported as 'not observable'.
- Size: unusual move -0.03 % (t -0.24, the cases of one day together: 1281 days) per case over 1 bars, -0.004 of the coin's usual move (4.73 %); normal drift in its direction +0.13 %, total +0.10 %; 3133 cases
Plan: `steps_cards/03_test_plan/night7_chopreversal_run/plans/046-01_calm-scaled-rise-second-day-continues_1d.md`
Record: `steps_cards/04_backtest/night7_chopreversal_run/backtests/046-01_calm-scaled-rise-second-day-continues_1d`
Measure: `measure.py`
