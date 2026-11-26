---
plan: 031-01.b1.b2.b2.e2_short-rise-in-uptrend-continues_1d
idea: 031-01.b1.b2.b2.e2_short-rise-in-uptrend-continues
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of slope of excess 3-bar return on forecast, trending grid bars: 0.000861343; OLS slope t: 3.73039 (threshold: confirm if t >= 2 (with forecast-weighted mean excess > 0); reject if t <= -2)
- Supporting check: forecast-weighted mean excess 3-bar return: 0.0089458, passed: True
- Counts: grid bars in trending with forecast above 0: 1651, grid bars in trending: 2864
- Decided by: The slope's t is 2 or more and the forecast-weighted mean excess return is above 0.
- Reading: The 60-day return is recomputed from the window's closes where 60 prior bars exist and taken as regime 'trending' otherwise, the 5-day rise is the recorded rise5 raw value; the normal 3-bar drift is each coin's mean 3-bar return over the non-overlapping grid of all its windows and all regimes, the slope t is the OLS slope t pooled over all coins and windows, and the plan's 100-bar minimum is applied as 'not observable'.
- Size: unusual move +0.08 % (t 0.28, the cases of one day together: 843 days) per case over 3 bars, 0.011 of the coin's usual move (7.96 %); normal drift in its direction +0.36 %, total +0.44 %; 1577 cases
Plan: `steps_cards/03_test_plan/night6_indecision_run/plans/031-01.b1.b2.b2.e2_short-rise-in-uptrend-continues_1d.md`
Record: `steps_cards/04_backtest/night6_indecision_run/backtests/031-01.b1.b2.b2.e2_short-rise-in-uptrend-continues_1d`
Measure: `measure.py`
