---
plan: 002-05_sma-up-regime-positive-drift_1d
idea: 002-05_sma-up-regime-positive-drift
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: in-stretch minus out-of-stretch mean next-bar return: 0.00144308; Welch t: 0.698919 (threshold: confirm if in-minus-out mean next-bar return > 0 with Welch t >= 2; reject if < 0 with t <= -2; |t| < 2 inconclusive; needs >= 100 in-stretch bars, >= 100 out-of-stretch bars and >= 3 distinct up-cross stretches)
- Supporting check: share of up next-bars in-stretch minus out-of-stretch: -0.00109646, passed: False
- Counts: in-stretch bars: 290, out-of-stretch bars: 434, distinct up-cross stretches: 5
- Decided by: Welch t = 0.70 has |t| < 2, which the plan calls inconclusive.
- Reading: In-stretch bars are rows with forecast > 0 and out-of-stretch rows with forecast == 0; the situation is the raw 50/200 SMA spread > 0 on the long side; distinct up-cross stretches are counted as contiguous runs of forecast > 0 inside each window (a run cut by a window boundary counts in each window); the supporting check passes when the up-share difference is > 0; a missing minimum count gives 'not observable' as the task prescribes.
Plan: `steps_cards/03_test_plan/plans/002-05_sma-up-regime-positive-drift_1d.md`
Record: `steps_cards/04_backtest/backtests/002-05_sma-up-regime-positive-drift_1d`
Measure: `measure.py`
