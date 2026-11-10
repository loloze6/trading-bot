---
plan: 002-06_sma-down-regime-negative-drift_1d
idea: 002-06_sma-down-regime-negative-drift
fit: adapted
status: inconclusive
---
Evidence:
- Main measure: in-state mean next-bar return minus all-bars mean: -0.000578031; stretch-clustered t: -0.312946 (threshold: difference <= -0.10% per day with stretch-clustered t <= -2)
- Supporting check: down-bar share in stretches minus down-bar share over all bars: -0.000439188, passed: False
- Counts: distinct down-cross stretches: 5, in-state bars pooled: 434, all bars pooled: 724, windows: 6
- Decided by: Inconclusive: the difference is negative but t > -2, or smaller than 0.10% per day, or the down-bar share inside stretches is not higher than over all bars.
- Reading: Stretches are contiguous runs of forecast < 0 inside one window (a run cut by a window edge counts as its own stretch), the t is the pooled difference over a cluster-robust standard error of the in-state mean with stretches as clusters (K/(K-1) correction, all-bars mean treated as fixed), a down bar is a negative next-bar return, and the supporting check's pass is the down-share comparison the confirm rule names (the equity-curve part is not used in the decision).
Plan: `steps_cards/03_test_plan/plans/002-06_sma-down-regime-negative-drift_1d.md`
Record: `steps_cards/04_backtest/backtests/002-06_sma-down-regime-negative-drift_1d`
Measure: `measure.py`
