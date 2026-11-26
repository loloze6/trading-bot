---
plan: 058-03.e1_calm-rise-stretch-ten-days_1d
idea: 058-03.e1_calm-rise-stretch-ten-days
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of 10-bar forward excess return on raw dist20, in-profile grid bars, pooled: 0.00239078; OLS slope t: 2.3219 (threshold: slope t >= 2 confirms (with positive supporting excess), t <= -2 rejects)
- Supporting check: mean 10-bar excess return on grid bars with forecast > 0: 0.0174127, passed: True
- Counts: in-profile grid cases: 301, grid bars with forecast > 0: 216
- Decided by: The slope's t is 2 or more and the supporting check's mean excess return is above 0.
- Reading: In-profile means regime 'unknown' with a recorded raw dist20; the coin's mean 10-bar return is the mean over all its windows' non-overlapping grid returns (positions 0, 10, 20, ... from each window's first row); the plan's 'fewer than 30 in-profile grid cases' minimum is reported as 'not observable' as the workflow requires.
- Size: unusual move +1.46 % (t 1.41, the cases of one day together: 264 days) per case over 10 bars, 0.095 of the coin's usual move (14.49 %); normal drift in its direction +1.27 %, total +2.73 %; 352 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.002098 on the check folds against +0.002391 on every fold
Plan: `steps_cards/03_test_plan/night8_risingagitated_run/plans/058-03.e1_calm-rise-stretch-ten-days_1d.md`
Record: `steps_cards/04_backtest/night8_risingagitated_run/backtests/058-03.e1_calm-rise-stretch-ten-days_1d`
Measure: `measure.py`
