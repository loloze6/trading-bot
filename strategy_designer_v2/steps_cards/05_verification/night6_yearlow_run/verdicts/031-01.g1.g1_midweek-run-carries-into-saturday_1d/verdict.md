---
plan: 031-01.g1.g1_midweek-run-carries-into-saturday_1d
idea: 031-01.g1.g1_midweek-run-carries-into-saturday
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of forecast/10 x (Saturday return - coin mean daily return) over Friday cases: 0.00545422; t of the mean, cases of one date summed: 3.31152 (threshold: confirm: mean > 0 with date-clustered t >= 2 and positive forecast coefficient; reject: mean < 0 with t <= -2; at least 100 distinct Fridays with cases)
- Supporting check: forecast coefficient in OLS of Saturday excess return on forecast and Friday return: 0.000409817, passed: True
- Counts: distinct Fridays with cases: 414, cases: 2476, regression cases: 2459
- Decided by: The main measure is positive with t >= 2 and the forecast's regression coefficient is positive.
- Reading: Friday is the bar whose UTC start timestamp is a Friday and the Monday-to-Thursday side is taken from close[t-1]/close[t-4]-1 (falling back on the sign of the raw mon_thu value when those bars are missing); the date-summed t is the cluster-robust t of the mean (deviations summed per date, G/(G-1) correction); the regression uses OLS with an intercept on cases with Friday's return available; and the plan's minimum of 100 distinct Fridays is applied as 'not observable' when unmet.
- Size: unusual move +0.40 % (t 3.02, the cases of one day together: 413 days) per case over 1 bars, 0.085 of the coin's usual move (4.78 %); normal drift in its direction -0.00 %, total +0.40 %; 2138 cases
Plan: `steps_cards/03_test_plan/night6_yearlow_run/plans/031-01.g1.g1_midweek-run-carries-into-saturday_1d.md`
Record: `steps_cards/04_backtest/night6_yearlow_run/backtests/031-01.g1.g1_midweek-run-carries-into-saturday_1d`
Measure: `measure.py`
