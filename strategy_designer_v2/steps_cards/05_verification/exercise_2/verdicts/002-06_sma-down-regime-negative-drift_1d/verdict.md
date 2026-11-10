---
plan: 002-06_sma-down-regime-negative-drift_1d
idea: 002-06_sma-down-regime-negative-drift
fit: adapted
status: inconclusive
---
Evidence:
- Main measure: pooled mean next-bar return on forecast<0 bars minus all-bars mean: -0.000578031 (threshold: at most -0.10% per day with stretch-clustered t <= -2; reject if >= 0)
- Supporting check: down-bar share in-state minus all bars (also: equity ends above flat, beats holding in-state): -0.000439188, passed: False
- Cases: 434
- Decided by: Inconclusive: the difference is negative but t > -2, or it is smaller than 0.10% per day, or the down-bar share is not higher inside the stretches.
- Reading: In-state bars are bars with forecast < 0 and stretches are their contiguous runs within one window (a run cut by a window edge counts once per window); the clustered SE treats the all-bars mean as fixed with a G/(G-1) correction; the confirm rule uses only the down-bar share from the supporting check, while the equity checks (pooled compounded before-cost gains) are reported in 'passed'.
Plan: `steps_cards/03_test_plan/plans/002-06_sma-down-regime-negative-drift_1d.md`
Record: `steps_cards/04_backtest/backtests/002-06_sma-down-regime-negative-drift_1d`
Measure: `measure.py`
