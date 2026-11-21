---
plan: 003-03_heavy-volume-rise-continues_1d
idea: 003-03_heavy-volume-rise-continues
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of the mean 5-bar excess return (vs the coin's mean 5-bar return) on grid bars with forecast >= 5: 0.0162132; t of the mean: 2.6199 (threshold: confirm: mean > 0 with t >= 2 over >= 30 cases and Spearman > 0; reject: mean < 0 with t <= -2 over >= 30 cases)
- Supporting check: Spearman(forecast, 5-bar excess) on grid bars with forecast > 0: 0.057759, passed: True
- Counts: grid cases with forecast >= 5: 389, grid bars with forecast > 0: 1642
- Decided by: The mean excess is positive with t >= 2 over at least 30 cases and the Spearman correlation is above 0.
- Reading: Grid bars are positions 0, 5, 10, ... of each window with t+5 inside the window. The coin's mean 5-bar return is the mean over all of that coin's grid samples in all windows. The plan's 'fewer than 30 cases' rule is reported as not observable.
- Size: unusual move +0.32 % per case over 5 bars, 0.020 of the coin's usual move (10.60 %); normal drift in its direction +0.59 %, total +0.91 %; 1672 cases
Plan: `steps_cards/03_test_plan/night_run/plans/003-03_heavy-volume-rise-continues_1d.md`
Record: `steps_cards/04_backtest/night_run/backtests/003-03_heavy-volume-rise-continues_1d`
Measure: `measure.py`
