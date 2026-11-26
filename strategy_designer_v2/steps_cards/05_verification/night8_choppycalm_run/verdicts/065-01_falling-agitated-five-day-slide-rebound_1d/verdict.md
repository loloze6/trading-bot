---
plan: 065-01_falling-agitated-five-day-slide-rebound_1d
idea: 065-01_falling-agitated-five-day-slide-rebound
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of next-day excess return on slide5 forecast (day-clustered): 0.000628279; day-clustered OLS slope t: 1.8621 (threshold: confirm: slope > 0 with t >= 2 and weighted mean > 0; reject: slope < 0 with t <= -2)
- Supporting check: forecast-weighted mean next-day excess return: 0.00444065, passed: True
- Counts: cases: 3225, distinct days: 896
- Decided by: The slope t lies between -2 and 2.
- Reading: The profile is the bars whose recorded regime is 'unknown' (the detector's non-vetoed regime); the 5-day return is the recorded slide5 raw value, recomputed from closes where missing; cases are profile bars with forecast > 0 and a next bar in the window, regressed on post_pipeline_value with cluster-robust (by UTC day) standard errors; the plan's minimum counts (200 cases, 50 days) are applied as 'not observable'.
- Size: unusual move +0.58 % (t 1.97, the cases of one day together: 512 days) per case over 1 bars, 0.125 of the coin's usual move (5.33 %); normal drift in its direction +0.14 %, total +0.71 %; 1374 cases
Plan: `steps_cards/03_test_plan/night8_choppycalm_run/plans/065-01_falling-agitated-five-day-slide-rebound_1d.md`
Record: `steps_cards/04_backtest/night8_choppycalm_run/backtests/065-01_falling-agitated-five-day-slide-rebound_1d`
Measure: `measure.py`
