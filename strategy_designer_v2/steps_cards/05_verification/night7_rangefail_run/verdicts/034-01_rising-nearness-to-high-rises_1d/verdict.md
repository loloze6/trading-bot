---
plan: 034-01_rising-nearness-to-high-rises_1d
idea: 034-01_rising-nearness-to-high-rises
fit: exact
status: inconclusive
---
Situation check: 95 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of drift-removed 5-day return on forecast (in-profile grid cases): 0.00179148; slope t (day-clustered): 1.63695 (threshold: slope t >= 2 (with positive supporting difference) confirms; t <= -2 rejects)
- Supporting check: mean drift-removed 5-day return, forecast > 0 minus forecast < 0: 0.00800968, passed: True
- Counts: independent in-profile grid cases: 2841, distinct days: 447
- Decided by: The slope's t lies between -2 and 2.
- Reading: Profile bars are those with regime 'unknown' (the config's only active regime, chop vetoed) and a non-missing forecast, all such grid bars enter the regression (forecast 0 included), the drift is the coin's mean 5-day return over all its non-overlapping grid bars, the slope's t uses day-clustered standard errors (CR1), and too few cases gives 'not observable'.
- Size: unusual move +1.31 % (t 3.34, the cases of one day together: 1083 days) per case over 5 bars, 0.104 of the coin's usual move (12.35 %); normal drift in its direction +0.24 %, total +1.55 %; 2376 cases
Plan: `steps_cards/03_test_plan/night7_rangefail_run/plans/034-01_rising-nearness-to-high-rises_1d.md`
Record: `steps_cards/04_backtest/night7_rangefail_run/backtests/034-01_rising-nearness-to-high-rises_1d`
Measure: `measure.py`
