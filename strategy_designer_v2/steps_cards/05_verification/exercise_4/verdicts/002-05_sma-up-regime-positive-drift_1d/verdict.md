---
plan: 002-05_sma-up-regime-positive-drift_1d
idea: 002-05_sma-up-regime-positive-drift
fit: adapted
status: inconclusive
---
Evidence:
- Main measure: in-stretch minus all-bar mean next-bar return (before costs): 0.000865053; Welch t (in-stretch vs all bars): 0.495162 (threshold: confirm if difference > 0 with one-sided t >= 2.0; reject if difference <= 0 or t <= -2.0)
- Supporting check: in-stretch up-day share minus all-bar up-day share: -0.000657268, passed: False
- Counts: in-stretch bars: 290, all bars: 724, distinct up-cross stretches: 5, in-stretch mean: 0.00113639, all-bar mean: 0.000271338, in-stretch up-day share: 0.475862, all-bar up-day share: 0.476519
- Decided by: Inconclusive: the in-stretch mean exceeds the all-bar mean but t 0.495 lies between -2.0 and 2.0.
- Reading: In-stretch means forecast > 0. With a 1-bar horizon, every bar with a next close in its window is a non-overlapping return, pooled over all coins and windows. The t is Welch's on in-stretch versus all-bar returns. Distinct up-cross stretches are runs of consecutive forecast > 0 bars inside each window, including a run that starts at a window's first row. Any non-positive mean difference rejects, as the reject rule states, so 'between -2.0 and 2.0' is inconclusive only when the difference is positive.
Plan: `steps_cards/03_test_plan/plans/002-05_sma-up-regime-positive-drift_1d.md`
Record: `steps_cards/04_backtest/backtests/002-05_sma-up-regime-positive-drift_1d`
Measure: `measure.py`
