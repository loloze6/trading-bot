---
plan: 002-05_sma-up-regime-positive-drift_1d
idea: 002-05_sma-up-regime-positive-drift
fit: adapted
status: inconclusive
---
Evidence:
- Main measure: in-stretch minus all-bar mean next-bar return (before costs): 0.000865053; Welch t (in-stretch minus all bars): 0.495162 (threshold: confirm if the difference is > 0 with t >= 2.0; reject if the difference is <= 0 (or t <= -2.0); otherwise inconclusive)
- Supporting check: in-stretch up-day share minus all-bar up-day share: -0.000657268, passed: False
- Counts: in-stretch bars: 290, distinct up-cross stretches: 5, all bars: 724
- Decided by: Inconclusive: the in-stretch mean exceeds the all-bar mean but the t-statistic lies between -2.0 and 2.0.
- Reading: In-stretch means forecast > 0. With a 1-bar horizon every bar is on the non-overlapping grid. The 'all bars' group includes the in-stretch bars, and the two groups are compared with Welch t. A distinct up-cross stretch is a maximal run of consecutive forecast > 0 bars within one window, including a run already under way at the window's start. An up day is a next-bar return > 0. A difference at or below 0 rejects even when t lies between -2 and 2, because the plan's reject rule says so explicitly.
Plan: `steps_cards/03_test_plan/plans/002-05_sma-up-regime-positive-drift_1d.md`
Record: `steps_cards/04_backtest/backtests/002-05_sma-up-regime-positive-drift_1d`
Measure: `measure.py`
