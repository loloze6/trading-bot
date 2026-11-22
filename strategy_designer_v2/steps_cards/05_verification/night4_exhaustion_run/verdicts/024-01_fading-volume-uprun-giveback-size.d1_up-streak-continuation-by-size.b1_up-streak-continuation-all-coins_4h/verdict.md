---
plan: 024-01_fading-volume-uprun-giveback-size.d1_up-streak-continuation-by-size.b1_up-streak-continuation-all-coins_4h
idea: 024-01_fading-volume-uprun-giveback-size.d1_up-streak-continuation-by-size.b1_up-streak-continuation-all-coins
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 18-bar move per case (long), all coins pooled: -0.000240891; t of the mean: -0.250066 (threshold: confirm t >= 2 with top-minus-bottom > 0; reject t <= -2; at least 100 cases)
- Supporting check: top-half minus bottom-half mean unusual move by forecast size: 0.00381238, passed: True
- Counts: cases: 12162, top_half_cases: 6081, bottom_half_cases: 6081
- Decided by: the t of the mean unusual move lies between -2 and 2
- Reading: cases are the first bet (long forecast rise >= 2 points from its low since the last bet) in each 18-bar grid cell from each window's first row, with the return dropped if t+18 leaves the window; top/bottom halves are the upper and lower n//2 cases by forecast at the signal bar (middle case dropped when n is odd); fewer than 100 cases is reported as not observable.
- Size: unusual move -0.02 % per case over 18 bars, -0.004 of the coin's usual move (9.29 %); normal drift in its direction +0.52 %, total +0.50 %; 12162 cases
Plan: `steps_cards/03_test_plan/night4_exhaustion_run/plans/024-01_fading-volume-uprun-giveback-size.d1_up-streak-continuation-by-size.b1_up-streak-continuation-all-coins_4h.md`
Record: `steps_cards/04_backtest/night4_exhaustion_run/backtests/024-01_fading-volume-uprun-giveback-size.d1_up-streak-continuation-by-size.b1_up-streak-continuation-all-coins_4h`
Measure: `measure.py`
