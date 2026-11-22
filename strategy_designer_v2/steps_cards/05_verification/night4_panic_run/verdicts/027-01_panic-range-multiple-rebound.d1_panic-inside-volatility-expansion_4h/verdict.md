---
plan: 027-01_panic-range-multiple-rebound.d1_panic-inside-volatility-expansion_4h
idea: 027-01_panic-range-multiple-rebound.d1_panic-inside-volatility-expansion
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 84-bar move per case (return minus coin's normal 84-bar drift): -0.00235384; ordinary t: -0.38997 (threshold: mean > 0 with t >= 2 (confirm, with supporting check); mean < 0 with t <= -2 (reject))
- Supporting check: top-half minus bottom-half forecast size mean unusual move: 0.0124794, passed: True
- Counts: cases in total: 1146
- Decided by: The t of the mean unusual move lies between -2 and 2.
- Reading: A case is the first long bet (forecast rise of at least 2 points from its lowest level since the last bet, from 0 after flat) in each 84-bar grid cell of a window, its return taken from that bar's close if 84 bars remain in the window; cases of all coins are pooled into one mean; the halves of forecast size are split by rank at the signal bar (the middle case left out when the count is odd); the plan's fewer-than-30-cases rule is treated as the minimum count.
- Size: unusual move -0.24 % per case over 84 bars, -0.012 of the coin's usual move (17.66 %); normal drift in its direction +2.10 %, total +1.87 %; 1146 cases
Plan: `steps_cards/03_test_plan/night4_panic_run/plans/027-01_panic-range-multiple-rebound.d1_panic-inside-volatility-expansion_4h.md`
Record: `steps_cards/04_backtest/night4_panic_run/backtests/027-01_panic-range-multiple-rebound.d1_panic-inside-volatility-expansion_4h`
Measure: `measure.py`
