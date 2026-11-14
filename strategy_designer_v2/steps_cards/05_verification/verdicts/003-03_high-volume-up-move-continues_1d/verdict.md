---
plan: 003-03_high-volume-up-move-continues_1d
idea: 003-03_high-volume-up-move-continues
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: forecast-weighted mean next-bar excess return over buy-and-hold drift: 0.000456998; t of the forecast-weighted mean: 0.16545 (threshold: above 0 with t >= 2 confirms; below 0 with t <= -2 rejects; otherwise inconclusive)
- Supporting check: top-fifth minus bottom-fifth mean next-bar excess return (top fifth must be > 0): 0.013066, passed: True
- Counts: active bars: 151
- Decided by: The t-statistic lies between -2 and 2, which the plan calls inconclusive.
- Reading: Volume regime taken as volume >= the rolling 20-bar mean of volume including the current bar, computed inside each window so the first 19 rows of each window (no full 20-bar history) are left out of the situation check; the up move is the raw 'move' component > 0; the drift is the mean next-bar return over all bars of all windows; the t-statistic is the weighted mean divided by its forecast-weighted (sandwich) standard error; the top/bottom fifths are the floor(n/5) active bars with the highest/lowest forecast.
Plan: `steps_cards/03_test_plan/plans/003-03_high-volume-up-move-continues_1d.md`
Record: `steps_cards/04_backtest/backtests/003-03_high-volume-up-move-continues_1d`
Measure: `measure.py`
