---
plan: 002-05_sma-up-regime-positive-drift_1d
idea: 002-05_sma-up-regime-positive-drift
fit: adapted
status: inconclusive
---
Evidence:
- Main measure: in-stretch minus all-bar mean next-bar return (before costs): 0.000865053; Welch t (in-stretch minus all bars): 0.495162 (threshold: confirm if difference > 0 with t >= 2.0; reject if difference <= 0 or t <= -2.0; inconclusive if t is between -2.0 and 2.0)
- Supporting check: in-stretch up-day share minus all-bar up-day share: -0.000657268, passed: False
- Counts: in-stretch bars: 290, distinct up-cross stretches: 5, all bars: 724
- Decided by: Inconclusive: the in-stretch mean exceeds the all-bar mean, but the t-statistic lies between -2.0 and 2.0.
- Reading: In-stretch bars are the bars with forecast > 0. Distinct up-cross stretches are contiguous runs of forecast > 0 within each window, counting a run that is already on at a window's first row. Every bar's next-bar return is used, since h = 1 makes every bar non-overlapping. The test is Welch's t of in-stretch returns against all-bar returns. An up day is a next-bar return > 0.
Plan: `steps_cards/03_test_plan/plans/002-05_sma-up-regime-positive-drift_1d.md`
Record: `steps_cards/04_backtest/backtests/002-05_sma-up-regime-positive-drift_1d`
Measure: `measure.py`
