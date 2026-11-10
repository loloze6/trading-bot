---
plan: 001-02_rsi-low-extreme-rebound_1d
idea: 001-02_rsi-low-extreme-rebound
fit: adapted
status: inconclusive
---
Situation check: 1 of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled mean 5-bar excess return (vs coin's window hold average) after top-quintile forecasts: 0.00388501; t of the mean: 0.496856 (threshold: t >= 2 with supporting check to confirm; t <= -2 to reject)
- Supporting check: coins (of 3) with top-quintile minus neutral excess > 0, need >= 2: 1, passed: False
- Counts: pooled non-overlapping top-quintile cases: 77, top-quintile cases BTCUSD: 36, top-quintile cases ETHUSD: 41, coins with positive top-minus-neutral excess: 1
- Decided by: Inconclusive: t is between -2 and 2.
- Reading: The top quintile is defined per coin as forecasts at or above the 80th percentile of that coin's non-zero forecasts pooled over its windows, the hold baseline is the mean 5-bar return on the same window's non-overlapping grid, and the '2 of 3 coins' rule is applied literally as at least 2 positive coins among those present.
Plan: `steps_cards/03_test_plan/plans/001-02_rsi-low-extreme-rebound_1d.md`
Record: `steps_cards/04_backtest/backtests/001-02_rsi-low-extreme-rebound_1d`
Measure: `measure.py`
