---
plan: 024-01_fading-volume-uprun-giveback-size.d2_fading-volume-down-run-rebound_4h
idea: 024-01_fading-volume-uprun-giveback-size.d2_fading-volume-down-run-rebound
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 18-bar move per case (return minus coin's normal 18-bar drift): 2.73067e-06; t of the mean: 0.0022302 (threshold: confirm: mean > 0 with t >= 2 and size check difference > 0; reject: mean < 0 with t <= -2; fewer than 30 cases: not observable)
- Supporting check: mean unusual move above minus below median case forecast: 0.0107146, passed: True
- Counts: cases: 4537, cases above median: 2268, cases below median: 2268, active bars: 10507
- Decided by: t lies between -2 and 2 (or cannot be computed), so neither the confirm nor the reject rule is met (inconclusive rule).
- Reading: The situation is rebuilt as bar t closing below bar t-1 inside an unbroken down streak (capped at 180 bars) whose down bars' volumes have a negative least-squares slope (at least 2 bars), with the recorded raw streak loss > 0 where present; a case is the first bet (long forecast rise of >= 2 points from its lowest level since the last bet, from 0 after flat) in each 18-bar grid cell of a window, the drift is the coin's mean 18-bar return on the grid of all its windows, and cases at exactly the median forecast are left out of the size check.
- Size: unusual move +0.00 % per case over 18 bars, 0.000 of the coin's usual move (8.17 %); normal drift in its direction +0.41 %, total +0.41 %; 4537 cases
Plan: `steps_cards/03_test_plan/night4_exhaustion_run/plans/024-01_fading-volume-uprun-giveback-size.d2_fading-volume-down-run-rebound_4h.md`
Record: `steps_cards/04_backtest/night4_exhaustion_run/backtests/024-01_fading-volume-uprun-giveback-size.d2_fading-volume-down-run-rebound_4h`
Measure: `measure.py`
