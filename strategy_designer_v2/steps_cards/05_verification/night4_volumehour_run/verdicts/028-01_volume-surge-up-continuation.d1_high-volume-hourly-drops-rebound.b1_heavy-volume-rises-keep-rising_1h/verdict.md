---
plan: 028-01_volume-surge-up-continuation.d1_high-volume-hourly-drops-rebound.b1_heavy-volume-rises-keep-rising_1h
idea: 028-01_volume-surge-up-continuation.d1_high-volume-hourly-drops-rebound.b1_heavy-volume-rises-keep-rising
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 24-bar move after each case: 0.000655686; t of the mean: 1.0327 (threshold: confirm t >= 2, reject t <= -2, over at least 30 cases)
- Supporting check: top half minus bottom half mean unusual move (by forecast): 0.00101475, passed: True
- Counts: cases: 4448
- Decided by: The t of the mean unusual move lies between -2 and 2.
- Reading: A case is the first bet (forecast rise >= 2 from its lowest positive level since the last bet, from 0 after flat) in each 24-bar cell counted from each window's first row, the drift is the coin's mean non-overlapping 24-bar return over all its windows, and the halves are the lower and upper floor(n/2) cases by forecast (stable sort), the middle case dropped when n is odd.
- Size: unusual move +0.07 % per case over 24 bars, 0.016 of the coin's usual move (4.12 %); normal drift in its direction +0.15 %, total +0.21 %; 4448 cases
Plan: `steps_cards/03_test_plan/night4_volumehour_run/plans/028-01_volume-surge-up-continuation.d1_high-volume-hourly-drops-rebound.b1_heavy-volume-rises-keep-rising_1h.md`
Record: `steps_cards/04_backtest/night4_volumehour_run/backtests/028-01_volume-surge-up-continuation.d1_high-volume-hourly-drops-rebound.b1_heavy-volume-rises-keep-rising_1h`
Measure: `measure.py`
