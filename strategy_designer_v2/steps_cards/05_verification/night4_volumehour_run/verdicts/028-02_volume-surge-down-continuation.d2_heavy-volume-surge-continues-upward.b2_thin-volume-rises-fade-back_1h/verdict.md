---
plan: 028-02_volume-surge-down-continuation.d2_heavy-volume-surge-continues-upward.b2_thin-volume-rises-fade-back_1h
idea: 028-02_volume-surge-down-continuation.d2_heavy-volume-surge-continues-upward.b2_thin-volume-rises-fade-back
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean short-side unusual 4-bar return of short bets, pooled over coins: 4.74087e-05; t of the mean: 0.347777 (threshold: confirm: mean > 0 with t >= 2 and slope > 0; reject: mean < 0 with t <= -2; fewer than 100 cases: inconclusive/not observable)
- Supporting check: OLS slope of short-side unusual return on |forecast|: 7.23718e-06, passed: True
- Counts: cases pooled over coins and windows: 11108
- Decided by: The t of the mean lies between -2 and 2, which the plan calls inconclusive.
- Reading: Situation = raw rise component > 0 (or the hour's close-to-close return > 0 where unrecorded) and volume over its 720-bar mean (current included, inside the window) <= 1, using the recorded regime on the first 719 bars of a window where that mean cannot be computed; a case is the first bar of each 4-bar grid cell (positions from the window's first row) where the short forecast's size rises by >= 2 from its smallest size since the last bet (from 0 after flat or a side change); drift is the coin's mean non-overlapping 4-bar return over all its windows; the minimum of 100 pooled cases maps to 'not observable'.
- Size: unusual move +0.00 % per case over 4 bars, 0.003 of the coin's usual move (1.62 %); normal drift in its direction -0.02 %, total -0.02 %; 11108 cases
Plan: `steps_cards/03_test_plan/night4_volumehour_run/plans/028-02_volume-surge-down-continuation.d2_heavy-volume-surge-continues-upward.b2_thin-volume-rises-fade-back_1h.md`
Record: `steps_cards/04_backtest/night4_volumehour_run/backtests/028-02_volume-surge-down-continuation.d2_heavy-volume-surge-continues-upward.b2_thin-volume-rises-fade-back_1h`
Measure: `measure.py`
