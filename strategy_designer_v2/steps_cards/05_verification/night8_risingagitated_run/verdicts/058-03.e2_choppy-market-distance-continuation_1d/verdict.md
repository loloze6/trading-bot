---
plan: 058-03.e2_choppy-market-distance-continuation_1d
idea: 058-03.e2_choppy-market-distance-continuation
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of 10-bar excess forward return on forecast: 0.000620153; day-clustered t of slope: 0.719132 (threshold: confirm: slope > 0 with t >= 2; reject: slope < 0 with t <= -2; else inconclusive)
- Supporting check: none
- Counts: grid cases with a non-zero forecast: 408, days: 187
- Decided by: The slope's t lies between -2 and 2.
- Reading: Choppy profile read as regime 'unknown' (no trend veto); slope is OLS with intercept of excess return on forecast, t from day-clustered standard errors with G/(G-1) correction; drift is the mean of each coin's non-overlapping 10-bar grid returns over all its windows.
- Size: unusual move -0.03 % (t -0.06, the cases of one day together: 528 days) per case over 10 bars, -0.014 of the coin's usual move (14.49 %); normal drift in its direction +0.03 %, total -0.00 %; 713 cases
Plan: `steps_cards/03_test_plan/night8_risingagitated_run/plans/058-03.e2_choppy-market-distance-continuation_1d.md`
Record: `steps_cards/04_backtest/night8_risingagitated_run/backtests/058-03.e2_choppy-market-distance-continuation_1d`
Measure: `measure.py`
