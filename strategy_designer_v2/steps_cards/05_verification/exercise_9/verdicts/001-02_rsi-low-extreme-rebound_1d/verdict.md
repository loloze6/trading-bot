---
plan: 001-02_rsi-low-extreme-rebound_1d
idea: 001-02_rsi-low-extreme-rebound
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled mean 5-bar excess return after top-quintile forecasts (vs window hold average): 0.00388501; t of the mean: 0.496856 (threshold: confirm if t >= 2 with the supporting check; reject if t <= -2)
- Supporting check: coins where top-quintile excess minus neutral excess > 0 (need >= 2): 1, passed: False
- Counts: pooled non-overlapping top-quintile cases: 77, BTCUSD top-quintile cases: 36, ETHUSD top-quintile cases: 41
- Decided by: The pooled t lies between -2 and 2.
- Reading: Top quintile is the 80th percentile of each coin's non-zero forecasts across all its windows, the hold baseline is the mean non-overlapping 5-bar return of the same window, and with only BTC and ETH in the record the per-coin minimum applies to these two coins and the supporting check needs both of them positive.
Plan: `steps_cards/03_test_plan/plans/001-02_rsi-low-extreme-rebound_1d.md`
Record: `steps_cards/04_backtest/backtests/001-02_rsi-low-extreme-rebound_1d`
Measure: `measure.py`
