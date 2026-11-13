---
plan: N2-03_deep-month-loss-rebound_1d
idea: N2-03_deep-month-loss-rebound
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean excess forward 20-bar return after top-decile positive forecasts: 0.0333368; t of the mean (non-overlapping episodes): 1.84542 (threshold: confirm if mean > 0 with t >= 2; reject if mean < 0 with t <= -2)
- Supporting check: slope of excess forward 20-bar return on forecast, nonzero-forecast bars: 0.000543474, passed: True
- Counts: non-overlapping top-decile episodes: 108
- Decided by: With at least 30 episodes, the t of the mean excess forward return lies between -2 and 2.
- Reading: The situation is a negative raw 20-bar change on the long side; the top decile is forecasts at or above the pooled 90th percentile of all positive forecasts, episodes are top-decile bars at positions 0, 20, 40, ... of each window, the coin's mean is over all its within-window 20-bar returns, and the supporting slope uses all nonzero-forecast bars by OLS.
Plan: `steps_cards/03_test_plan/overnight_run/plans/N2-03_deep-month-loss-rebound_1d.md`
Record: `steps_cards/04_backtest/overnight_run/backtests/N2-03_deep-month-loss-rebound_1d`
Measure: `measure.py`
