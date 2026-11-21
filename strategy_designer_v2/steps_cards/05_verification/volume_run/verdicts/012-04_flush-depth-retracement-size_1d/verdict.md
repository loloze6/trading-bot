---
plan: 012-04_flush-depth-retracement-size_1d
idea: 012-04_flush-depth-retracement-size
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of excess 3-bar return on forecast, flush bars: -0.00310886; OLS slope t: -0.746134 (threshold: confirm: slope > 0 with t >= 2 and mean excess > 0; reject: slope < 0 with t <= -2)
- Supporting check: mean excess 3-bar return of flush bars: 0.00223649, passed: True
- Counts: kept flush bars: 73
- Decided by: The slope t lies between -2 and 2.
- Reading: Situation recomputed from prices (return over 20-bar std of 1-bar returns incl. current, volume over mean of prior 20, lower wick over range), active bars whose rule cannot be recomputed in-window excluded; flush bars within <=3 bars of a kept one dropped; coin mean 3-bar return from the non-overlapping 0,3,6,... grid of every window pooled; OLS slope t; fewer than 30 kept flush bars reported as not observable per the workflow's minimum-count rule.
- Size: unusual move +0.18 % per case over 3 bars, 0.029 of the coin's usual move (7.96 %); normal drift in its direction +0.36 %, total +0.54 %; 74 cases
Plan: `steps_cards/03_test_plan/volume_run/plans/012-04_flush-depth-retracement-size_1d.md`
Record: `steps_cards/04_backtest/volume_run/backtests/012-04_flush-depth-retracement-size_1d`
Measure: `measure.py`
