---
plan: 030-03_heavy-flat-high-close-reverses_1d
idea: 030-03_heavy-flat-high-close-reverses
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean short-side unusual 5-bar move (minus the 5-bar return from the signal close, minus the coin's normal 5-bar drift): -0.00736527; t of the mean: -0.936177 (threshold: confirm: t >= 2 over at least 30 cases with correlation > 0; reject: t <= -2 over at least 30 cases)
- Supporting check: correlation of |forecast| on the signal bar with the short-side unusual move, above 0: 0.0398178, passed: True
- Counts: cases: 150
- Decided by: Inconclusive rule: t lies between -2 and 2 over at least 30 cases.
- Reading: Situation recomputed from prices as volume / mean of the prior 20 recorded bars of the same window >= 2 and |close - open| / open <= 1 %, expected side short; active bars in a window's first 20 rows, where the prior 20-bar mean cannot be computed, are left out of the agreement (34 such bars); cases are the first short bet (a rise of the short forecast of at least 2 points from its lowest level since the last bet) in each 5-bar grid cell of each window, measured from that bet's close over 5 bars inside the window, with the coin's drift the mean of its non-overlapping 5-bar grid returns over all its windows.
- Size: unusual move -0.74 % per case over 5 bars, -0.064 of the coin's usual move (10.60 %); normal drift in its direction -0.61 %, total -1.35 %; 150 cases
Plan: `steps_cards/03_test_plan/brief_absorption_run/plans/030-03_heavy-flat-high-close-reverses_1d.md`
Record: `steps_cards/04_backtest/brief_absorption_run/backtests/030-03_heavy-flat-high-close-reverses_1d`
Measure: `measure.py`
