---
plan: 037-01_choppy-swing-scaled-fall-continues_1d
idea: 037-01_choppy-swing-scaled-fall-continues
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean short-direction 5-bar unusual move (return minus drift) on grid cases with forecast < 0: 0.00653383; t of the mean, clustered by day: 0.935135 (threshold: confirm: mean > 0 with t >= 2 and larger-half minus smaller-half > 0; reject: mean < 0 with t <= -2; at least 30 cases on at least 30 distinct days)
- Supporting check: mean unusual move of larger-|forecast| half minus smaller half: 0.000379424, passed: True
- Counts: cases: 776, distinct days: 288
- Decided by: The main t is between -2 and 2.
- Reading: Choppy profile read as regime 'unknown'; cases are grid bars (0, 5, 10, ... of each window) with forecast < 0 and a full 5-bar forward return inside the window; drift is each coin's mean 5-bar grid return over all its windows; the clustered t uses day sums of deviations with a G/(G-1) correction; the larger half is |forecast| above the median, the smaller half at or below it.
- Size: unusual move +0.52 % (t 1.42, the cases of one day together: 777 days) per case over 5 bars, 0.036 of the coin's usual move (12.35 %); normal drift in its direction -0.80 %, total -0.28 %; 1444 cases
Plan: `steps_cards/03_test_plan/night7_rangefail_run/plans/037-01_choppy-swing-scaled-fall-continues_1d.md`
Record: `steps_cards/04_backtest/night7_rangefail_run/backtests/037-01_choppy-swing-scaled-fall-continues_1d`
Measure: `measure.py`
