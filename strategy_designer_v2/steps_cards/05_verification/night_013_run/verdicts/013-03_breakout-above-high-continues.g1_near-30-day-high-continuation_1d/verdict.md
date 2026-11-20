---
plan: 013-03_breakout-above-high-continues.g1_near-30-day-high-continuation_1d
idea: 013-03_breakout-above-high-continues.g1_near-30-day-high-continuation
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of slope of excess 10-bar forward return on forecast (pooled, non-overlapping): 0.00347844; OLS slope t: 2.97652 (threshold: confirm if t >= 2 with positive top-minus-bottom quintile difference; reject if t <= -2)
- Supporting check: top-minus-bottom forecast quintile mean excess 10-bar return: 0.0367837, passed: True
- Counts: independent 10-bar cases: 1691
- Decided by: The slope's t is 2 or more and the top-minus-bottom quintile difference is positive.
- Reading: Samples at positions 0,10,20,... of each window with a full 10-bar return inside it, the coin's mean 10-bar return taken over those pooled samples, OLS with intercept on the recorded forecast, quintiles by pooled forecast rank, and fewer than 300 cases reported as 'not observable' per the workflow's minimum-count rule.
- Size: unusual move +2.19 % per case over 10 bars, 0.134 of the coin's usual move (14.49 %); normal drift in its direction +0.28 %, total +2.47 %; 1073 cases
Plan: `steps_cards/03_test_plan/night_013_run/plans/013-03_breakout-above-high-continues.g1_near-30-day-high-continuation_1d.md`
Record: `steps_cards/04_backtest/night_013_run/backtests/013-03_breakout-above-high-continues.g1_near-30-day-high-continuation_1d`
Measure: `measure.py`
