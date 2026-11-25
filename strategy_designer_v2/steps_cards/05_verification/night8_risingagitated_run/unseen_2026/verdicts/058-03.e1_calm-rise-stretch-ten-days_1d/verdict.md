---
plan: 058-03.e1_calm-rise-stretch-ten-days_1d
idea: 058-03.e1_calm-rise-stretch-ten-days
fit: exact
status: not observable
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of 10-bar forward excess return on raw dist20, in-profile grid bars, pooled: 0.00759725; OLS slope t: 2.59107 (threshold: slope t >= 2 confirms (with positive supporting excess), t <= -2 rejects)
- Supporting check: mean 10-bar excess return on grid bars with forecast > 0: 0.0473009, passed: True
- Counts: in-profile grid cases: 29, grid bars with forecast > 0: 22
- Decided by: Only 29 in-profile grid cases, fewer than the plan's minimum of 30.
- Reading: In-profile means regime 'unknown' with a recorded raw dist20; the coin's mean 10-bar return is the mean over all its windows' non-overlapping grid returns (positions 0, 10, 20, ... from each window's first row); the plan's 'fewer than 30 in-profile grid cases' minimum is reported as 'not observable' as the workflow requires.
- Size: unusual move +6.24 % (t 1.93, the cases of one day together: 30 days) per case over 10 bars, 0.411 of the coin's usual move (9.14 %); normal drift in its direction +1.10 %, total +7.34 %; 39 cases
Plan: `steps_cards/03_test_plan/night8_risingagitated_run/plans/058-03.e1_calm-rise-stretch-ten-days_1d.md`
Record: `steps_cards/04_backtest/night8_risingagitated_run/unseen_2026/backtests/058-03.e1_calm-rise-stretch-ten-days_1d`
Measure: `measure.py`
