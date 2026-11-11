---
plan: 002-02_sma-death-cross-downward-drift_1d
idea: 002-02_sma-death-cross-downward-drift
fit: adapted
status: inconclusive
---
Situation check: 1 of the active bars match the plan's situation and side
Evidence:
- Main measure: weighted mean excess gain of the short over holding (10 bars, non-overlapping, pooled): 0.00149497; t of |forecast|-weighted mean (weighted standard error): 0.261822 (threshold: confirm if mean > 0 with t >= 2; reject if mean < 0 with t <= -2; else inconclusive; fewer than 30 cases inconclusive)
- Supporting check: top minus bottom |forecast| tercile weighted excess gain: 0.00647281, passed: True
- Counts: non-overlapping short cases: 825
- Decided by: The t-statistic lies strictly between -2 and 2, which the plan calls inconclusive.
- Reading: Holding is each coin's mean 10-bar return over the same non-overlapping grid (positions 0, 10, 20, ... of every window) pooled across its windows, the short's excess gain is -(forward return - holding), the t uses the weighted standard error sqrt(n/(n-1) * sum(w^2 (x-m)^2)) / sum(w), and terciles are equal-count splits of the short cases sorted by |forecast| compared by their weighted means.
Plan: `steps_cards/03_test_plan/full_data_run/plans/002-02_sma-death-cross-downward-drift_1d.md`
Record: `steps_cards/04_backtest/full_data_run/backtests/002-02_sma-death-cross-downward-drift_1d`
Measure: `measure.py`
