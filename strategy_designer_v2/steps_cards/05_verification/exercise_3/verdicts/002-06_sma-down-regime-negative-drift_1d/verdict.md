---
plan: 002-06_sma-down-regime-negative-drift_1d
idea: 002-06_sma-down-regime-negative-drift
fit: adapted
status: inconclusive
---
Evidence:
- Main measure: in-state minus all-bars mean next-bar return: -0.000578031; stretch-clustered t: -0.312946 (threshold: difference <= -0.10% per day with stretch-clustered t <= -2)
- Supporting check: share of down bars in stretches minus share over all bars: -0.000439188, passed: False
- Counts: distinct down-cross stretches: 5, in-state bars pooled: 434, all bars pooled: 724
- Decided by: Inconclusive: the difference is negative but t > -2 or it is smaller than 0.10% per day.
- Reading: In-state bars are those with forecast < 0, a stretch is each contiguous run of such bars within one window (a run open at a window's start counts as one stretch), the t uses a cluster-robust standard error of the pooled in-state mean by stretch with the all-bars mean taken as fixed, a down bar is a negative next-bar return, and only the down-bar share enters the confirm rule while the equity checks are reported but not decisive.
Plan: `steps_cards/03_test_plan/plans/002-06_sma-down-regime-negative-drift_1d.md`
Record: `steps_cards/04_backtest/backtests/002-06_sma-down-regime-negative-drift_1d`
Measure: `measure.py`
