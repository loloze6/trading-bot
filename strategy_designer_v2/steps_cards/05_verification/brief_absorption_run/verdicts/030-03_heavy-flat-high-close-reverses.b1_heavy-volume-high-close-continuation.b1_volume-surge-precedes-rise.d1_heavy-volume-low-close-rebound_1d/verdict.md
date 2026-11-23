---
plan: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d1_heavy-volume-low-close-rebound_1d
idea: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d1_heavy-volume-low-close-rebound
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled OLS slope of excess next-10-bar return on forecast: 0.00135766; OLS t of the slope: 2.58977 (threshold: t >= 2.0 confirms (with the check), t <= -2.0 rejects)
- Supporting check: mean excess 10-bar return on grid bars with forecast >= 10: 0.0139168, passed: True
- Counts: grid cases: 1691, cases with a forecast of 10 or more: 377
- Decided by: The slope's t is 2.0 or more and the mean excess return on forecast >= 10 cases is above 0.
- Reading: The situation is taken as graded, so it holds on every bar where the raw component value (close's nearness to the low times the volume ratio) is positive (from prices when the raw value is missing), on the long side; the coin's mean 10-bar return is taken over the same non-overlapping grid of all its windows; the slope's t is the ordinary least-squares t; missing a minimum count gives 'not observable'.
- Size: unusual move +0.38 % per case over 10 bars, 0.021 of the coin's usual move (14.49 %); normal drift in its direction +1.18 %, total +1.56 %; 1593 cases
Plan: `steps_cards/03_test_plan/brief_absorption_run/plans/030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d1_heavy-volume-low-close-rebound_1d.md`
Record: `steps_cards/04_backtest/brief_absorption_run/backtests/030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d1_heavy-volume-low-close-rebound_1d`
Measure: `measure.py`
