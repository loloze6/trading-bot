---
plan: 028-03_low-volume-up-fade.d2_volume-surge-rises-continue.b1_volume-surge-rises-continue-a-day_1h
idea: 028-03_low-volume-up-fade.d2_volume-surge-rises-continue.b1_volume-surge-rises-continue-a-day
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean strength of the 24-bar unusual move of bets: 0.0155796; t of the mean: 1.02154 (threshold: confirm: positive with t >= 2 over >= 30 cases; reject: negative with t <= -2 over >= 30 cases)
- Supporting check: mean unusual move, forecast above case median minus at or below: 0.00101475, passed: True
- Counts: cases: 4448, cases above median forecast: 2224, cases at or below median forecast: 2224, active bars: 68136
- Decided by: t between -2 and 2 is inconclusive.
- Reading: a case is the first bet (forecast rise >= 2 from its lowest long level since the last bet, reset to 0 after a flat) in each 24-bar grid cell counted from each window's first row, dropped when its 24-bar return leaves the window; drift and usual move are the mean and std of the coin's grid 24-bar returns over all windows; the confirm/reject t is the t of the mean strength (the plan's main measure), and the supporting check splits cases by the signal bar's forecast against the cases' median; situation = positive raw component (rising hour) on the long side.
- Size: unusual move +0.07 % per case over 24 bars, 0.016 of the coin's usual move (4.12 %); normal drift in its direction +0.15 %, total +0.21 %; 4448 cases
Plan: `steps_cards/03_test_plan/night4_volumehour_run/plans/028-03_low-volume-up-fade.d2_volume-surge-rises-continue.b1_volume-surge-rises-continue-a-day_1h.md`
Record: `steps_cards/04_backtest/night4_volumehour_run/backtests/028-03_low-volume-up-fade.d2_volume-surge-rises-continue.b1_volume-surge-rises-continue-a-day_1h`
Measure: `measure.py`
