---
plan: 001-03_rsi-high-extreme-continuation_1d
idea: 001-03_rsi-high-extreme-continuation
fit: adapted
status: rejected
---
Situation check: 1 of the active bars match the plan's situation and side
Evidence:
- Main measure: mean 5-bar forward return after extreme minus after neutral bars: -0.000700598; Welch t: -0.0556966 (threshold: t >= 2 confirms (with >= 2 coins positive and positive pooled supporting excess); t <= 0 rejects)
- Supporting check: strategy return minus exposure-scaled buy-and-hold, pooled: 0.467728, passed: True
- Counts: non-overlapping extreme cases pooled: 42, neutral cases: 180, coins with positive difference: 1, coins in record: 2
- Decided by: Reject: the pooled difference is zero or negative (t <= 0).
- Reading: The 80th-percentile cut of non-zero forecasts is pooled over all coins and windows, neutral bars are forecast < 1 (including 0) on the same 0,5,10,... grid, 'at least 2 of the 3 coins' is applied as at least 2 coins among those in the record, and the supporting excess per coin is the summed daily strategy gain minus the coin's mean allocation times its summed daily returns, added over coins.
Plan: `steps_cards/03_test_plan/plans/001-03_rsi-high-extreme-continuation_1d.md`
Record: `steps_cards/04_backtest/backtests/001-03_rsi-high-extreme-continuation_1d`
Measure: `measure.py`
