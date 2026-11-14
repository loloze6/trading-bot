---
plan: 002-01_sma-upcross-upward-drift_1d
idea: 002-01_sma-upcross-upward-drift
fit: adapted
status: inconclusive
---
Evidence:
- Main measure: mean excess 10-bar forward return in long blocks over all-block mean (pooled, before costs): 0.00466185 (threshold: > 0 with t >= 2 to confirm; <= 0 rejects)
- Supporting check: hit rate in long blocks minus all-block hit rate (second view: slope of return on forecast): -0.0315271, passed: False
- Cases: 29
- Decided by: Inconclusive: excess > 0 but t < 2; hit rate not above unconditional; excess positive in fewer than 4 windows; result carried by a single window.
- Reading: Blocks start every 10 rows from each window's first row, using only blocks whose 10-bar end is inside the window; the random-point baseline is the pooled mean (and hit rate) over all such blocks; the per-window excess is that window's long-block mean minus the pooled baseline; the slope is fitted over all blocks; 'carried by a single window' means the pooled excess turns <= 0 once the window with the largest summed excess is removed; a failed hit-rate test with t >= 2 counts as inconclusive.
Plan: `steps_cards/03_test_plan/plans/002-01_sma-upcross-upward-drift_1d.md`
Record: `steps_cards/04_backtest/backtests/002-01_sma-upcross-upward-drift_1d`
Measure: `measure.py`
