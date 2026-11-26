---
plan: 013-03_breakout-above-high-continues.g1_near-30-day-high-continuation_1d
idea: 013-03_breakout-above-high-continues.g1_near-30-day-high-continuation
fit: exact
status: not observable
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of slope of excess 10-bar forward return on forecast (pooled, non-overlapping): 0.00342062; OLS slope t: 0.737328 (threshold: confirm if t >= 2 with positive top-minus-bottom quintile difference; reject if t <= -2)
- Supporting check: top-minus-bottom forecast quintile mean excess 10-bar return: 0.0353608, passed: True
- Counts: independent 10-bar cases: 284
- Decided by: Only 284 independent 10-bar cases, fewer than the plan's minimum of 300.
- Reading: Samples at positions 0,10,20,... of each window with a full 10-bar return inside it, the coin's mean 10-bar return taken over those pooled samples, OLS with intercept on the recorded forecast, quintiles by pooled forecast rank, and fewer than 300 cases reported as 'not observable' per the workflow's minimum-count rule.
- Size: unusual move +3.64 % (t 1.35, the cases of one day together: 154 days) per case over 10 bars, 0.113 of the coin's usual move (30.80 %); normal drift in its direction +4.14 %, total +7.78 %; 193 cases
Plan: `steps_cards/03_test_plan/night_013_run/plans/013-03_breakout-above-high-continues.g1_near-30-day-high-continuation_1d.md`
Record: `steps_cards/04_backtest/night_013_run/unseen_2016_2017/backtests/013-03_breakout-above-high-continues.g1_near-30-day-high-continuation_1d`
Measure: `measure.py`
