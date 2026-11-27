---
plan: 086-01_first-down-day-streak-length_1d
idea: 086-01_first-down-day-streak-length
fit: exact
status: no effect
---
Situation check: 99 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean short-direction unusual 3-bar move per case: -0.0155826; t of the mean, same-day cases summed: -1.73522 (threshold: mean > 0 with day-clustered t >= 2 confirms (with slope check); mean < 0 with t <= -2 rejects)
- Supporting check: OLS slope of unusual move on broken run length, t >= 1.5: 0.28674, passed: False
- Counts: cases: 313, distinct days: 235
- Decided by: Inconclusive: the t of the mean unusual move lies between -2 and 2. No effect (common/verdicts.md): t in the idea's direction -1.735 (below 1), 313 cases (30 needed).
- Reading: Situation = recorded broken_run count >= 2 on a down close (first window row accepted on the count alone) in regime 'trending' (profile vetoes passed), side short; a case is the first short bet (forecast magnitude rising >= 2 points from its lowest level since the last bet, from 0 after flat) in each 3-bar grid cell of a window, its return taken from that bar's close over 3 bars inside the window; drift = mean of the coin's non-overlapping 3-bar grid returns over all its windows; day-clustered t uses a G/(G-1) correction; slope t is the ordinary OLS t; the plan's 'fewer than 30 cases on 30 distinct days' is treated as the minimum count.
- Size: unusual move -1.56 % (t -1.74, the cases of one day together: 235 days) per case over 3 bars, -0.179 of the coin's usual move (9.34 %); normal drift in its direction -0.35 %, total -1.91 %; 313 cases
- Effect check (common/verdicts.md): no effect: t in the idea's direction -1.735 (below 1), 313 cases (30 needed)
Plan: `steps_cards/03_test_plan/pilot_a4_named_run/plans/086-01_first-down-day-streak-length_1d.md`
Record: `steps_cards/04_backtest/pilot_a4_named_run/backtests/086-01_first-down-day-streak-length_1d`
Measure: `measure.py`
