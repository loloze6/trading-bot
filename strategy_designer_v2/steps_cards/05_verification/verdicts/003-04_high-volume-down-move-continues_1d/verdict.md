---
plan: 003-04_high-volume-down-move-continues_1d
idea: 003-04_high-volume-down-move-continues
fit: adapted
status: inconclusive
---
Situation check: 1 of the active bars match the plan's situation and side
Evidence:
- Main measure: mean demeaned per-bar gain of (forecast/10) x next-bar return: -0.00118999; t of the mean: -0.241528 (threshold: confirm if mean > 0 with t >= 2; reject if mean < 0 with t <= -2; otherwise, or fewer than 40 active bars, inconclusive)
- Supporting check: mean gain larger-short half minus smaller-short half: -0.00754835, passed: False
- Counts: active bars pooled across windows: 148
- Decided by: The t-statistic lies between -2 and 2, so the result is neither confirmed nor rejected.
- Reading: The position is forecast/10 as the plan states, and the window's mean daily return is the mean of all next-bar close-to-close returns in that window. The 20-bar mean volume includes the current bar and is computed within each window. For the supporting check, active bars are sorted by forecast; the floor(n/2) most negative bars form the larger-short half and the floor(n/2) least negative bars form the smaller-short half, and the middle bar is dropped when n is odd.
Plan: `steps_cards/03_test_plan/plans/003-04_high-volume-down-move-continues_1d.md`
Record: `steps_cards/04_backtest/backtests/003-04_high-volume-down-move-continues_1d`
Measure: `measure.py`
