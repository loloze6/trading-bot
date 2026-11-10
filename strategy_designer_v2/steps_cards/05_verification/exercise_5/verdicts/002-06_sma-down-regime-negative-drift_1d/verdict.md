---
plan: 002-06_sma-down-regime-negative-drift_1d
idea: 002-06_sma-down-regime-negative-drift
fit: adapted
status: inconclusive
---
Evidence:
- Main measure: in-state mean next-bar return minus all-bars mean (% per day): -0.0578031; stretch-clustered t: -0.312946 (threshold: at least 0.10% per day below the all-bars mean with stretch-clustered t <= -2)
- Supporting check: down-bar share in stretches minus over all bars; equity above flat and beats holding in-state: -0.000439188, passed: False
- Counts: distinct down-cross stretches: 5, in-state bars: 434
- Decided by: Inconclusive: the difference is negative but t > -2, or it is smaller than 0.10% per day, or the down-bar share inside the stretches is not higher than over all bars.
- Reading: In-state bars are bars with forecast < 0 that have a next close in the same window, a stretch is each run of consecutive such bars within one window, the t uses a cluster-robust (by stretch, G/(G-1) corrected) standard error of the in-state mean taking the all-bars mean as the reference, and the confirm rule uses only the down-bar share comparison while 'passed' also requires the pre-cost equity (compounded over all bars) to end above 1 and to beat holding over in-state bars.
Plan: `steps_cards/03_test_plan/plans/002-06_sma-down-regime-negative-drift_1d.md`
Record: `steps_cards/04_backtest/backtests/002-06_sma-down-regime-negative-drift_1d`
Measure: `measure.py`
