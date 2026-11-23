---
plan: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b2_heavy-low-close-next-day-rebound_1d
idea: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b2_heavy-low-close-next-day-rebound
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of next-day excess return on forecast, over cases with forecast > 0: 0.00113262; OLS slope t: 4.22837 (threshold: confirm: slope t >= 2 with forecast-weighted mean excess > 0 and >= 100 cases; reject: slope t <= -2 with >= 100 cases)
- Supporting check: forecast-weighted mean next-day excess return > 0: 0.00803841, passed: True
- Counts: cases: 1607
- Decided by: Slope t >= 2 and forecast-weighted mean excess return > 0 with at least 100 cases (confirm rule).
- Reading: Situation bars are bars whose volume is at least 2x the mean of the prior 20 bars (recomputed from prices, the recorded regime used where the window lacks 20 prior bars) with a close location from the high above 0, on the long side; cases are all forecast>0 bars with a next bar in the same window (a 1-bar grid is every bar), pooled over coins and windows, the excess removing each coin's mean 1-bar return over all its windows, and the slope t is the OLS t of excess return on forecast.
- Size: unusual move +0.52 % per case over 1 bars, 0.113 of the coin's usual move (4.78 %); normal drift in its direction +0.12 %, total +0.64 %; 1226 cases
Plan: `steps_cards/03_test_plan/brief_absorption_run/plans/030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b2_heavy-low-close-next-day-rebound_1d.md`
Record: `steps_cards/04_backtest/brief_absorption_run/backtests/030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b2_heavy-low-close-next-day-rebound_1d`
Measure: `measure.py`
