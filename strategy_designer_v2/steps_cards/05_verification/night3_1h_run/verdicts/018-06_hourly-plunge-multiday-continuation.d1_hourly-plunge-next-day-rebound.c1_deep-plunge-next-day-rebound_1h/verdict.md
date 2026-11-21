---
plan: 018-06_hourly-plunge-multiday-continuation.d1_hourly-plunge-next-day-rebound.c1_deep-plunge-next-day-rebound_1h
idea: 018-06_hourly-plunge-multiday-continuation.d1_hourly-plunge-next-day-rebound.c1_deep-plunge-next-day-rebound
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean excess 24-bar return after a bet, before costs: 0.0010826; t of the mean: 1.92127 (threshold: confirm: mean > 0 with t >= 2 over at least 30 cases; reject: mean < 0 with t <= -2 over at least 30 cases)
- Supporting check: mean excess, forecast >= 10 minus forecast < 10 (Welch t 1.999): 0.00289852, passed: True
- Counts: cases: 8426, cases forecast >= 10: 1860, cases forecast < 10: 6566
- Decided by: The t of the mean excess 24-bar return lies between -2 and 2.
- Reading: The situation is read as a negative 24-bar return (a drop, which standardise expresses as a multiple of the usual daily move and the graded dead zone weights), on the long side. A bet is a rise of the forecast of at least 2 points from its lowest level since the last bet (from 0 after a flat), and the first bet in each 24-bar grid cell is the case. The coin's normal drift is the mean of its non-overlapping 24-bar returns on the grid of all its windows. The supporting check passes when the difference of means (forecast >= 10 minus < 10) is above 0, and the Welch t is reported. The plan's 30-case minimum, when not reached, gives 'not observable'.
- Size: unusual move +0.11 % per case over 24 bars, 0.020 of the coin's usual move (4.87 %); normal drift in its direction +0.15 %, total +0.25 %; 8426 cases
Plan: `steps_cards/03_test_plan/night3_1h_run/plans/018-06_hourly-plunge-multiday-continuation.d1_hourly-plunge-next-day-rebound.c1_deep-plunge-next-day-rebound_1h.md`
Record: `steps_cards/04_backtest/night3_1h_run/backtests/018-06_hourly-plunge-multiday-continuation.d1_hourly-plunge-next-day-rebound.c1_deep-plunge-next-day-rebound_1h`
Measure: `measure.py`
