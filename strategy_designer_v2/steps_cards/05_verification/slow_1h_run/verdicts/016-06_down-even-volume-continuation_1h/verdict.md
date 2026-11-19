---
plan: 016-06_down-even-volume-continuation_1h
idea: 016-06_down-even-volume-continuation
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled OLS slope of 72-bar excess forward return on forecast, trending grid bars: 0.00133669; OLS slope t: 0.936593 (threshold: confirm: slope > 0 with t >= 2; reject: slope < 0 with t <= -2; otherwise inconclusive; at least 200 grid cases)
- Supporting check: none
- Counts: grid cases in the fallen regime: 2762
- Decided by: The slope's t = 0.94 lies between -2 and 2 over 2762 grid cases (inconclusive rule).
- Reading: Situation bars are those whose 72-bar close-to-close return inside the window is below zero (active bars without 72 bars of window history are left out) and the expected side is short; grid bars are positions 0, 72, 144, ... of each window whose recorded regime is 'trending', the coin's mean 72-bar return is the mean over all grid bars of all its windows, and the plan's 'fewer than 200 grid cases' is treated as the minimum count (not observable).
Plan: `steps_cards/03_test_plan/slow_1h_run/plans/016-06_down-even-volume-continuation_1h.md`
Record: `steps_cards/04_backtest/slow_1h_run/backtests/016-06_down-even-volume-continuation_1h`
Measure: `measure.py`
