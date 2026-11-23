---
plan: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.d1_extreme-surge-low-close-rise.d2_close-at-low-grades-surge_1d
idea: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.d1_extreme-surge-low-close-rise.d2_close-at-low-grades-surge
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean excess next-day return over bet cases (return minus coin mean daily return): 0.00223264; ordinary t of the mean: 2.99077 (threshold: confirm: positive with t >= 2 and timing > 0; reject: negative with t <= -2)
- Supporting check: timing part of the book's mean daily return: 0.000310379, passed: True
- Counts: cases: 4705
- Decided by: Mean excess next-day return is positive with t >= 2 and the timing part is above 0.
- Reading: Situation bars are those with a positive raw component value on the long side; cases are the holding-period bets (forecast rise >= 2 on the long side from its lowest level since the last bet), every bar being a 1-bar grid cell, excluding a window's last bar; the plan's 'fewer than 100 cases' is treated as the minimum count giving 'not observable'.
- Size: unusual move +0.22 % per case over 1 bars, 0.046 of the coin's usual move (4.78 %); normal drift in its direction +0.12 %, total +0.34 %; 4705 cases
Plan: `steps_cards/03_test_plan/brief_absorption_run/plans/030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.d1_extreme-surge-low-close-rise.d2_close-at-low-grades-surge_1d.md`
Record: `steps_cards/04_backtest/brief_absorption_run/backtests/030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.d1_extreme-surge-low-close-rise.d2_close-at-low-grades-surge_1d`
Measure: `measure.py`
