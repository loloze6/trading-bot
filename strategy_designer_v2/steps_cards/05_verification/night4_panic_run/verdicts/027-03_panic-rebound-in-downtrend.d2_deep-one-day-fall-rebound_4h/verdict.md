---
plan: 027-03_panic-rebound-in-downtrend.d2_deep-one-day-fall-rebound_4h
idea: 027-03_panic-rebound-in-downtrend.d2_deep-one-day-fall-rebound
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled OLS slope of 84-bar excess return (return minus coin's normal drift) on forecast: -0.000863072; OLS slope t: -0.870628 (threshold: slope t >= 2 confirms (with supporting check), t <= -2 rejects, at least 200 cases)
- Supporting check: mean unusual move of cases with forecast > 0: -0.00781452, passed: False
- Counts: cases: 1152, cases with forecast above 0: 578
- Decided by: The slope's t is between -2 and 2.
- Reading: The 200-case minimum is read as the number of pooled grid samples in the regression. Each coin's normal drift is its mean 84-bar return over the grid samples of all its windows. A grid bar whose 84-bar end falls outside its window is left out.
- Size: unusual move -0.06 % per case over 84 bars, -0.005 of the coin's usual move (17.66 %); normal drift in its direction +2.11 %, total +2.04 %; 1152 cases
Plan: `steps_cards/03_test_plan/night4_panic_run/plans/027-03_panic-rebound-in-downtrend.d2_deep-one-day-fall-rebound_4h.md`
Record: `steps_cards/04_backtest/night4_panic_run/backtests/027-03_panic-rebound-in-downtrend.d2_deep-one-day-fall-rebound_4h`
Measure: `measure.py`
