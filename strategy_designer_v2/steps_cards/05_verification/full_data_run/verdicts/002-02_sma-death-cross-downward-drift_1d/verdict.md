---
plan: 002-02_sma-death-cross-downward-drift_1d
idea: 002-02_sma-death-cross-downward-drift
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: |forecast|-weighted mean excess gain of the short over holding, 10 bars, non-overlapping, pooled: 0.00223806; t of the |forecast|-weighted mean: 0.391989 (threshold: confirm if > 0 with t >= 2; reject if < 0 with t <= -2; else inconclusive; fewer than 30 cases inconclusive)
- Supporting check: top minus bottom tercile of |forecast|, weighted mean short excess gain: 0.00711283, passed: True
- Counts: non-overlapping short cases: 825
- Decided by: The t-statistic lies strictly between -2 and 2, which the plan calls inconclusive.
- Reading: Holding is the coin's mean of all overlapping 10-bar forward returns over all its windows, the short's excess gain is -(forward return - holding), cases are bars 0,10,20,... of each window with forecast < 0, the t uses a weighted-mean standard error sqrt(sum w^2 (x-m)^2 * n/(n-1)) / sum w, and terciles are equal-count thirds of the pooled cases ranked by |forecast|, compared by their |forecast|-weighted means.
Plan: `steps_cards/03_test_plan/full_data_run/plans/002-02_sma-death-cross-downward-drift_1d.md`
Record: `steps_cards/04_backtest/full_data_run/backtests/002-02_sma-death-cross-downward-drift_1d`
Measure: `measure.py`
