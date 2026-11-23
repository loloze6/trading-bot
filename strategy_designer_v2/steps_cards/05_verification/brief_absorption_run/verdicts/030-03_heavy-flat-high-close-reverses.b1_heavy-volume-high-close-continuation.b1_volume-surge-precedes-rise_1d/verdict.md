---
plan: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise_1d
idea: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled OLS slope of excess 10-bar forward return on forecast (non-overlapping grid): 0.00212884; OLS slope t: 3.25541 (threshold: confirm: slope > 0 with t >= 2 and supporting check passes; reject: slope < 0 with t <= -2)
- Supporting check: mean excess 10-bar return on grid bars with forecast > 0: 0.00848519, passed: True
- Counts: independent grid cases with forecast > 0: 708, independent grid cases (all): 1691
- Decided by: The slope is positive with t >= 2 and the mean excess on forecast > 0 bars is above 0.
- Reading: Situation read as raw log volume ratio > 0 with a long forecast (raw recomputed from volume where missing); grid bars at positions 0,10,20,... of each window with a full 10-bar forward return inside the window; the coin's mean 10-bar return is the mean over its grid returns of all windows; slope and t from ordinary least squares with intercept; the plan's minimum of 100 grid cases with forecast > 0 is treated as a minimum count giving 'not observable'.
- Size: unusual move +0.43 % per case over 10 bars, 0.015 of the coin's usual move (14.49 %); normal drift in its direction +1.18 %, total +1.61 %; 1423 cases
Plan: `steps_cards/03_test_plan/brief_absorption_run/plans/030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise_1d.md`
Record: `steps_cards/04_backtest/brief_absorption_run/backtests/030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise_1d`
Measure: `measure.py`
