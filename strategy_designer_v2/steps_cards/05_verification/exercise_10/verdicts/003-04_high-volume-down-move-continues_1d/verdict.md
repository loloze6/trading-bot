---
plan: 003-04_high-volume-down-move-continues_1d
idea: 003-04_high-volume-down-move-continues
fit: adapted
status: inconclusive
---
Situation check: 1 of the active bars match the plan's situation and side
Evidence:
- Main measure: mean demeaned per-bar gain (forecast/10 x next-bar return minus window mean daily return): -0.00118999; t of the mean: -0.241528 (threshold: confirm if mean > 0 with t >= 2; reject if mean < 0 with t <= -2; else inconclusive; at least 40 active bars)
- Supporting check: larger-short half minus smaller-short half mean demeaned gain: -0.00754835, passed: False
- Counts: active bars pooled across windows: 148
- Decided by: The t-statistic lies between -2 and 2 with at least 40 active bars, so it neither confirms nor rejects.
- Reading: The 20-bar mean volume includes the current bar and is computed inside each window, so active bars in the first 19 rows of a window are left out of the situation check; the window's mean daily return is the mean of all its next-bar close-to-close returns; for the supporting check, active bars are sorted by forecast, and with an odd count the middle bar is dropped.
Plan: `steps_cards/03_test_plan/plans/003-04_high-volume-down-move-continues_1d.md`
Record: `steps_cards/04_backtest/backtests/003-04_high-volume-down-move-continues_1d`
Measure: `measure.py`
