---
plan: 003-01_thin-volume-rise-reverses_1d
idea: 003-01_thin-volume-rise-reverses
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean 5-bar excess return after thin-volume rise events (forecast <= -2): -0.00178307; t of the mean: -0.501122 (threshold: confirm: mean <= 0 with t <= -2 on >= 30 events and check passes; reject: mean >= 0 with t >= +2 on >= 30 events)
- Supporting check: mean excess return, larger-|forecast| half minus smaller half (must be <= 0): 0.00176791, passed: False
- Counts: non-overlapping events: 930, active bars: 3838
- Decided by: t lies between -2 and +2, which the plan calls inconclusive.
- Reading: Thin volume is recomputed as volume over its 30-bar mean including the current bar (the regime column where 30 bars are not yet available in the window), a rise is the recorded raw vol-scaled return > 0 (else the bar's return); events are de-overlapped before dropping those without a 5-bar return inside the window; the larger half is |forecast| strictly above the median and the smaller half at or below it, and an empty half fails the check.
- Size: unusual move +0.28 % per case over 5 bars, 0.015 of the coin's usual move (10.60 %); normal drift in its direction -0.60 %, total -0.32 %; 1041 cases
Plan: `steps_cards/03_test_plan/volume_run/plans/003-01_thin-volume-rise-reverses_1d.md`
Record: `steps_cards/04_backtest/volume_run/backtests/003-01_thin-volume-rise-reverses_1d`
Measure: `measure.py`
