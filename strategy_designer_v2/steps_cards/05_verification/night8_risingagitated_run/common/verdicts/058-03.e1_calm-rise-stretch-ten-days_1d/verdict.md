---
plan: 058-03.e1_calm-rise-stretch-ten-days_1d
idea: 058-03.e1_calm-rise-stretch-ten-days
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of 10-bar forward excess return on raw dist20, in-profile grid bars, pooled: 0.00184524; OLS slope t: 3.12267 (threshold: slope t >= 2 confirms (with positive supporting excess), t <= -2 rejects)
- Supporting check: mean 10-bar excess return on grid bars with forecast > 0: 0.00714784, passed: True
- Counts: in-profile grid cases: 692, grid bars with forecast > 0: 490
- Decided by: The slope's t is 2 or more and the supporting check's mean excess return is above 0.
- Reading: In-profile means regime 'unknown' with a recorded raw dist20; the coin's mean 10-bar return is the mean over all its windows' non-overlapping grid returns (positions 0, 10, 20, ... from each window's first row); the plan's 'fewer than 30 in-profile grid cases' minimum is reported as 'not observable' as the workflow requires.
- Size: unusual move +1.35 % (t 1.65, the cases of one day together: 494 days) per case over 10 bars, 0.087 of the coin's usual move (16.68 %); normal drift in its direction +1.34 %, total +2.68 %; 820 cases
- Direction check on folds A, D (the years step 7 does not explore): not judged: no check fold (the plan has none, or the backtest did not run on its folds)
Plan: `steps_cards/03_test_plan/night8_risingagitated_run/plans/058-03.e1_calm-rise-stretch-ten-days_1d.md`
Record: `steps_cards/04_backtest/night8_risingagitated_run/common/backtests/058-03.e1_calm-rise-stretch-ten-days_1d`
Measure: `measure.py`
