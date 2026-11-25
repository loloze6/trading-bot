---
plan: 054-04.b1_reclaimed-low-after-rise_1d
idea: 054-04.b1_reclaimed-low-after-rise
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 10-bar short move per case, before costs: 0.0371841; t of the mean, cases clustered by day: 1.48316 (threshold: confirm: mean > 0 with t >= 2 over at least 30 cases; reject: mean < 0 with t <= -2 over at least 30 cases)
- Supporting check: mean unusual short move, larger |forecast| half minus smaller half: 0.123124, passed: True
- Counts: cases: 39, days: 31
- Decided by: The t is between -2 and 2 over at least 30 cases.
- Reading: The situation is low below the lowest low of the 30 prior bars of the same window with close at or above it (bars without 30 prior bars in the window left out of the agreement), the expected side is short; a case is the first short bet (forecast rise of at least 2 points on the short side from its lowest level since the last bet, from 0 after a flat) in each 10-bar grid cell of a window, its return taken from that bet's close over 10 bars inside the window; the coin's drift is the mean of its non-overlapping 10-bar returns on the grid of all windows; the t clusters deviations by UTC day with a D/(D-1) correction; the supporting halves are |forecast| above the median versus at or below it.
- Size: unusual move +3.72 % (t 1.51, the cases of one day together: 31 days) per case over 10 bars, 0.220 of the coin's usual move (14.49 %); normal drift in its direction -1.18 %, total +2.54 %; 39 cases
Plan: `steps_cards/03_test_plan/pilot_panic_run/plans/054-04.b1_reclaimed-low-after-rise_1d.md`
Record: `steps_cards/04_backtest/pilot_panic_run/backtests/054-04.b1_reclaimed-low-after-rise_1d`
Measure: `measure.py`
