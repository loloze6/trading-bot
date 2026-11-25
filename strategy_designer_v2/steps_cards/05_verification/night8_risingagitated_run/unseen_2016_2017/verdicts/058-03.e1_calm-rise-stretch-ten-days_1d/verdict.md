---
plan: 058-03.e1_calm-rise-stretch-ten-days_1d
idea: 058-03.e1_calm-rise-stretch-ten-days
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of 10-bar forward excess return on raw dist20, in-profile grid bars, pooled: 0.000829414; OLS slope t: 0.195718 (threshold: slope t >= 2 confirms (with positive supporting excess), t <= -2 rejects)
- Supporting check: mean 10-bar excess return on grid bars with forecast > 0: -0.0118196, passed: False
- Counts: in-profile grid cases: 36, grid bars with forecast > 0: 31
- Decided by: The slope's t is between -2 and 2.
- Reading: In-profile means regime 'unknown' with a recorded raw dist20; the coin's mean 10-bar return is the mean over all its windows' non-overlapping grid returns (positions 0, 10, 20, ... from each window's first row); the plan's 'fewer than 30 in-profile grid cases' minimum is reported as 'not observable' as the workflow requires.
- Size: unusual move -1.78 % (t -0.74, the cases of one day together: 42 days) per case over 10 bars, -0.029 of the coin's usual move (24.91 %); normal drift in its direction +7.64 %, total +5.86 %; 42 cases
Plan: `steps_cards/03_test_plan/night8_risingagitated_run/plans/058-03.e1_calm-rise-stretch-ten-days_1d.md`
Record: `steps_cards/04_backtest/night8_risingagitated_run/unseen_2016_2017/backtests/058-03.e1_calm-rise-stretch-ten-days_1d`
Measure: `measure.py`
