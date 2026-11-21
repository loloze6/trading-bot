---
plan: 003-03_heavy-volume-rise-continues_1d
idea: 003-03_heavy-volume-rise-continues
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean 5-bar excess return over coin mean on grid bars with forecast >= 2: 0.016876; ordinary t of the mean: 2.97614 (threshold: confirm: mean > 0 with t >= 2 and Spearman > 0; reject: mean < 0 with t <= -2)
- Supporting check: Spearman(forecast, excess return) on signal bars: 0.0371572, passed: True
- Counts: signal grid bars: 511
- Decided by: Mean excess return above 0 with t >= 2 and Spearman correlation above 0 (confirm rule).
- Reading: A bar is in the situation when the raw component value is above 0 (long side); grid bars are positions 0,5,10,... of each window with close[t+5] inside the window, and the coin's mean 5-bar return is taken over all its windows' grid bars together.
- Size: unusual move +0.32 % per case over 5 bars, 0.020 of the coin's usual move (10.60 %); normal drift in its direction +0.59 %, total +0.91 %; 1672 cases
Plan: `steps_cards/03_test_plan/volume_run/plans/003-03_heavy-volume-rise-continues_1d.md`
Record: `steps_cards/04_backtest/volume_run/backtests/003-03_heavy-volume-rise-continues_1d`
Measure: `measure.py`
