---
plan: 002-05_sma-up-regime-positive-drift_1d
idea: 002-05_sma-up-regime-positive-drift
fit: adapted
status: inconclusive
---
Situation check: 1 of the active bars match the plan's situation and side
Evidence:
- Main measure: in-stretch minus all-bar mean next-bar return (before costs): 0.000865053; Welch t (in-stretch vs all bars): 0.495162 (threshold: confirm: in-stretch mean > all-bar mean with one-sided t >= 2.0 and higher up-day share; reject: in-stretch mean <= all-bar mean or t <= -2.0; inconclusive: -2.0 < t < 2.0, fewer than 100 in-stretch bars or fewer than 3 up-cross stretches)
- Supporting check: in-stretch up-day share minus all-bar up-day share: -0.000657268, passed: False
- Counts: in-stretch bars: 290, all bars: 724, distinct up-cross stretches: 5
- Decided by: Inconclusive: the in-stretch mean exceeds the all-bar mean but the t-statistic lies between -2.0 and 2.0.
- Reading: Situation taken as the component's raw spread (last_history_value) above 0 with a positive forecast; in-stretch means forecast > 0, the all-bar group includes the in-stretch bars, an up day is a next-bar return above 0, and distinct up-cross stretches are counted as runs of consecutive forecast > 0 bars within each window (a run open at a window's first row counts as one).
Plan: `steps_cards/03_test_plan/plans/002-05_sma-up-regime-positive-drift_1d.md`
Record: `steps_cards/04_backtest/backtests/002-05_sma-up-regime-positive-drift_1d`
Measure: `measure.py`
