---
plan: 003-01_low-volume-up-move-reverts_1d
idea: 003-01_low-volume-up-move-reverts
fit: adapted
status: rejected
---
Situation check: 1 of the active bars match the plan's situation and side
Evidence:
- Main measure: position-weighted, drift-adjusted next-bar return of the short after thin up bars: -0.00205571; t of the mean: -0.758302 (threshold: above 0 with a t-stat of at least 2.0 (reject: 0 or less with t of 0 or below))
- Supporting check: largest third minus smallest third of |position|, mean drift-adjusted next-bar drop: 8.08454e-06, passed: True
- Counts: qualifying bars: 164, cases with non-zero position: 136, active bars: 165
- Decided by: The short earns 0 or less after the drift adjustment, with a t-stat of 0 or below.
- Reading: Up bar = one-bar close-to-close move > 0, and thin = volume < its 20-bar mean with the current bar included, computed inside each window. Bars without 20 bars of volume history are left out of the check. Qualifying cases are all thin up bars with a next-bar return. The main measure is the |position|-weighted mean of the short's drift-adjusted next-bar return, -(r - window mean). Its t is the ordinary t of the per-case gains alloc x (r - window mean) over cases with a non-zero position. Thirds are made by sorting the qualifying cases on |position| and splitting them with array_split.
Plan: `steps_cards/03_test_plan/plans/003-01_low-volume-up-move-reverts_1d.md`
Record: `steps_cards/04_backtest/backtests/003-01_low-volume-up-move-reverts_1d`
Measure: `measure.py`
