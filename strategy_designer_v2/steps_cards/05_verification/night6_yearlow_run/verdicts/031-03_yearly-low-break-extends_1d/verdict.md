---
plan: 031-03_yearly-low-break-extends_1d
idea: 031-03_yearly-low-break-extends
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean short-side unusual 10-bar move of short bets (vs coin's normal 10-bar drift): 0.000161299; t of the mean, cases of one day taken together: 0.00681091 (threshold: confirm: mean > 0 with day-clustered t >= 2; reject: mean < 0 with t <= -2)
- Supporting check: deeper half (|forecast| above median) mean unusual move >= shallower half mean (deeper minus shallower): -0.0322197, passed: False
- Counts: cases: 77, distinct days: 57
- Decided by: Inconclusive rule: the t of the mean short-side unusual move lies between -2 and 2.
- Reading: A case is the first short bet (forecast rising in size on the short side by at least 0.05 forecast points, the config's min_allocation_change, from its lowest size since the last bet) in each 10-bar grid cell counted from each window's first row, dropped if its 10-bar return leaves the window; the deeper half is |forecast| strictly above the median and the shallower half the rest; the plan's minimum of 30 cases on 20 days, when unmet, gives 'not observable'.
- Size: unusual move -5.50 % (t -1.96, the cases of one day together: 24 days) per case over 10 bars, -0.333 of the coin's usual move (14.49 %); normal drift in its direction -1.63 %, total -7.13 %; 33 cases
Plan: `steps_cards/03_test_plan/night6_yearlow_run/plans/031-03_yearly-low-break-extends_1d.md`
Record: `steps_cards/04_backtest/night6_yearlow_run/backtests/031-03_yearly-low-break-extends_1d`
Measure: `measure.py`
