---
plan: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.d2_absorption-in-volatile-markets_1d
idea: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.d2_absorption-in-volatile-markets
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of next-day return minus coin mean on forecast, regime-active bars pooled: 0.000564783; OLS slope t: 6.17336 (threshold: t >= 2 (with timing gain > 0) confirms, t <= -2 rejects, on at least 300 active bars)
- Supporting check: book timing gain (mean daily return minus position x coin mean daily return): 0.00034239, passed: True
- Counts: regime-active bars pooled: 7591
- Decided by: The slope t is 2 or more on at least 300 active bars and the timing gain is above 0.
- Reading: Situation bars are those where the detector chose the volatility regime (20-day vol over its 60-day mean >= 1, recorded as regime 'mean_reversion') and the component's raw product (close distance from high x volume ratio x vol ratio) is positive, on the long side; regime-active bars are bars with regime 'mean_reversion', the coin's mean daily return is pooled over all its windows, the slope t is the OLS t with an intercept, and the timing gain uses each coin's postRebalance_total_value day returns averaged across coins per day minus the held position times the coin's mean daily return averaged the same way.
- Size: unusual move +0.16 % per case over 1 bars, 0.033 of the coin's usual move (4.78 %); normal drift in its direction +0.12 %, total +0.28 %; 3071 cases
Plan: `steps_cards/03_test_plan/brief_absorption_run/plans/030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.d2_absorption-in-volatile-markets_1d.md`
Record: `steps_cards/04_backtest/brief_absorption_run/backtests/030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.d2_absorption-in-volatile-markets_1d`
Measure: `measure.py`
