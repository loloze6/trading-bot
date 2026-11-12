---
plan: 001-04_rsi-low-extreme-continuation_1d
idea: 001-04_rsi-low-extreme-continuation
fit: adapted
status: inconclusive
---
Situation check: 1 of the active bars match the plan's situation and side
Evidence:
- Main measure: mean 5-bar forward return after extremes minus after neutral: -0.00471703; Welch t: -0.47198 (threshold: confirm if negative with Welch t <= -2; reject if positive with t >= +2)
- Supporting check: same sign in at least 2 of 2 coins: 1, passed: False
- Counts: non-overlapping extreme cases: 77, non-overlapping neutral cases: 160
- Decided by: Welch t = -0.47 lies between -2 and +2.
- Reading: Quintiles of |forecast| are cut over the pooled non-overlapping grid bars (positions 0,5,10,... of each window) that have a non-zero forecast and a valid 5-bar forward return, extremes being |forecast| >= the 80th percentile and neutral being forecast 0 or |forecast| <= the 20th percentile; the difference is extremes minus neutral with Welch t; with only the coins present, the supporting check requires the same sign in at least 2 coins of those in the record.
Plan: `steps_cards/03_test_plan/plans/001-04_rsi-low-extreme-continuation_1d.md`
Record: `steps_cards/04_backtest/backtests/001-04_rsi-low-extreme-continuation_1d`
Measure: `measure.py`
