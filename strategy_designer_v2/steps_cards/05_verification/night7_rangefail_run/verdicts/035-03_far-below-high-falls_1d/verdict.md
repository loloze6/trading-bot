---
plan: 035-03_far-below-high-falls_1d
idea: 035-03_far-below-high-falls
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual move over 5 bars of short cases (day-clustered t): 0.00683512; t of the mean, clustered by day: 1.98869 (threshold: confirm: mean > 0 with t >= 2 and supporting check passed; reject: mean < 0 with t <= -2)
- Supporting check: mean unusual move deeper half minus shallower half (median depth split): 0.000942463, passed: True
- Counts: distinct case days: 1149, cases: 3666, active bars: 20969
- Decided by: The t of the mean unusual move lies between -2 and 2, meeting neither confirm nor reject (inconclusive rule).
- Reading: A case is the first short bet (forecast magnitude rising by at least 2 points from its lowest level since the last bet, from 0 after a flat or side change) in each 5-bar grid cell of a window, its return taken from that bar's close over 5 bars inside the window; the normal drift is the coin's mean 5-bar return on the grid over all its windows; the day-clustered t uses per-day summed deviations with a G/(G-1) correction; the deeper half is depth at or below the median, the shallower half above it; fewer than 30 case days is reported as not observable.
- Size: unusual move +0.68 % (t 1.99, the cases of one day together: 1149 days) per case over 5 bars, 0.049 of the coin's usual move (12.35 %); normal drift in its direction -0.81 %, total -0.13 %; 3666 cases
Plan: `steps_cards/03_test_plan/night7_rangefail_run/plans/035-03_far-below-high-falls_1d.md`
Record: `steps_cards/04_backtest/night7_rangefail_run/backtests/035-03_far-below-high-falls_1d`
Measure: `measure.py`
