---
plan: 003-04_high-volume-down-move-continues_1d
idea: 003-04_high-volume-down-move-continues
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean demeaned per-bar gain (forecast/10 x next-bar return minus window mean): -0.00118999; t of the mean: -0.241528 (threshold: confirm if mean > 0 with t >= 2; reject if mean < 0 with t <= -2; inconclusive otherwise or if fewer than 40 active bars)
- Supporting check: larger-short half minus smaller-short half mean demeaned gain: -0.00754835, passed: False
- Counts: active bars: 148
- Decided by: The t-statistic lies between -2 and 2, so the plan calls the result inconclusive.
- Reading: Volume test uses a 20-bar rolling mean that includes the current bar, computed within each window. Bars before 20 bars of history are left out of the situation check. The position is forecast/10 as the plan says. The window mean daily return is the mean of close-to-close changes in that window. Active bars are non-zero-forecast bars with a next bar in the same window. The halves come from a rank split by forecast, most negative first, and the middle bar is dropped when the count is odd.
Plan: `steps_cards/03_test_plan/plans/003-04_high-volume-down-move-continues_1d.md`
Record: `steps_cards/04_backtest/backtests/003-04_high-volume-down-move-continues_1d`
Measure: `measure.py`
