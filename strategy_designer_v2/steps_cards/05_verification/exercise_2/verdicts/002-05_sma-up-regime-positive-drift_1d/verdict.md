---
plan: 002-05_sma-up-regime-positive-drift_1d
idea: 002-05_sma-up-regime-positive-drift
fit: adapted
status: inconclusive
---
Evidence:
- Main measure: in-stretch minus all-bar mean next-bar return (one-sided t-stat): 0.627829 (threshold: t >= 2.0 with positive difference confirms; difference <= 0 or t <= -2.0 rejects)
- Supporting check: in-stretch up-day share minus all-bar up-day share: -0.000657268, passed: False
- Cases: 290
- Decided by: Inconclusive: the t-statistic lies between -2.0 and 2.0.
- Reading: t-statistic is the one-sample t of in-stretch next-bar returns against the pooled all-bar mean (mean_in - mean_all) / (sd_in / sqrt(n_in)); in-stretch means forecast > 0; a distinct up-cross stretch is a contiguous run of forecast > 0 within one window, including a run already under way at a window's first bar; insufficient counts are checked first, then reject, then confirm.
Plan: `steps_cards/03_test_plan/plans/002-05_sma-up-regime-positive-drift_1d.md`
Record: `steps_cards/04_backtest/backtests/002-05_sma-up-regime-positive-drift_1d`
Measure: `measure.py`
