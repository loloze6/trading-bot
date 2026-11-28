---
plan: 050-03_falling-calm-range-scaled-week-fall_1d
idea: 050-03_falling-calm-range-scaled-week-fall
fit: adapted
status: no effect
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean short-direction 3-bar unusual move on forecast<0 grid cases: -0.004176; t of the mean, cases of one day taken together: -0.983357 (threshold: confirm: mean > 0 with t >= 2 (and slope > 0); reject: mean < 0 with t <= -2)
- Supporting check: OLS slope of unusual move on |forecast|: 0.000621773, passed: True
- Counts: grid cases: 585, distinct days: 291
- Decided by: The main t lies between -2 and 2 (inconclusive rule). No effect (common/verdicts.md): t in the idea's direction -0.983 (below 1), 585 cases (30 needed).
- Reading: All coins and windows present in the record are used; the drift is each coin's mean 3-bar return on the non-overlapping grid of all its windows; the per-day t uses day-summed deviations with a D/(D-1) correction; the falling calm profile is read from the recorded regime 'unknown'.
- Size: unusual move +0.07 % (t 0.18, the cases of one day together: 410 days) per case over 3 bars, 0.004 of the coin's usual move (7.84 %); normal drift in its direction -0.29 %, total -0.22 %; 613 cases
- Effect check (common/verdicts.md): no effect: t in the idea's direction -0.983 (below 1), 585 cases (30 needed)
Plan: `steps_cards/03_test_plan/night10_fallcalmshort_run/plans/050-03_falling-calm-range-scaled-week-fall_1d.md`
Record: `steps_cards/04_backtest/night10_fallcalmshort_run/backtests/050-03_falling-calm-range-scaled-week-fall_1d`
Measure: `measure.py`
