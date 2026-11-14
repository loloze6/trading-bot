---
plan: 003-04_high-volume-down-move-continues_1d
idea: 003-04_high-volume-down-move-continues
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean demeaned per-bar gain (forecast/10 x next-bar return minus window mean): -0.00118999; t of the mean: -0.241528 (threshold: confirm if mean > 0 with t >= 2; reject if mean < 0 with t <= -2)
- Supporting check: larger-short half minus smaller-short half mean demeaned gain: -0.00754835, passed: False
- Counts: active bars: 148
- Decided by: The t-statistic lies between -2 and 2, so the result neither confirms nor rejects.
- Reading: The situation is a negative 1-day change on a bar whose volume is at or above the rolling 20-bar mean including that bar, checked only on active bars where 20 bars of volume exist in the window; the window's mean daily return is the mean of its close-to-close returns; position is forecast/10 as the plan says; the forecast split puts the n//2 most negative forecasts in the larger-short half and the n//2 least negative in the smaller-short half (middle bar dropped if n is odd); the 40-bar minimum counts active bars with a next-bar return.
Plan: `steps_cards/03_test_plan/plans/003-04_high-volume-down-move-continues_1d.md`
Record: `steps_cards/04_backtest/backtests/003-04_high-volume-down-move-continues_1d`
Measure: `measure.py`
