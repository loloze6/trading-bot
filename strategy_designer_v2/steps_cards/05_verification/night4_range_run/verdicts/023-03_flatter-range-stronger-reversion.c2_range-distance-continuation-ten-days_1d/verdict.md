---
plan: 023-03_flatter-range-stronger-reversion.c2_range-distance-continuation-ten-days_1d
idea: 023-03_flatter-range-stronger-reversion.c2_range-distance-continuation-ten-days
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of coin-demeaned 10-bar forward return on forecast, pooled: 0.000737896; OLS slope t: 2.17207 (threshold: confirm if t >= 2 (with positive timing part); reject if t <= -2)
- Supporting check: book mean daily return minus gain from market rise (timing part): 0.000436302, passed: True
- Counts: non-overlapping cases: 1691
- Decided by: The slope t is 2 or more and the timing part is positive.
- Reading: All grid bars (0, 10, 20, ... with a full 10-bar return inside the window) enter the regression including zero forecasts, the coin mean 10-bar return is taken on those same grid samples over all windows, each coin's book is its own value series with the position held into a day taken from the previous bar's post-rebalance allocation, and the plan's 'fewer than 300 cases' is reported as 'not observable' per the workflow.
- Size: unusual move +0.33 % per case over 10 bars, 0.018 of the coin's usual move (14.49 %); normal drift in its direction -0.06 %, total +0.27 %; 1579 cases
Plan: `steps_cards/03_test_plan/night4_range_run/plans/023-03_flatter-range-stronger-reversion.c2_range-distance-continuation-ten-days_1d.md`
Record: `steps_cards/04_backtest/night4_range_run/backtests/023-03_flatter-range-stronger-reversion.c2_range-distance-continuation-ten-days_1d`
Measure: `measure.py`
