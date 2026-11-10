---
plan: 001-02_rsi-low-extreme-rebound_1d
idea: 001-02_rsi-low-extreme-rebound
fit: adapted
status: rejected
---
Evidence:
- Main measure: top-quintile minus zero-forecast forward 5-bar return: -0.0140356 (threshold: > 0 with t-stat >= 2 (pooled, non-overlapping), positive in >= 2 coins)
- Supporting check: Spearman rank correlation of forecast vs forward 5-bar return (forecast > 0): -0.0988932, passed: False
- Cases: 102
- Decided by: Pooled excess return is at or below 0 and non-positive in 2 coins (>= 2), so rejected.
- Reading: Top quintile is forecast >= the 80th percentile of all positive forecasts pooled across coins and windows; non-overlap is enforced greedily within each coin-window for each group (top, zero, positive) keeping bars at least 5 bars apart; the t-statistic is Welch's two-sample t of top versus zero samples; with only the coins present in the record, 'at least 2 of the 3 coins' is applied as a count of at least 2 among those coins (so both when two are present); the supporting check passes if the Spearman correlation is above 0 and does not enter the decision.
Plan: `steps_cards/03_test_plan/plans/001-02_rsi-low-extreme-rebound_1d.md`
Record: `steps_cards/04_backtest/backtests/001-02_rsi-low-extreme-rebound_1d`
Measure: `measure.py`
