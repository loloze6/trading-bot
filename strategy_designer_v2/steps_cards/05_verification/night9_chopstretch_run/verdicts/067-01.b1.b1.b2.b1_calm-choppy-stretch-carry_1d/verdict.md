---
plan: 067-01.b1.b1.b2.b1_calm-choppy-stretch-carry_1d
idea: 067-01.b1.b1.b2.b1_calm-choppy-stretch-carry
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of drift-adjusted 10-bar forward return on forecast: 0.000985369; OLS t, standard errors clustered by day: 1.22403 (threshold: slope positive with t >= 2 (and carry on both sides) to confirm; negative with t <= -2 to reject)
- Supporting check: carry on both sides: smaller of long mean and sign-flipped short mean drift-adjusted 10-bar return, must be > 0: 0.00375505, passed: True
- Counts: grid cases with nonzero forecast: 514, long cases: 274, short cases: 240
- Decided by: The slope has |t| < 2.
- Reading: Drift is the coin's mean 10-bar return on the non-overlapping grid of all its windows; 'cases on the same day together' is read as day-clustered standard errors of the OLS slope (with intercept); the supporting check is the sign of each side's mean; a minimum count not reached gives 'not observable'.
- Size: unusual move +0.25 % (t 0.41, the cases of one day together: 566 days) per case over 10 bars, 0.016 of the coin's usual move (15.92 %); normal drift in its direction +0.13 %, total +0.38 %; 971 cases
Plan: `steps_cards/03_test_plan/night9_chopstretch_run/plans/067-01.b1.b1.b2.b1_calm-choppy-stretch-carry_1d.md`
Record: `steps_cards/04_backtest/night9_chopstretch_run/backtests/067-01.b1.b1.b2.b1_calm-choppy-stretch-carry_1d`
Measure: `measure.py`
