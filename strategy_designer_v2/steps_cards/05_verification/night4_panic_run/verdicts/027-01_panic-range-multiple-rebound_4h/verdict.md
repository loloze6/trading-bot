---
plan: 027-01_panic-range-multiple-rebound_4h
idea: 027-01_panic-range-multiple-rebound
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 84-bar move of long cases (return minus coin's normal drift): -0.00126051; t of the mean: -0.208766 (threshold: confirm: mean > 0 with t >= 2 and upper-minus-lower gradient > 0; reject: mean < 0 with t <= -2)
- Supporting check: upper-minus-lower half (median forecast at entry) mean unusual move, Welch t (Welch t 1.052): 0.0127031, passed: True
- Counts: cases over all coins and windows: 1144, upper half cases: 572, lower half cases: 572
- Decided by: the t of the mean unusual move is between -2 and 2, which the plan calls inconclusive
- Reading: a case is the first long bet (forecast rise >= 2 from its lowest positive level since the last bet, from 0 after a flat) in each 84-bar grid cell from each window's first row, kept only if its 84-bar return stays inside the window; the median split sorts cases by entry forecast (ties in case order) into equal lower and upper halves, dropping the middle case when odd; the plan's fewer-than-30-cases rule is reported as not observable.
- Size: unusual move -0.13 % per case over 84 bars, -0.007 of the coin's usual move (17.66 %); normal drift in its direction +2.11 %, total +1.98 %; 1144 cases
Plan: `steps_cards/03_test_plan/night4_panic_run/plans/027-01_panic-range-multiple-rebound_4h.md`
Record: `steps_cards/04_backtest/night4_panic_run/backtests/027-01_panic-range-multiple-rebound_4h`
Measure: `measure.py`
