---
plan: 003-03_high-volume-up-move-continues_1d
idea: 003-03_high-volume-up-move-continues
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: forecast-weighted mean next-bar return on active bars minus buy-and-hold drift: 0.000456998; t of the forecast-weighted mean: 0.16545 (threshold: above 0 with t >= 2 confirms; below 0 with t <= -2 rejects; otherwise inconclusive)
- Supporting check: top-fifth minus bottom-fifth mean excess next-bar return (top must be > 0 and > bottom): 0.013066, passed: True
- Counts: active bars: 151
- Decided by: The t-statistic lies between -2 and 2, which the plan calls inconclusive.
- Reading: The volume regime is computed as volume >= its 20-bar rolling mean (current bar included) within each window, with the window's first 19 bars left out of the situation check; the drift is the mean next-bar return over all bars of all windows pooled; the t-statistic of the forecast-weighted mean uses the weighted standard error sqrt(n/(n-1) * sum(w^2 (x-m)^2)) / sum(w); the top and bottom fifths are the floor(n/5) active bars with the highest and lowest forecast after a stable sort.
Plan: `steps_cards/03_test_plan/plans/003-03_high-volume-up-move-continues_1d.md`
Record: `steps_cards/04_backtest/backtests/003-03_high-volume-up-move-continues_1d`
Measure: `measure.py`
