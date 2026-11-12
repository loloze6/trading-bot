---
plan: 003-03_high-volume-up-move-continues_1d
idea: 003-03_high-volume-up-move-continues
fit: adapted
status: inconclusive
---
Situation check: 1 of the active bars match the plan's situation and side
Evidence:
- Main measure: forecast-weighted mean next-bar excess return over buy-and-hold drift: 0.000456998; t of the forecast-weighted mean: 0.165394 (threshold: confirm if above 0 with t >= 2; reject if below 0 with t <= -2; else inconclusive)
- Supporting check: top-fifth minus bottom-fifth mean excess return (top must be > 0 and > bottom): 0.013066, passed: True
- Counts: active bars: 151
- Decided by: The t-statistic lies between -2 and 2 (or its sign disagrees with the mean), which the plan calls inconclusive.
- Reading: Situation = volume at or above its 20-bar mean (including the current bar, computed inside each window, active bars without 20 bars of volume history left out of the check) and a positive one-bar move from the move component, side long; the excess return is next-bar return minus the mean next-bar return over all bars of all windows pooled; the t-statistic is the ordinary t of the per-bar contributions forecast x excess / mean(forecast) over active bars (whose mean equals the forecast-weighted mean); the 60-bar minimum counts active bars with a next-bar return; top and bottom fifths are the floor(n/5) active bars with the highest and lowest forecast.
Plan: `steps_cards/03_test_plan/plans/003-03_high-volume-up-move-continues_1d.md`
Record: `steps_cards/04_backtest/backtests/003-03_high-volume-up-move-continues_1d`
Measure: `measure.py`
