---
plan: 028-03_low-volume-up-fade.b1_quiet-up-hour-fade-wider_1h
idea: 028-03_low-volume-up-fade.b1_quiet-up-hour-fade-wider
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual move of short bets over 6 bars (in the signal's direction): 0.000390256; ordinary t of the mean: 2.13603 (threshold: mean > 0 with t >= 2 over at least 30 cases (confirm); mean < 0 with t <= -2 (reject))
- Supporting check: slope of unusual move on forecast size: 3.39506e-05, passed: True
- Counts: cases: 19299
- Decided by: Mean unusual move above 0 with t >= 2 over at least 30 cases and a slope above 0.
- Reading: The volume condition is read from the recorded regime (mean_reversion = volume ratio between 0.67 and 1.5) and the rise from the raw scaled return being above 0; a case is the first short bet (forecast falling by >= 2 points from its least-short level since the last bet, reset at 0) in each 6-bar grid cell counted from each window's first row, with a full 6-bar return inside the window; the normal drift is the coin's mean non-overlapping 6-bar return over all its windows; the slope regresses the unusual move on |forecast|; the plan's 'fewer than 30 cases' is reported as not observable as the workflow requires.
- Size: unusual move +0.04 % per case over 6 bars, 0.017 of the coin's usual move (2.45 %); normal drift in its direction -0.03 %, total +0.00 %; 19299 cases
Plan: `steps_cards/03_test_plan/night4_volumehour_run/plans/028-03_low-volume-up-fade.b1_quiet-up-hour-fade-wider_1h.md`
Record: `steps_cards/04_backtest/night4_volumehour_run/backtests/028-03_low-volume-up-fade.b1_quiet-up-hour-fade-wider_1h`
Measure: `measure.py`
