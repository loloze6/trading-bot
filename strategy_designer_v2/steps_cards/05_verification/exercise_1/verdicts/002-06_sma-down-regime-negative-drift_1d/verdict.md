---
plan: 002-06_sma-down-regime-negative-drift_1d
idea: 002-06_sma-down-regime-negative-drift
fit: adapted
status: inconclusive
---
Evidence:
- Main measure: in-state (forecast<0) mean next-bar return minus all-bars mean, pooled: -0.000578031 (threshold: <= -0.10% per day with stretch-clustered t <= -2 to confirm; >= 0 to reject)
- Supporting check: down-bar share in stretches minus down-bar share over all bars: -0.000439188, passed: False
- Cases: 5
- Decided by: Inconclusive: the difference is negative but t > -2, or it is smaller than 0.10% per day, or the down-bar share condition of the confirm rule is not met.
- Reading: A stretch is a run of consecutive bars with forecast < 0 inside one window, cases counts stretches holding at least one in-state bar with a next-bar return, the clustered t treats the all-bars mean as fixed with a G/(G-1) correction, a down bar is a negative next-bar return, and the equity-curve parts of the supporting check are reported but only the down-share condition named in the confirm rule enters the decision.
Plan: `steps_cards/03_test_plan/plans/002-06_sma-down-regime-negative-drift_1d.md`
Record: `steps_cards/04_backtest/backtests/002-06_sma-down-regime-negative-drift_1d`
Measure: `measure.py`
