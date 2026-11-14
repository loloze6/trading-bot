---
plan: 002-06_sma-down-regime-negative-drift_1d
idea: 002-06_sma-down-regime-negative-drift
fit: adapted
status: inconclusive
---
Evidence:
- Main measure: in-state mean next-bar return minus all-bars mean: -0.000578031; stretch-clustered t: -0.312946 (threshold: difference <= -0.10% per day (-0.001) with stretch-clustered t <= -2)
- Supporting check: down-bar share in stretches minus share over all bars: -0.000439188, passed: False
- Counts: distinct down-cross stretches: 5, in-state bars pooled: 434
- Decided by: Inconclusive: the difference is negative but t > -2, or smaller than 0.10% per day, or the down-bar share in stretches is not higher than over all bars. (Info: strategy equity end 0.9423561551789104, holding over in-state bars end 0.6993358720075438.)
- Reading: In-state bars are bars with forecast < 0 and a next-bar return in the same window, stretches are contiguous runs of such bars per window (a run open at a window edge counts as a stretch), t is the difference divided by the cluster-robust (CR1) SE of the in-state mean over stretches treating the all-bars mean as fixed, and only the down-share comparison enters the confirm rule while the equity checks are reported for information.
Plan: `steps_cards/03_test_plan/plans/002-06_sma-down-regime-negative-drift_1d.md`
Record: `steps_cards/04_backtest/backtests/002-06_sma-down-regime-negative-drift_1d`
Measure: `measure.py`
