---
plan: 002-05_sma-up-regime-positive-drift_1d
idea: 002-05_sma-up-regime-positive-drift
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean next-bar return in-stretch minus out-of-stretch: 0.00144308; Welch t: 0.698919 (threshold: positive with t >= 2 confirms; negative with t <= -2 rejects; |t| < 2 inconclusive)
- Supporting check: share of up next-bars in-stretch minus out-of-stretch: -0.00109646, passed: False
- Counts: in-stretch bars: 290, out-of-stretch bars: 434, distinct up-cross stretches: 5
- Decided by: |t| < 2, which the plan calls inconclusive.
- Reading: Distinct up-cross stretches are counted as contiguous runs of positive raw SMA spread within each window, including a run already under way at the window's first bar, and the supporting check passes when the in-stretch up-share exceeds the out-of-stretch one.
Plan: `steps_cards/03_test_plan/plans/002-05_sma-up-regime-positive-drift_1d.md`
Record: `steps_cards/04_backtest/backtests/002-05_sma-up-regime-positive-drift_1d`
Measure: `measure.py`
