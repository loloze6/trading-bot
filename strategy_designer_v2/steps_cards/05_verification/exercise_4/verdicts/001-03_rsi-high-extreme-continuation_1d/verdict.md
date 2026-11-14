---
plan: 001-03_rsi-high-extreme-continuation_1d
idea: 001-03_rsi-high-extreme-continuation
fit: adapted
status: rejected
---
Evidence:
- Main measure: mean 5-bar forward return, extreme minus neutral bars: -0.000700598; Welch t: -0.0556966 (threshold: positive with t >= 2 to confirm; t <= 0 rejects)
- Supporting check: strategy return minus exposure-scaled buy-and-hold, pooled, before costs: -0.716453, passed: False
- Counts: non-overlapping extreme cases pooled: 42, neutral cases: 180, coins with positive difference: 1, coins present: 2
- Decided by: The pooled extreme-minus-neutral difference is zero or negative (t <= 0), which rejects.
- Reading: The top-20% cut-off is the 80th percentile of all non-zero forecasts pooled over every coin, window and row (extreme means forecast >= the cut-off). Neutral means forecast < 1, including 0. Only the grid bars 0, 5, 10, ... of each window are used. The 'at least 2 of 3 coins' rule is applied as at least 2 positive coins among those present. The supporting excess is the sum of daily allocation x next-bar return minus the mean allocation x the summed daily coin returns, added over windows and coins, and it is judged by the sign of the pooled total.
Plan: `steps_cards/03_test_plan/plans/001-03_rsi-high-extreme-continuation_1d.md`
Record: `steps_cards/04_backtest/backtests/001-03_rsi-high-extreme-continuation_1d`
Measure: `measure.py`
