---
plan: 024-01_fading-volume-uprun-giveback-size.g3_volume-surge-precedes-rise.b1_volume-surge-more-coins_4h
idea: 024-01_fading-volume-uprun-giveback-size.g3_volume-surge-precedes-rise.b1_volume-surge-more-coins
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: forecast-weighted mean excess 18-bar return of long bets: 0.00200335; t of the weighted mean: 1.80809 (threshold: above 0 with t >= 2 to confirm; below 0 with t <= -2 to reject)
- Supporting check: upper-half minus lower-half mean excess return (split at median forecast): None, passed: False
- Counts: cases: 10265, active bars: 72934, upper half cases: 0, lower half cases: 10265
- Decided by: The t of the forecast-weighted mean excess return lies between -2 and 2, which the plan calls inconclusive.
- Reading: Situation read as the volume ratio above 1 (raw component value > 0) on the long side; bets detected per window from 0 at its start, first bet per 18-bar grid cell (counted from the window's first row) taken as the case; t of the weighted mean is the ordinary t of f*x/mean(f); the median split puts forecasts above the median in the upper half; fewer than 100 cases gives 'not observable' per the workflow.
- Size: unusual move +0.14 % per case over 18 bars, 0.013 of the coin's usual move (9.29 %); normal drift in its direction +0.52 %, total +0.66 %; 10265 cases
Plan: `steps_cards/03_test_plan/night4_exhaustion_run/plans/024-01_fading-volume-uprun-giveback-size.g3_volume-surge-precedes-rise.b1_volume-surge-more-coins_4h.md`
Record: `steps_cards/04_backtest/night4_exhaustion_run/backtests/024-01_fading-volume-uprun-giveback-size.g3_volume-surge-precedes-rise.b1_volume-surge-more-coins_4h`
Measure: `measure.py`
