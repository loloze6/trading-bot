---
plan: 031-03.b1_wide-day-extends-up-run_1d
idea: 031-03.b1_wide-day-extends-up-run
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: forecast-weighted mean unusual 3-bar move (return minus coin's normal 3-bar drift), before costs: 0.011137; t of the weighted mean, cases on the same day pooled: 2.54096 (threshold: confirm: mean > 0 with t >= 2 and slope > 0; reject: mean < 0 with t <= -2; at least 30 distinct case days)
- Supporting check: OLS slope of unusual move on forecast > 0: 0.00109411, passed: True
- Counts: distinct case days: 564, cases: 890, active bars checked: 1201
- Decided by: the weighted mean unusual move is above 0 with t >= 2 and the slope is above 0
- Reading: the situation is recomputed from prices as today's high-low over the mean high-low of the last 20 bars of the same window (today included), side long; active bars in a window's first 19 bars, where the ratio cannot be computed, are left out of the agreement; a case is a bet (a rise of the long forecast of at least 2 points from its lowest level since the last bet, from 0 after a flat bar), only the first bet of each 3-bar grid cell of its window is kept and weighted by its forecast, cases without 3 further bars in the window are dropped, the normal drift is the coin's mean non-overlapping 3-bar return over all windows, and the day-pooled t uses per-day sums of weighted deviations with a D/(D-1) correction; with fewer than 30 case days the status is 'not observable'
- Size: unusual move +0.82 % (t 2.15, the cases of one day together: 564 days) per case over 3 bars, 0.084 of the coin's usual move (7.96 %); normal drift in its direction +0.36 %, total +1.18 %; 890 cases
Plan: `steps_cards/03_test_plan/night6_indecision_run/plans/031-03.b1_wide-day-extends-up-run_1d.md`
Record: `steps_cards/04_backtest/night6_indecision_run/backtests/031-03.b1_wide-day-extends-up-run_1d`
Measure: `measure.py`
