---
plan: 031-01.b1.b2.b2.e2_short-rise-in-uptrend-continues_1d
idea: 031-01.b1.b2.b2.e2_short-rise-in-uptrend-continues
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of slope of excess 3-bar return on forecast, trending grid bars: 0.0013101; OLS slope t: 1.92233 (threshold: confirm if t >= 2 (with forecast-weighted mean excess > 0); reject if t <= -2)
- Supporting check: forecast-weighted mean excess 3-bar return: 0.0152955, passed: True
- Counts: grid bars in trending with forecast above 0: 163, grid bars in trending: 289
- Decided by: The slope's t is between -2 and 2.
- Reading: The 60-day return is recomputed from the window's closes where 60 prior bars exist and taken as regime 'trending' otherwise, the 5-day rise is the recorded rise5 raw value; the normal 3-bar drift is each coin's mean 3-bar return over the non-overlapping grid of all its windows and all regimes, the slope t is the OLS slope t pooled over all coins and windows, and the plan's 100-bar minimum is applied as 'not observable'.
- Size: unusual move -0.04 % (t -0.04, the cases of one day together: 87 days) per case over 3 bars, 0.023 of the coin's usual move (5.48 %); normal drift in its direction +0.14 %, total +0.10 %; 149 cases
Plan: `steps_cards/03_test_plan/night6_indecision_run/plans/031-01.b1.b2.b2.e2_short-rise-in-uptrend-continues_1d.md`
Record: `steps_cards/04_backtest/night6_indecision_run/unseen_2026/backtests/031-01.b1.b2.b2.e2_short-rise-in-uptrend-continues_1d`
Measure: `measure.py`
