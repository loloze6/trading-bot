---
plan: 025-01_downtrend-bounce-given-back_1d
idea: 025-01_downtrend-bounce-given-back
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean short-direction unusual 5-bar move of the short cases: 0.0047878; t of the mean: 1.80956 (threshold: positive with t >= 2 confirms; negative with t <= -2 rejects; between is inconclusive)
- Supporting check: larger-|forecast| half minus smaller half, mean unusual move: -0.0068697, passed: False
- Counts: cases: 1324, larger half: 662, smaller half: 662
- Decided by: The t of the mean short-direction unusual move lies between -2 and 2.
- Reading: A case is the first short bet (a fall of the forecast of at least 2 points from its lowest short level since the last bet, from 0 after a flat) in each 5-bar cell counted from each window's first row, cases without 5 bars left in the window are dropped, the drift is the coin's mean non-overlapping 5-bar return over all its windows, the larger half is |forecast| above the median (ties at the median go to the smaller half), and fewer than 30 cases is reported as not observable.
- Size: unusual move +0.48 % per case over 5 bars, 0.048 of the coin's usual move (10.60 %); normal drift in its direction -0.59 %, total -0.11 %; 1324 cases
Plan: `steps_cards/03_test_plan/night4_fallingbounce_run/plans/025-01_downtrend-bounce-given-back_1d.md`
Record: `steps_cards/04_backtest/night4_fallingbounce_run/backtests/025-01_downtrend-bounce-given-back_1d`
Measure: `measure.py`
