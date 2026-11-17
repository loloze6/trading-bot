---
plan: 003-04_heavy-volume-drop-continues_1d
idea: 003-04_heavy-volume-drop-continues
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean excess 5-bar return after signal bars (vs holding the coin): -0.00894038; t of the mean: -1.50541 (threshold: confirm: mean < 0 with t <= -2 over >= 30 independent events; reject: mean > 0 with t >= +2 over >= 30)
- Supporting check: mean excess of more-negative-forecast half minus other half (< 0): -0.00857291, passed: True
- Counts: independent events: 286
- Decided by: t lies between -2 and +2 over at least 30 events.
- Reading: A signal is kept when at least 5 bars after the previous kept one in its window (so 5-bar returns do not overlap) and only if close[t+5] exists in the window; the coin's mean is over non-overlapping 5-bar returns on positions 0,5,10,... of all its windows; the median split puts the floor(n/2) most negative forecasts (stable sort) in the more-negative half.
Plan: `steps_cards/03_test_plan/volume_run/plans/003-04_heavy-volume-drop-continues_1d.md`
Record: `steps_cards/04_backtest/volume_run/backtests/003-04_heavy-volume-drop-continues_1d`
Measure: `measure.py`
