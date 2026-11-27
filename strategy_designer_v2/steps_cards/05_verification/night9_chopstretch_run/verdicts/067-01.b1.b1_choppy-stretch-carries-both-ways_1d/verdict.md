---
plan: 067-01.b1.b1_choppy-stretch-carries-both-ways_1d
idea: 067-01.b1.b1_choppy-stretch-carries-both-ways
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled slope of 5-bar excess return on forecast: 0.000353043; slope t, clustered by day: 0.910955 (threshold: slope t >= 2 (with both sides carrying) confirms; slope t <= -2 rejects)
- Supporting check: both sides carry (long mean excess > 0, short mean excess < 0): -0.00532488, passed: False
- Counts: grid cases: 819, long cases: 414, short cases: 405, days: 374
- Decided by: The slope t lies between -2 and 2.
- Reading: The 60-day return (percent, close[t]/close[t-60]-1) is recomputed from the prices inside each window, so active bars in a window's first 60 rows are left out of the situation check, and the choppy band is taken as inclusive of +-10 % like the config's strict vetoes; the expected side is the sign of the raw stretch; drift is the coin's mean 5-bar return on the non-overlapping grid of all its windows; the regressor is the stretch post_pipeline_value (forecast where missing), OLS with intercept, slope t with standard errors clustered by UTC day (CR1); the supporting check uses the signs of the side means only; the plan's minimum counts, though listed as inconclusive, give 'not observable' as the workflow requires.
- Size: unusual move +0.24 % (t 0.78, the cases of one day together: 807 days) per case over 5 bars, 0.018 of the coin's usual move (10.60 %); normal drift in its direction -0.01 %, total +0.23 %; 1112 cases
Plan: `steps_cards/03_test_plan/night9_chopstretch_run/plans/067-01.b1.b1_choppy-stretch-carries-both-ways_1d.md`
Record: `steps_cards/04_backtest/night9_chopstretch_run/backtests/067-01.b1.b1_choppy-stretch-carries-both-ways_1d`
Measure: `measure.py`
