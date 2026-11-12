---
plan: 002-05_sma-up-regime-positive-drift_1d
idea: 002-05_sma-up-regime-positive-drift
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: in-stretch minus out-of-stretch mean next-bar return: 0.00144308; Welch t: 0.698919 (threshold: confirm if difference > 0 with Welch t >= 2; reject if difference < 0 with t <= -2; |t| < 2 inconclusive; needs >=100 in-stretch bars, >=100 out-of-stretch bars, >=3 distinct up-cross stretches)
- Supporting check: share of up next-bars in-stretch minus out-of-stretch: -0.00109646, passed: False
- Counts: in-stretch bars: 290, out-of-stretch bars: 434, distinct up-cross stretches: 5
- Decided by: The Welch t has |t| < 2, which the plan rules inconclusive.
- Reading: In-stretch and out-of-stretch bars are those with forecast > 0 and forecast = 0 that have a next bar in the same window. A distinct up-cross stretch is each maximal run of raw SMA spread > 0 within a window, including a run already under way at the window's first bar.
Plan: `steps_cards/03_test_plan/plans/002-05_sma-up-regime-positive-drift_1d.md`
Record: `steps_cards/04_backtest/backtests/002-05_sma-up-regime-positive-drift_1d`
Measure: `measure.py`
