---
plan: 031-01_near-yearly-low-keeps-falling_1d
idea: 031-01_near-yearly-low-keeps-falling
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of drift-adjusted 20-bar short gain on |forecast|: 0.00235943; OLS slope t: 1.7029 (threshold: slope > 0 with t >= 2 confirms (with top-fifth check); slope < 0 with t <= -2 rejects)
- Supporting check: mean drift-adjusted short gain of the top fifth of |forecast|: 0.0487591, passed: True
- Counts: non-overlapping cases: 806, top-fifth cases: 161
- Decided by: The slope's t is between -2 and 2.
- Reading: Cases are grid positions 0, 20, 40, ... of each window with a 20-bar forward close in the same window, all kept including |forecast| 0, drift is each coin's mean 20-bar grid return over all its windows, and the top fifth is the floor(n/5) pooled cases with the largest |forecast|.
- Size: unusual move -1.41 % (t -0.75, the cases of one day together: 243 days) per case over 20 bars, -0.063 of the coin's usual move (21.24 %); normal drift in its direction -3.03 %, total -4.44 %; 394 cases
Plan: `steps_cards/03_test_plan/night6_yearlow_run/plans/031-01_near-yearly-low-keeps-falling_1d.md`
Record: `steps_cards/04_backtest/night6_yearlow_run/backtests/031-01_near-yearly-low-keeps-falling_1d`
Measure: `measure.py`
