---
plan: 028-03_low-volume-up-fade.d2_volume-surge-rises-continue_1h
idea: 028-03_low-volume-up-fade.d2_volume-surge-rises-continue
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 6-bar move of long signals (return minus coin's normal 6-bar drift): 3.55825e-05; t of the mean: 0.143296 (threshold: confirm: mean > 0 with t >= 2 (and supporting check > 0); reject: mean < 0 with t <= -2)
- Supporting check: mean unusual move of upper forecast half minus lower half: 0.000205953, passed: True
- Counts: cases in total: 8827, upper half cases: 4413, lower half cases: 4414
- Decided by: The t of the mean unusual 6-bar move lies between -2 and 2.
- Reading: A case is the first bet bar (long forecast rising >= 2 points from its lowest level since the last bet, reset to 0 when flat) in each 6-bar grid cell counted from each window's first row, cases whose 6-bar return would leave the window are dropped, the drift is the coin's mean 6-bar return on the same grid over all windows, and the median split puts forecasts above the median in the upper half and those at or below it in the lower half.
- Size: unusual move +0.00 % per case over 6 bars, 0.000 of the coin's usual move (1.98 %); normal drift in its direction +0.03 %, total +0.04 %; 8827 cases
Plan: `steps_cards/03_test_plan/night4_volumehour_run/plans/028-03_low-volume-up-fade.d2_volume-surge-rises-continue_1h.md`
Record: `steps_cards/04_backtest/night4_volumehour_run/backtests/028-03_low-volume-up-fade.d2_volume-surge-rises-continue_1h`
Measure: `measure.py`
