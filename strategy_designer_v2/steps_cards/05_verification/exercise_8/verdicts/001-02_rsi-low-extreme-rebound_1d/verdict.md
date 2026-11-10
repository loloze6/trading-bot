---
plan: 001-02_rsi-low-extreme-rebound_1d
idea: 001-02_rsi-low-extreme-rebound
fit: adapted
status: inconclusive
---
Situation check: 1 of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled mean 5-bar excess return (vs window hold average) after top-quintile forecast bars: 0.00470992; t of the mean: 0.60183 (threshold: confirm if t >= 2 and supporting check holds; reject if t <= -2; inconclusive otherwise or if < 30 pooled top-quintile cases or < 8 per coin)
- Supporting check: coins with top-quintile minus neutral excess > 0 (need >= 2): 2, passed: True
- Counts: pooled non-overlapping top-quintile cases: 77, top-quintile cases BTCUSD: 36, top-quintile cases ETHUSD: 41, coins with positive top-minus-neutral excess: 2
- Decided by: Inconclusive: t lies between -2 and 2, or t >= 2 but the supporting check (positive in at least 2 coins) fails.
- Reading: Top quintile is forecast >= the 80th percentile of each coin's non-zero forecasts over all its windows, the hold baseline is the mean of all 5-bar forward returns in the same window, and with only the coins present the supporting check still requires at least 2 positive coins.
Plan: `steps_cards/03_test_plan/plans/001-02_rsi-low-extreme-rebound_1d.md`
Record: `steps_cards/04_backtest/backtests/001-02_rsi-low-extreme-rebound_1d`
Measure: `measure.py`
