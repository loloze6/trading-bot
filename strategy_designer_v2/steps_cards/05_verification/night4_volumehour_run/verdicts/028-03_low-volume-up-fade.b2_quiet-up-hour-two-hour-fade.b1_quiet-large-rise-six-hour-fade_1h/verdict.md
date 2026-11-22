---
plan: 028-03_low-volume-up-fade.b2_quiet-up-hour-two-hour-fade.b1_quiet-large-rise-six-hour-fade_1h
idea: 028-03_low-volume-up-fade.b2_quiet-up-hour-two-hour-fade.b1_quiet-large-rise-six-hour-fade
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean short-signed unusual 6-bar move of short bets: 0.000191148; t of the mean: 0.911988 (threshold: positive with t >= 2 to confirm, negative with t <= -2 to reject, over at least 30 cases)
- Supporting check: larger-forecast half minus smaller-forecast half mean unusual move (>= 0): -0.000263007, passed: False
- Counts: cases: 9180, larger_half_cases: 4590, smaller_half_cases: 4590
- Decided by: t is between -2 and 2 over at least 30 cases.
- Reading: Bets are falls of the forecast of at least 2 points from its lowest short level since the last bet (reset at flat), the first bet in each 6-bar cell counted from each window's first row, the drift is the coin's mean 6-bar return on that grid pooled over all windows, the median split puts cases strictly above the median in the larger half (or at/above it if that leaves a half empty), and the volume band is rebuilt from volume over 720 bars including the current one, falling back to the recorded regime where a window has fewer than 720 bars of history.
- Size: unusual move +0.02 % per case over 6 bars, 0.009 of the coin's usual move (1.98 %); normal drift in its direction -0.03 %, total -0.02 %; 9180 cases
Plan: `steps_cards/03_test_plan/night4_volumehour_run/plans/028-03_low-volume-up-fade.b2_quiet-up-hour-two-hour-fade.b1_quiet-large-rise-six-hour-fade_1h.md`
Record: `steps_cards/04_backtest/night4_volumehour_run/backtests/028-03_low-volume-up-fade.b2_quiet-up-hour-two-hour-fade.b1_quiet-large-rise-six-hour-fade_1h`
Measure: `measure.py`
