---
plan: 033-03.b1_upper-range-drifts-higher_1d
idea: 033-03.b1_upper-range-drifts-higher
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled slope t of 10-bar excess return on forecast (day-clustered): 0.00128057; day-clustered slope t: 1.53497 (threshold: t >= 2 confirms (with check difference > 0); t <= -2 rejects; otherwise inconclusive)
- Supporting check: mean excess return when above_high > 0 minus mean excess return when forecast < 0: 0.0683324, passed: True
- Counts: grid cases in total: 1691, cases above the 20-day high: 108, grid cases with forecast below 0: 880, days (clusters): 304
- Decided by: The slope's t is between -2 and 2.
- Reading: Expected side taken as long when above_high > 0, else the sign of the raw range position; the slope is OLS with intercept of excess return on forecast, its t day-clustered (CR1); the drift is each coin's mean grid 10-bar return over all its windows; the minimum counts the plan lists under inconclusive are applied as 'not observable'.
- Size: unusual move +0.59 % (t 1.02, the cases of one day together: 832 days) per case over 10 bars, 0.024 of the coin's usual move (14.49 %); normal drift in its direction -0.01 %, total +0.57 %; 1588 cases
Plan: `steps_cards/03_test_plan/night7_rangefail_run/plans/033-03.b1_upper-range-drifts-higher_1d.md`
Record: `steps_cards/04_backtest/night7_rangefail_run/backtests/033-03.b1_upper-range-drifts-higher_1d`
Measure: `measure.py`
