---
plan: 031-01.b1_wide-day-extends-up-run_1d
idea: 031-01.b1_wide-day-extends-up-run
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope t of excess 3-bar return on forecast, clustered by day: 0.000707909; OLS slope t, day-clustered: 1.42708 (threshold: confirm if the slope is > 0 with t >= 2; reject if the slope is < 0 with t <= -2; at least 200 independent cases)
- Supporting check: none
- Counts: independent in-regime grid cases: 2907, days: 781
- Decided by: The slope's t = 1.43 lies between -2 and 2 over 2907 cases (inconclusive rule).
- Reading: Situation check: the 5-bar return is computed inside each window from closes, and the first 5 bars of a window are left out because they have no 5-bar history; main measure: the trending regime is read from the record's regime column, the coin's mean 3-bar return is taken over the non-overlapping grid of all its bars in all windows, the t is an OLS slope t with standard errors clustered by UTC day, and the independent cases are the in-regime grid cases with a 3-bar forward return.
- Size: unusual move +0.15 % (t 0.74, the cases of one day together: 1484 days) per case over 3 bars, 0.016 of the coin's usual move (7.96 %); normal drift in its direction +0.36 %, total +0.51 %; 3259 cases
Plan: `steps_cards/03_test_plan/night6_indecision_run/plans/031-01.b1_wide-day-extends-up-run_1d.md`
Record: `steps_cards/04_backtest/night6_indecision_run/backtests/031-01.b1_wide-day-extends-up-run_1d`
Measure: `measure.py`
