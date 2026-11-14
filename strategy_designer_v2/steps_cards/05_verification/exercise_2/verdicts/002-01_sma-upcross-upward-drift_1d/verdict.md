---
plan: 002-01_sma-upcross-upward-drift_1d
idea: 002-01_sma-upcross-upward-drift
fit: adapted
status: inconclusive
---
Evidence:
- Main measure: mean excess 10-bar return of long blocks over all-block mean: 0.00466185 (threshold: > 0 with t >= 2 to confirm; <= 0 to reject)
- Supporting check: hit rate of long blocks minus unconditional hit rate: -0.0315271, passed: False
- Cases: 29
- Decided by: Inconclusive: the excess is > 0 but t = 0.295679652303545 is below 2; the long hit rate is not above the unconditional hit rate; the excess is positive in only 2 windows (needs 4).
- Reading: Blocks are consecutive non-overlapping 10-bar blocks starting at each window's first row, and a block is long when the forecast at its start is > 0. The baseline is the pooled mean over all blocks of all windows, and the per-window excess is that window's long-block mean minus this pooled baseline. The t-stat is a one-sample t on the long-block excess returns. 'Carried by a single window' is read as the excess being positive in only one window; with fewer than 4 windows containing long blocks, confirmation cannot be met.
Plan: `steps_cards/03_test_plan/plans/002-01_sma-upcross-upward-drift_1d.md`
Record: `steps_cards/04_backtest/backtests/002-01_sma-upcross-upward-drift_1d`
Measure: `measure.py`
