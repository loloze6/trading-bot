---
plan: 072-04.b1_choppy-deep-close-ten-day-fall_1d
idea: 072-04.b1_choppy-deep-close-ten-day-fall
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of drift-removed 10-bar return on forecast: -0.000234868; OLS slope t, clustered by day: -0.201135 (threshold: positive with t >= 2 confirms (with check); negative with t <= -2 rejects; else inconclusive)
- Supporting check: mean excess return, forecast <= -10 minus forecast in (-10, 0): -0.000347441, passed: True
- Counts: grid cases with a nonzero forecast: 352, days of the cases: 174, grid cases with forecast at or below -10: 187, grid cases with forecast between -10 and 0: 165
- Decided by: The slope's t lies between -2 and +2.
- Reading: The coin's drift is the mean of all its grid 10-bar returns over all windows (nonzero forecast or not), the slope is from an OLS with an intercept whose t uses day-clustered standard errors with the usual small-sample correction, the plan's fewer-than-100-cases rule is applied as a minimum count (not observable), and the choppy profile is read from the recorded regime 'unknown'.
- Size: unusual move +0.87 % (t 1.48, the cases of one day together: 508 days) per case over 10 bars, 0.068 of the coin's usual move (14.49 %); normal drift in its direction -1.14 %, total -0.28 %; 658 cases
Plan: `steps_cards/03_test_plan/night9_chopdeep_run/plans/072-04.b1_choppy-deep-close-ten-day-fall_1d.md`
Record: `steps_cards/04_backtest/night9_chopdeep_run/backtests/072-04.b1_choppy-deep-close-ten-day-fall_1d`
Measure: `measure.py`
