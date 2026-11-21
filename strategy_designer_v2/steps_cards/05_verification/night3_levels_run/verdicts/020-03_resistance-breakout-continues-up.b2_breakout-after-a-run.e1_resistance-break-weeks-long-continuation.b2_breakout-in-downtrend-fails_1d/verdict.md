---
plan: 020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.e1_resistance-break-weeks-long-continuation.b2_breakout-in-downtrend-fails_1d
idea: 020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.e1_resistance-break-weeks-long-continuation.b2_breakout-in-downtrend-fails
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean short-direction unusual 20-bar move per case: 0.0198868; t of the mean: 1.8574 (threshold: confirm t >= 2 over >= 20 cases with rank correlation > 0; reject t <= -2 over >= 20 cases)
- Supporting check: Spearman rank correlation of |entry forecast| vs short-direction unusual move: 0.0261511, passed: True
- Counts: cases: 413
- Decided by: t lies between -2 and 2, which the plan calls inconclusive.
- Reading: A case is the first short bet (a rise of at least 2 forecast points in short size from its lowest level since the last bet) in each 20-bar grid cell of a window, dropped when its 20-bar return would leave the window, with drift the coin's mean non-overlapping 20-bar return over all its windows.
- Size: unusual move +1.99 % per case over 20 bars, 0.076 of the coin's usual move (21.24 %); normal drift in its direction -2.51 %, total -0.52 %; 413 cases
Plan: `steps_cards/03_test_plan/night3_levels_run/plans/020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.e1_resistance-break-weeks-long-continuation.b2_breakout-in-downtrend-fails_1d.md`
Record: `steps_cards/04_backtest/night3_levels_run/backtests/020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.e1_resistance-break-weeks-long-continuation.b2_breakout-in-downtrend-fails_1d`
Measure: `measure.py`
