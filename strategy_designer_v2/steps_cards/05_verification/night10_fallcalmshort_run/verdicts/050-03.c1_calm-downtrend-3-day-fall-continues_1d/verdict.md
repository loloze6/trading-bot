---
plan: 050-03.c1_calm-downtrend-3-day-fall-continues_1d
idea: 050-03.c1_calm-downtrend-3-day-fall-continues
fit: exact
status: no effect
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 3-bar move of short bets, short direction: 0.00194295; day-clustered t: 0.58162 (threshold: day-clustered t >= 2 confirms (with supporting difference > 0); t <= -2 rejects)
- Supporting check: large-|forecast| half mean unusual move minus small half: -0.001122, passed: False
- Counts: cases: 659, distinct days: 415
- Decided by: The main measure's t lies between -2 and 2. No effect (common/verdicts.md): t in the idea's direction +0.582 (below 1), 659 cases (30 needed).
- Reading: A case is the first short bet (forecast magnitude rising >= 2 points from its lowest level since the last bet, reset at flat) in each 3-bar grid cell of a window, with its 3-bar return inside the window; drift is the coin's mean non-overlapping 3-bar return over all its windows; the t clusters by UTC day with a G/(G-1) correction; the large half is |forecast| above the median, the small half at or below it; the 30-case minimum counts distinct days and, as a minimum count, gives 'not observable'.
- Size: unusual move +0.19 % (t 0.58, the cases of one day together: 415 days) per case over 3 bars, 0.017 of the coin's usual move (7.84 %); normal drift in its direction -0.28 %, total -0.09 %; 659 cases
- Effect check (common/verdicts.md): no effect: t in the idea's direction +0.582 (below 1), 659 cases (30 needed)
Plan: `steps_cards/03_test_plan/night10_fallcalmshort_run/plans/050-03.c1_calm-downtrend-3-day-fall-continues_1d.md`
Record: `steps_cards/04_backtest/night10_fallcalmshort_run/backtests/050-03.c1_calm-downtrend-3-day-fall-continues_1d`
Measure: `measure.py`
