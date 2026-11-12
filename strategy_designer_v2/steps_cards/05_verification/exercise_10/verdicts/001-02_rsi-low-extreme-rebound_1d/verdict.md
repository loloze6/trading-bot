---
plan: 001-02_rsi-low-extreme-rebound_1d
idea: 001-02_rsi-low-extreme-rebound
fit: adapted
status: inconclusive
---
Situation check: 1 of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled mean 5-bar excess return (vs coin's window hold average) after top-quintile forecast bars: 0.00388501; t of the mean: 0.496856 (threshold: confirm if pooled t >= 2 and the supporting check holds; reject if pooled t <= -2; otherwise inconclusive; at least 30 pooled non-overlapping top-quintile cases and at least 8 per coin)
- Supporting check: coins where top-quintile excess minus neutral excess > 0 (need >= 2): 1, passed: False
- Counts: pooled top-quintile cases: 77, top-quintile cases BTCUSD: 36, top-quintile cases ETHUSD: 41
- Decided by: Pooled t = 0.50 lies between -2 and 2, the plan's inconclusive rule.
- Reading: The top quintile is the coin's non-zero forecasts at or above their 80th percentile over all its windows; the hold baseline is the mean 5-bar return over the window's non-overlapping grid; the per-coin minimum of 8 and the '2 of 3 coins' rule are applied to the coins present in the record (BTC, ETH), so both must be positive.
Plan: `steps_cards/03_test_plan/plans/001-02_rsi-low-extreme-rebound_1d.md`
Record: `steps_cards/04_backtest/backtests/001-02_rsi-low-extreme-rebound_1d`
Measure: `measure.py`
