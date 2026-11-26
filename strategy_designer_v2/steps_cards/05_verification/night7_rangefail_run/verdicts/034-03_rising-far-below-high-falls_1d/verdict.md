---
plan: 034-03_rising-far-below-high-falls_1d
idea: 034-03_rising-far-below-high-falls
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of excess 5-bar return on forecast (forecast < 0, non-overlapping grid, pooled): 0.000293879; OLS slope t: 0.63687 (threshold: slope > 0 with t >= 2 confirms (with supporting check); slope < 0 with t <= -2 rejects)
- Supporting check: mean excess 5-bar return on grid bars with forecast <= -10 is below 0: 0.00051957, passed: False
- Counts: grid cases with forecast below 0: 2350, grid cases with forecast -10 or below: 1174
- Decided by: The slope's t lies between -2 and 2 (inconclusive rule).
- Reading: Rising market read as the recorded regime not being 'chop' (the profile veto), the raw distance taken from last_history_value or recomputed from closes where missing; each coin's mean 5-bar return is taken on the non-overlapping grid of all its windows; the plan's 'inconclusive' for too few cases is reported as 'not observable' per the workflow's rule.
- Size: unusual move -0.33 % (t -0.74, the cases of one day together: 992 days) per case over 5 bars, -0.038 of the coin's usual move (12.35 %); normal drift in its direction -0.82 %, total -1.15 %; 2463 cases
Plan: `steps_cards/03_test_plan/night7_rangefail_run/plans/034-03_rising-far-below-high-falls_1d.md`
Record: `steps_cards/04_backtest/night7_rangefail_run/backtests/034-03_rising-far-below-high-falls_1d`
Measure: `measure.py`
