---
plan: 002-05_sma-up-regime-positive-drift_1d
idea: 002-05_sma-up-regime-positive-drift
fit: adapted
status: inconclusive
---
Evidence:
- Main measure: in-stretch minus all-bar mean next-bar return (before costs): 0.000865053; Welch t (in-stretch vs all bars): 0.495162 (threshold: confirm if difference > 0 with one-sided t >= 2.0; reject if difference <= 0 or t <= -2.0; otherwise inconclusive)
- Supporting check: in-stretch minus all-bar up-day share: -0.000657268, passed: False
- Counts: in-stretch bars: 290, all bars: 724, distinct up-cross stretches: 5
- Decided by: Inconclusive: the in-stretch mean exceeds the all-bar mean but the t-statistic lies between -2.0 and 2.0.
- Reading: In-stretch bars are rows with forecast > 0, distinct up-cross stretches are contiguous runs of forecast > 0 counted per window (a run already open at a window's start counts), the t is Welch's two-sample t of in-stretch next-bar returns against all-bar next-bar returns on every bar (h=1), an up day is a next-bar return > 0, and a non-positive difference rejects even when t lies between -2.0 and 0.
Plan: `steps_cards/03_test_plan/plans/002-05_sma-up-regime-positive-drift_1d.md`
Record: `steps_cards/04_backtest/backtests/002-05_sma-up-regime-positive-drift_1d`
Measure: `measure.py`
