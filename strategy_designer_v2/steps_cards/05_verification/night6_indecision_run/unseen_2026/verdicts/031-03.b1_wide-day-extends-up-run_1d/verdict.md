---
plan: 031-03.b1_wide-day-extends-up-run_1d
idea: 031-03.b1_wide-day-extends-up-run
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: forecast-weighted mean unusual 3-bar move (return minus coin's normal 3-bar drift), before costs: 0.00606643; t of the weighted mean, cases on the same day pooled: 0.465707 (threshold: confirm: mean > 0 with t >= 2 and slope > 0; reject: mean < 0 with t <= -2; at least 30 distinct case days)
- Supporting check: OLS slope of unusual move on forecast > 0: 0.00154027, passed: True
- Counts: distinct case days: 64, cases: 98, active bars checked: 110
- Decided by: t lies between -2 and 2
- Reading: the situation is recomputed from prices as today's high-low over the mean high-low of the last 20 bars of the same window (today included), side long; active bars in a window's first 19 bars, where the ratio cannot be computed, are left out of the agreement; a case is a bet (a rise of the long forecast of at least 2 points from its lowest level since the last bet, from 0 after a flat bar), only the first bet of each 3-bar grid cell of its window is kept and weighted by its forecast, cases without 3 further bars in the window are dropped, the normal drift is the coin's mean non-overlapping 3-bar return over all windows, and the day-pooled t uses per-day sums of weighted deviations with a D/(D-1) correction; with fewer than 30 case days the status is 'not observable'
- Size: unusual move +0.22 % (t 0.18, the cases of one day together: 64 days) per case over 3 bars, 0.083 of the coin's usual move (5.48 %); normal drift in its direction +0.09 %, total +0.31 %; 98 cases
Plan: `steps_cards/03_test_plan/night6_indecision_run/plans/031-03.b1_wide-day-extends-up-run_1d.md`
Record: `steps_cards/04_backtest/night6_indecision_run/unseen_2026/backtests/031-03.b1_wide-day-extends-up-run_1d`
Measure: `measure.py`
