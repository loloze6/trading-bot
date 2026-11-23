---
plan: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.d2_absorption-in-volatile-markets.d1_absorbed-selling-on-down-days_1d
idea: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.d2_absorption-in-volatile-markets.d1_absorbed-selling-on-down-days
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean timing gain on bars in a position (position x (next-day return - coin mean daily return)): 0.00140091; ordinary t of the mean: 4.63559 (threshold: t >= 2 to confirm (with supporting check), t <= -2 to reject, over at least 300 bars in a position)
- Supporting check: top third minus bottom third by forecast of next-day return minus coin mean, Welch t > 0: 0.0079572, passed: True
- Counts: bars in a position: 8433
- Decided by: The mean timing gain has t >= 2 over at least 300 bars in a position and the top third beats the bottom third with Welch t > 0.
- Reading: Bars in a position are bars with a non-zero postRebalance_current_allocation and a next close in the same window; the thirds are cut by forecast pooled over all coins and windows (stable sort, equal-size split); the situation check uses close below the prior close within the window with forecast > 0, leaving out each window's first bar.
- Size: unusual move +0.20 % per case over 1 bars, 0.042 of the coin's usual move (4.78 %); normal drift in its direction +0.12 %, total +0.32 %; 6112 cases
Plan: `steps_cards/03_test_plan/brief_absorption_run/plans/030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.d2_absorption-in-volatile-markets.d1_absorbed-selling-on-down-days_1d.md`
Record: `steps_cards/04_backtest/brief_absorption_run/backtests/030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.d2_absorption-in-volatile-markets.d1_absorbed-selling-on-down-days_1d`
Measure: `measure.py`
