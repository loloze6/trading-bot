---
plan: 003-03_high-volume-up-move-continues_1d
idea: 003-03_high-volume-up-move-continues
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: forecast-weighted mean next-bar return on active bars minus mean next-bar return over all bars: 0.000456998; t of the forecast-weighted mean: 0.16545 (threshold: confirm if forecast-weighted mean excess next-bar return > 0 with t >= 2; reject if < 0 with t <= -2; otherwise, or with fewer than 60 active bars, inconclusive)
- Supporting check: top-fifth minus bottom-fifth mean next-bar excess return (top must be > 0 and > bottom): 0.013066, passed: True
- Counts: active bars: 151, bars per fifth: 30
- Decided by: The t-statistic lies between -2 and 2, which the plan calls inconclusive.
- Reading: Volume regime taken as volume >= its 20-bar rolling mean computed within each window including the current bar (active bars without 20 bars of window history are left out of the agreement share); the drift is the mean next-bar return over all bars of all windows pooled; the t-statistic of the weighted mean uses the weighted standard error sqrt(n/(n-1) * sum(w^2 (x-m)^2)) / sum(w); the top and bottom fifths are the floor(n/5) active bars with the highest and lowest forecasts.
Plan: `steps_cards/03_test_plan/plans/003-03_high-volume-up-move-continues_1d.md`
Record: `steps_cards/04_backtest/backtests/003-03_high-volume-up-move-continues_1d`
Measure: `measure.py`
