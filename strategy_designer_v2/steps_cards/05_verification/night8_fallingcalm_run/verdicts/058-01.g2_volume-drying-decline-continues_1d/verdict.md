---
plan: 058-01.g2_volume-drying-decline-continues_1d
idea: 058-01.g2_volume-drying-decline-continues
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 5-bar move, short direction: 0.0111135; t of the mean, cases of one day together: 2.00176 (threshold: confirm: mean > 0 with t >= 2 and check > 0; reject: t <= -2)
- Supporting check: larger-|forecast| half minus smaller half, mean unusual move: 0.0111164, passed: True
- Counts: distinct case-days: 270, cases: 332
- Decided by: The mean unusual short move is above 0 with t >= 2 and the larger-forecast half beats the smaller half.
- Reading: Situation = regime 'mean_reversion' (the detector's fall30<0 with the falling-calm profile vetoes passed) and the 30-day return from prices <0 where computable in the window, and the raw vol_dryup log ratio <0 (recomputed from volume where not recorded), on the short side; a case is the first short bet in each 5-bar grid cell counted from each window's first row, with cases lacking 5 bars ahead in the window dropped; the day-clustered t uses the per-day summed deviations with a G/(G-1) correction; the larger half is |forecast| strictly above the median and the smaller half at or below it; the plan's 'at least 30 distinct case-days' is applied as the minimum count giving 'not observable'.
- Size: unusual move +1.11 % (t 2.01, the cases of one day together: 270 days) per case over 5 bars, 0.107 of the coin's usual move (10.60 %); normal drift in its direction -0.65 %, total +0.46 %; 332 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.008 on the check folds against +0.01111 on every fold
Plan: `steps_cards/03_test_plan/night8_fallingcalm_run/plans/058-01.g2_volume-drying-decline-continues_1d.md`
Record: `steps_cards/04_backtest/night8_fallingcalm_run/backtests/058-01.g2_volume-drying-decline-continues_1d`
Measure: `measure.py`
