---
plan: 016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d2_slow-three-day-rebound-hold_1h
idea: 016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d2_slow-three-day-rebound-hold
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of the slope of 72-bar excess return on forecast (mean_reversion grid bars): 2.74545; OLS slope t: 2.74545 (threshold: confirm if t >= 2 with supporting check passed; reject if t <= -2)
- Supporting check: slope of 24-to-72-bar excess return on forecast, > 0 and >= half the main slope: 6.03439e-05, passed: False
- Counts: grid cases in the regime: 2762, grid cases with forecast > 0: 1891
- Decided by: Main slope t >= 2 but the supporting check fails.
- Reading: Grid bars are positions 0, 72, 144... of each window with close[t+72] inside it, the regime is the recorded `regime` at the grid bar, and each excess (72-bar and 24-to-72-bar) is over that coin's mean of the same grid return across all its grid bars in all windows.
- Size: unusual move -0.25 % per case over 72 bars, -0.030 of the coin's usual move (8.23 %); normal drift in its direction +0.41 %, total +0.16 %; 4678 cases
Plan: `steps_cards/03_test_plan/d_line_1h_run/plans/016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d2_slow-three-day-rebound-hold_1h.md`
Record: `steps_cards/04_backtest/d_line_1h_run/backtests/016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d2_slow-three-day-rebound-hold_1h`
Measure: `measure.py`
