---
plan: 067-01.b1.b1.b1_choppy-downside-stretch-keeps-falling_1d
idea: 067-01.b1.b1.b1_choppy-downside-stretch-keeps-falling
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of excess 5-bar return on forecast, forecast<0 grid cases: -0.000391604; slope t, clustered by day: -0.555412 (threshold: confirm: slope > 0 with t >= 2 and supporting check passes; reject: slope < 0 with t <= -2)
- Supporting check: mean excess 5-bar return on cases with forecast <= -10 is below 0: -0.0105992, passed: True
- Counts: grid cases with forecast < 0: 405, cases with forecast <= -10: 157, days of the cases: 228
- Decided by: Inconclusive: |t| < 2 for the slope.
- Reading: The choppy profile is the strategy's regime 'unknown'; the regression is OLS with an intercept and a cluster-robust (by UTC day, CR1 small-sample corrected) slope variance; the coin's mean 5-bar return is over all its non-overlapping grid returns in all windows; and the plan's minimum counts give 'not observable' as the workflow requires.
- Size: unusual move +0.60 % (t 1.50, the cases of one day together: 449 days) per case over 5 bars, 0.071 of the coin's usual move (10.60 %); normal drift in its direction -0.57 %, total +0.03 %; 605 cases
Plan: `steps_cards/03_test_plan/night9_chopstretch_run/plans/067-01.b1.b1.b1_choppy-downside-stretch-keeps-falling_1d.md`
Record: `steps_cards/04_backtest/night9_chopstretch_run/backtests/067-01.b1.b1.b1_choppy-downside-stretch-keeps-falling_1d`
Measure: `measure.py`
