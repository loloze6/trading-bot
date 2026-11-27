---
plan: 067-01.b1.g1.b1.d1.g2_accelerating-month-slide-continues_1d
idea: 067-01.b1.g1.b1.d1.g2_accelerating-month-slide-continues
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 10-bar move per case, short direction: 0.00897604; t of the mean, cases of one day taken together: 1.17572 (threshold: confirm t >= 2 (day-clustered) with larger-minus-smaller half > 0; reject t <= -2)
- Supporting check: larger-half minus smaller-half mean unusual move (|forecast| median split): -0.0180589, passed: False
- Counts: cases: 705, distinct days: 422
- Decided by: The t of the mean unusual move lies between -2 and 2.
- Reading: A case is the first short bet (forecast falling >= 2 points from its lowest short level since the last bet) in each 10-bar grid cell of a window; the median split puts the top floor(n/2) cases by |forecast| (ties ordered by time and coin) in the larger half; the situation uses prices where the lookback fits in the window, else the recorded regime.
- Size: unusual move +0.90 % (t 1.18, the cases of one day together: 422 days) per case over 10 bars, 0.048 of the coin's usual move (16.82 %); normal drift in its direction -1.49 %, total -0.59 %; 705 cases
Plan: `steps_cards/03_test_plan/night9_chopmonth_run/plans/067-01.b1.g1.b1.d1.g2_accelerating-month-slide-continues_1d.md`
Record: `steps_cards/04_backtest/night9_chopmonth_run/backtests/067-01.b1.g1.b1.d1.g2_accelerating-month-slide-continues_1d`
Measure: `measure.py`
