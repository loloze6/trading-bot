---
plan: 028-02_volume-surge-down-continuation.d1_heavy-volume-plunge-rebounds_1h
idea: 028-02_volume-surge-down-continuation.d1_heavy-volume-plunge-rebounds
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 4-bar move after heavy-volume plunge bets (long): 0.000423007; t of the mean: 2.51814 (threshold: confirm t >= 2 over >= 30 cases with slope > 0; reject t <= -2 over >= 30 cases)
- Supporting check: OLS slope of unusual move on signal-bar forecast: 2.46602e-05, passed: True
- Counts: cases: 13013
- Decided by: The mean unusual move has t >= 2 over at least 30 cases and the slope on the forecast is above 0.
- Reading: Situation = bars whose raw volume-weighted scaled return is negative (graded fall), side long; a case is the first long bet (forecast rise >= 2 points from its lowest level since the last bet, reset to 0 after a flat bar) in each 4-bar grid cell counted from each window's first row, with its 4-bar return kept only when it stays inside the window, and the normal drift is each coin's mean non-overlapping 4-bar return over all its windows.
- Size: unusual move +0.04 % per case over 4 bars, 0.026 of the coin's usual move (1.62 %); normal drift in its direction +0.02 %, total +0.07 %; 13013 cases
Plan: `steps_cards/03_test_plan/night4_volumehour_run/plans/028-02_volume-surge-down-continuation.d1_heavy-volume-plunge-rebounds_1h.md`
Record: `steps_cards/04_backtest/night4_volumehour_run/backtests/028-02_volume-surge-down-continuation.d1_heavy-volume-plunge-rebounds_1h`
Measure: `measure.py`
