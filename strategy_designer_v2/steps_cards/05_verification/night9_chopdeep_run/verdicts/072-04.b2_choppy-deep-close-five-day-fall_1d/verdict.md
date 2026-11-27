---
plan: 072-04.b2_choppy-deep-close-five-day-fall_1d
idea: 072-04.b2_choppy-deep-close-five-day-fall
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: clustered-by-day t of the slope of drift-adjusted 5-bar return on forecast (grid bars, forecast < 0): 3.20714e-05; slope t, clustered by day (CR1): 0.0440604 (threshold: confirm if t >= +2 with supporting check passing; reject if t <= -2; else inconclusive; at least 100 grid cases with forecast < 0)
- Supporting check: mean drift-adjusted 5-bar return on grid bars with forecast <= -10 is below 0: -0.0131221, passed: True
- Counts: grid cases with forecast below 0: 721, days of those cases: 352, grid cases with forecast at or below -10: 379
- Decided by: The slope's t lies between -2 and +2 (inconclusive rule).
- Reading: Grid cases are grid bars (positions 0,5,10,... per window) with a 5-bar forward return inside the window, the normal drift is each coin's mean 5-bar return over all its grid bars in all windows, 'cases of one day together' is a day-clustered (CR1) OLS slope t, the choppy situation is the recorded default regime 'unknown', and a missing minimum count gives 'not observable' as the workflow requires.
- Size: unusual move +0.64 % (t 2.00, the cases of one day together: 702 days) per case over 5 bars, 0.071 of the coin's usual move (10.60 %); normal drift in its direction -0.56 %, total +0.08 %; 958 cases
Plan: `steps_cards/03_test_plan/night9_chopdeep_run/plans/072-04.b2_choppy-deep-close-five-day-fall_1d.md`
Record: `steps_cards/04_backtest/night9_chopdeep_run/backtests/072-04.b2_choppy-deep-close-five-day-fall_1d`
Measure: `measure.py`
