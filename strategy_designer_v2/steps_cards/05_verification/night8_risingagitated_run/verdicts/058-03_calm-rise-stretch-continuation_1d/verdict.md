---
plan: 058-03_calm-rise-stretch-continuation_1d
idea: 058-03_calm-rise-stretch-continuation
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope t of demeaned 5-bar return on forecast, grid bars with forecast > 0: 0.00133421; OLS slope t, day-clustered: 1.48801 (threshold: confirm: slope > 0 with t >= 2; reject: slope < 0 with t <= -2; else inconclusive)
- Supporting check: none
- Counts: grid cases with forecast > 0: 428, distinct days: 188
- Decided by: The slope's t lies between -2 and 2.
- Reading: Cases on the same day were pooled across coins by a day-clustered standard error on the OLS slope; the coin's mean 5-bar return is over all its grid bars of all windows; the situation was regime 'unknown' with a positive raw ma_dist, long side.
- Size: unusual move +1.01 % (t 1.61, the cases of one day together: 338 days) per case over 5 bars, 0.093 of the coin's usual move (10.60 %); normal drift in its direction +0.63 %, total +1.64 %; 471 cases
Plan: `steps_cards/03_test_plan/night8_risingagitated_run/plans/058-03_calm-rise-stretch-continuation_1d.md`
Record: `steps_cards/04_backtest/night8_risingagitated_run/backtests/058-03_calm-rise-stretch-continuation_1d`
Measure: `measure.py`
