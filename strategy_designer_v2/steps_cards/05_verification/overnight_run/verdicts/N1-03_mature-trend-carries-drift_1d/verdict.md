---
plan: N1-03_mature-trend-carries-drift_1d
idea: N1-03_mature-trend-carries-drift
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled OLS slope of forward 20-bar excess return on forecast: 0.000866576; OLS t of slope (non-overlapping 20-bar blocks): 0.598819 (threshold: confirm: slope > 0 with t >= 2 and position-weighted mean excess > 0; reject: slope < 0 with t <= -2)
- Supporting check: mean forward 20-bar excess return at age 5-20 (< 0): -0.0143814, passed: True
- Counts: non-overlapping 20-bar blocks with forecast > 0: 393, non-overlapping 20-bar blocks (all): 777, blocks with age 5 to 20: 71
- Decided by: Slope t = 0.60 lies between -2 and 2, which the plan calls inconclusive.
- Reading: Used non-overlapping 20-bar blocks at window positions 0,20,40,... with plain OLS t over all grid bars (forecast 0 included), the coin benchmark as the mean of all its in-window forward 20-bar returns, position weights as postRebalance_current_allocation on the grid, and the supporting check on the same grid.
Plan: `steps_cards/03_test_plan/overnight_run/plans_newcomp/N1-03_mature-trend-carries-drift_1d.md`
Record: `steps_cards/04_backtest/overnight_run/backtests/N1-03_mature-trend-carries-drift_1d`
Measure: `measure.py`
