---
plan: 010-05_rsi-above-share-reversal_1d
idea: 010-05_rsi-above-share-reversal
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of coin-demeaned 14-bar forward return on forecast: -0.0010096; OLS slope t: -1.43368 (threshold: confirm if slope > 0 with t >= 2, reject if slope < 0 with t <= -2, on at least 300 independent cases)
- Supporting check: book mean daily timing gain before costs (> 0): -0.000985372, passed: False
- Counts: independent cases: 384
- Decided by: The slope t is between -2 and 2.
- Reading: Grid bars at positions 0, 14, 28, ... of each window with a full 14-bar forward return inside the window, coin mean = mean of those grid returns over all its windows, pooled OLS with intercept; the timing check uses the position held after each day's trade times the next day's close-to-close return (before costs) minus that position times the coin's all-window mean daily return, averaged over coins per day, then over days.
Plan: `steps_cards/03_test_plan/night_rsi_run/plans/010-05_rsi-above-share-reversal_1d.md`
Record: `steps_cards/04_backtest/night_rsi_run/backtests/010-05_rsi-above-share-reversal_1d`
Measure: `measure.py`
