---
plan: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.d1_extreme-surge-low-close-rise.d1_absorbed-selling-two-day-rise_1d
idea: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.d1_extreme-surge-low-close-rise.d1_absorbed-selling-two-day-rise
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of excess 2-day return on forecast, pooled: 0.000335298; OLS slope t: 6.31707 (threshold: confirm: slope > 0 with t >= 2; reject: slope < 0 with t <= -2)
- Supporting check: top-fifth mean excess 2-day return > 0: 0.00977258, passed: True
- Counts: grid cells pooled: 8650, top fifth cells: 1730
- Decided by: The slope is positive with t >= 2 and the top-fifth mean excess return is above 0.
- Reading: The situation for this graded, long-only idea is taken as every bar where the raw close-near-low times volume-multiple value is positive (recomputed from prices where unrecorded); the coin's mean 2-day return is taken over its grid cells in all windows; the forecast for the regression and the ranking is post_pipeline_value; the top fifth is the floor(n/5) highest cells (stable sort); and the plan's minimum counts, when not reached, give 'not observable' per the workflow.
- Size: unusual move +0.09 % per case over 2 bars, 0.015 of the coin's usual move (6.58 %); normal drift in its direction +0.23 %, total +0.33 %; 5664 cases
Plan: `steps_cards/03_test_plan/brief_absorption_run/plans/030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.d1_extreme-surge-low-close-rise.d1_absorbed-selling-two-day-rise_1d.md`
Record: `steps_cards/04_backtest/brief_absorption_run/backtests/030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.d1_extreme-surge-low-close-rise.d1_absorbed-selling-two-day-rise_1d`
Measure: `measure.py`
