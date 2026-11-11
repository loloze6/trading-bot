---
plan: 002-01_sma-golden-cross-upward-drift_1d
idea: 002-01_sma-golden-cross-upward-drift
fit: adapted
status: rejected
---
Situation check: 1 of the active bars match the plan's situation and side
Evidence:
- Main measure: forecast-weighted mean 10-bar forward return minus mean 10-bar forward return of all bars of the same coin and window: -0.0225387; t of the forecast-weighted mean excess across non-overlapping blocks: -3.2857 (threshold: excess > 0 with t >= 2 confirms (with positive hit-rate difference); excess < 0 with t <= -2 rejects; otherwise or fewer than 30 positive-forecast blocks inconclusive)
- Supporting check: hit rate of positive-forecast bars minus hit rate of all bars (10-bar forward return > 0): -0.0201716, passed: False
- Counts: non-overlapping 10-bar blocks with a positive forecast: 832, non-overlapping 10-bar blocks, all bars: 1657
- Decided by: The excess over holding is negative with t <= -2: moves after up-crosses underperform holding.
- Reading: Blocks are the bars at positions 0, 10, 20, ... of each window with a full 10-bar forward return inside it; each positive-forecast block's return is taken minus the mean over all grid blocks of its own coin and window, then forecast-weighted and pooled, with t = weighted mean / weighted standard error; the hit-rate shares use the same grid pooled across coins and windows.
Plan: `steps_cards/03_test_plan/full_data_run/plans/002-01_sma-golden-cross-upward-drift_1d.md`
Record: `steps_cards/04_backtest/full_data_run/backtests/002-01_sma-golden-cross-upward-drift_1d`
Measure: `measure.py`
