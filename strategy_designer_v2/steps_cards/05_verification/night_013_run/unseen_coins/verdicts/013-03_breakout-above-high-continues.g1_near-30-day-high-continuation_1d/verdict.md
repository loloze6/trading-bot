---
plan: 013-03_breakout-above-high-continues.g1_near-30-day-high-continuation_1d
idea: 013-03_breakout-above-high-continues.g1_near-30-day-high-continuation
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of slope of excess 10-bar forward return on forecast (pooled, non-overlapping): 0.00302987; OLS slope t: 2.06499 (threshold: confirm if t >= 2 with positive top-minus-bottom quintile difference; reject if t <= -2)
- Supporting check: top-minus-bottom forecast quintile mean excess 10-bar return: 0.0267338, passed: True
- Counts: independent 10-bar cases: 1907
- Decided by: The slope's t is 2 or more and the top-minus-bottom quintile difference is positive.
- Reading: Samples at positions 0,10,20,... of each window with a full 10-bar return inside it, the coin's mean 10-bar return taken over those pooled samples, OLS with intercept on the recorded forecast, quintiles by pooled forecast rank, and fewer than 300 cases reported as 'not observable' per the workflow's minimum-count rule.
- Size: unusual move +1.57 % (t 1.90, the cases of one day together: 641 days) per case over 10 bars, 0.091 of the coin's usual move (16.96 %); normal drift in its direction +0.44 %, total +2.02 %; 1170 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.00245 on the check folds against +0.00303 on every fold
Plan: `steps_cards/03_test_plan/night_013_run/plans/013-03_breakout-above-high-continues.g1_near-30-day-high-continuation_1d.md`
Record: `steps_cards/04_backtest/night_013_run/unseen_coins/backtests/013-03_breakout-above-high-continues.g1_near-30-day-high-continuation_1d`
Measure: `measure.py`
