---
plan: 006-04_upside-squeeze-break-continuation.b1_wide-range-breakout-continuation_1d
idea: 006-04_upside-squeeze-break-continuation.b1_wide-range-breakout-continuation
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of slope of excess 10-bar return on width forecast: 0.391598; OLS slope t: 0.391598 (threshold: slope t >= 2 (with top-minus-bottom third > 0) confirms; slope t <= -2 rejects)
- Supporting check: top minus bottom third mean excess 10-bar return (Welch t 0.36): 0.00929638, passed: True
- Counts: non-overlapping breakout cases: 404
- Decided by: Slope t 0.39 lies between -2 and 2, which the plan calls inconclusive.
- Reading: Situation recomputed as close above the highest high of the prior 20 rows within each window, active bars in a window's first 20 rows (no in-window history) left out of the agreement; breakout cases are regime 'trending' bars taken greedily (first, then next at least 10 bars later) per window, cases without a 10-bar forward return inside the window dropped; the coin's mean 10-bar return is taken on the non-overlapping grid (positions 0,10,20,...) of all its windows; thirds are the floor(n/3) lowest and highest forecasts; the plan's 'fewer than 60 cases' is reported as 'not observable'.
Plan: `steps_cards/03_test_plan/night_006_run/plans/006-04_upside-squeeze-break-continuation.b1_wide-range-breakout-continuation_1d.md`
Record: `steps_cards/04_backtest/night_006_run/backtests/006-04_upside-squeeze-break-continuation.b1_wide-range-breakout-continuation_1d`
Measure: `measure.py`
