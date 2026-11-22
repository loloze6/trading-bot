---
plan: 024-01_fading-volume-uprun-giveback-size.g3_volume-surge-precedes-rise_4h
idea: 024-01_fading-volume-uprun-giveback-size.g3_volume-surge-precedes-rise
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean excess 18-bar return of bet cases (return minus coin's normal 18-bar drift): 0.00213395; ordinary t of the mean: 1.62527 (threshold: confirm: mean > 0 with t >= 2 over >= 30 cases and Spearman > 0; reject: mean < 0 with t <= -2 over >= 30 cases)
- Supporting check: Spearman(forecast at signal bar, excess 18-bar return) > 0: -0.0143911, passed: False
- Counts: cases: 4437, active bars: 34339
- Decided by: t is between -2 and 2 (or undefined), which the plan calls inconclusive.
- Reading: Situation is the raw component (volume ratio minus 1) above 0 with a positive forecast; a case is the first bar of each non-overlapping 18-bar grid cell (from each window's first row) where the forecast rises on its side by >= 2 points from its lowest level since its last bet (from 0 after flat or a side change), and the excess is the raw 18-bar return minus the coin's mean non-overlapping 18-bar return over all its windows, not sign-adjusted; the plan's 'fewer than 30 cases' is treated as the minimum count giving 'not observable'.
- Size: unusual move +0.21 % per case over 18 bars, 0.024 of the coin's usual move (8.17 %); normal drift in its direction +0.41 %, total +0.62 %; 4437 cases
Plan: `steps_cards/03_test_plan/night4_exhaustion_run/plans/024-01_fading-volume-uprun-giveback-size.g3_volume-surge-precedes-rise_4h.md`
Record: `steps_cards/04_backtest/night4_exhaustion_run/backtests/024-01_fading-volume-uprun-giveback-size.g3_volume-surge-precedes-rise_4h`
Measure: `measure.py`
