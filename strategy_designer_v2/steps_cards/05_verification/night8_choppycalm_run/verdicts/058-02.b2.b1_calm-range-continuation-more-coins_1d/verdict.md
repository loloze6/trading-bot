---
plan: 058-02.b2.b1_calm-range-continuation-more-coins_1d
idea: 058-02.b2.b1_calm-range-continuation-more-coins
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of excess 5-bar forward return on forecast (non-overlapping grid, nonzero forecast): 0.000394405; slope t (day-clustered): 0.874992 (threshold: confirm: slope > 0 with t >= 2; reject: slope < 0 with t <= -2; else inconclusive)
- Supporting check: none
- Counts: grid cases with a nonzero forecast: 1050, distinct days: 322
- Decided by: Inconclusive rule: the slope's t lies between -2 and 2.
- Reading: The situation is the bars whose regime is 'unknown' (the choppy calm profile) and the side is the sign of the recorded range position (rebuilt from the 20-bar high/low where not recorded); the coin's mean 5-bar return is taken over all grid bars of all its windows; the slope is OLS of excess return on forecast with a day-clustered standard error (per-day sums of x-deviation times residual, with the G/(G-1) correction); the plan's minimum of 100 cases over 50 days is applied as 'not observable'.
- Size: unusual move +0.71 % (t 2.12, the cases of one day together: 827 days) per case over 5 bars, 0.064 of the coin's usual move (11.68 %); normal drift in its direction +0.03 %, total +0.74 %; 1536 cases
Plan: `steps_cards/03_test_plan/night8_choppycalm_run/plans/058-02.b2.b1_calm-range-continuation-more-coins_1d.md`
Record: `steps_cards/04_backtest/night8_choppycalm_run/backtests/058-02.b2.b1_calm-range-continuation-more-coins_1d`
Measure: `measure.py`
