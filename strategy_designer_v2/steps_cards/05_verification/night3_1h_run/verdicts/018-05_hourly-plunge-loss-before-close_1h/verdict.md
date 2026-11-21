---
plan: 018-05_hourly-plunge-loss-before-close_1h
idea: 018-05_hourly-plunge-loss-before-close
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean excess short return from the first -2 crossing to the same UTC day's close: -0.000196782; one-group t of the mean: -0.451061 (threshold: confirm t >= 2 with supporting difference > 0, reject t <= -2, over at least 30 cases)
- Supporting check: mean excess (forecast <= -10) minus mean excess (-10 < forecast <= -2): 0.00241055, passed: True
- Counts: cases: 7593, cases forecast <= -10: 745, cases forecast between -10 and -2: 6848
- Decided by: The t of the mean excess short return lies between -2 and 2.
- Reading: A case is the first bar of each coin-window-UTC-day whose forecast is <= -2 while the previous bar's forecast in the same window was > -2 (a window's first row cannot cross), its end is the last recorded bar of that UTC day in the window (a signal on that last bar counts with a zero return), the hours remaining are the clock hours between the two bars, the coin's mean hourly return pools all its windows, and the one-case-per-coin-day cases stand in for the 24-bar grid.
- Size: unusual move -0.11 % per case over 24 bars, -0.020 of the coin's usual move (4.87 %); normal drift in its direction -0.15 %, total -0.25 %; 8426 cases
Plan: `steps_cards/03_test_plan/night3_1h_run/plans/018-05_hourly-plunge-loss-before-close_1h.md`
Record: `steps_cards/04_backtest/night3_1h_run/backtests/018-05_hourly-plunge-loss-before-close_1h`
Measure: `measure.py`
