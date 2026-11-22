---
plan: 027-01_panic-range-multiple-rebound.b1_panic-rebound-within-a-day_4h
idea: 027-01_panic-range-multiple-rebound.b1_panic-rebound-within-a-day
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean 6-bar excess return (return minus coin's normal 6-bar drift) over bet cases: 0.00194064; t of the mean: 3.08715 (threshold: t >= 2 over at least 30 cases pooled (confirm, with positive slope); t <= -2 over at least 30 cases (reject))
- Supporting check: slope of excess 6-bar return on forecast, grid bars with forecast > 0: 0.000327819, passed: True
- Counts: cases: 6548, supporting grid bars with forecast > 0: 8411
- Decided by: Mean excess return t >= 2 over at least 30 pooled cases and the supporting slope is positive.
- Reading: A case is the first long bet (forecast rise >= 2 from its low since the last bet, reset at flat) in each 6-bar grid cell counted from each window's first row, the drift is each coin's mean non-overlapping 6-bar return over all its windows, and the slope is an ordinary least-squares slope on the grid bars with forecast > 0 and a full 6-bar return inside the window.
- Size: unusual move +0.19 % per case over 6 bars, 0.040 of the coin's usual move (4.78 %); normal drift in its direction +0.14 %, total +0.33 %; 6548 cases
Plan: `steps_cards/03_test_plan/night4_panic_run/plans/027-01_panic-range-multiple-rebound.b1_panic-rebound-within-a-day_4h.md`
Record: `steps_cards/04_backtest/night4_panic_run/backtests/027-01_panic-range-multiple-rebound.b1_panic-rebound-within-a-day_4h`
Measure: `measure.py`
