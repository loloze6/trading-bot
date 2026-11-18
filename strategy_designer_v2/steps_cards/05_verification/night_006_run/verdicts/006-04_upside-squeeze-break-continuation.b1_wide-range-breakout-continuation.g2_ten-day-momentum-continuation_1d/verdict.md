---
plan: 006-04_upside-squeeze-break-continuation.b1_wide-range-breakout-continuation.g2_ten-day-momentum-continuation_1d
idea: 006-04_upside-squeeze-break-continuation.b1_wide-range-breakout-continuation.g2_ten-day-momentum-continuation
fit: exact
status: confirmed
---
Situation check: 99 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of the pooled OLS slope of excess 10-bar forward return on forecast: 2.57645; OLS slope t: 2.57645 (threshold: confirm: t >= 2 with top-minus-bottom quintile > 0; reject: t <= -2; else inconclusive)
- Supporting check: top minus bottom forecast quintile mean excess 10-bar return: 0.0240831, passed: True
- Counts: independent grid cases: 1691, top quintile cases: 338, bottom quintile cases: 339
- Decided by: Confirm rule met: slope t is 2 or more and the top-minus-bottom quintile difference is above 0.
- Reading: Grid at positions 0,10,20,... of each window with forward return close[t+10]/close[t]-1 inside the window; excess over each coin's mean grid 10-bar return across all its windows; quintiles are of the pooled grid forecasts (ties broken by order).
Plan: `steps_cards/03_test_plan/night_006_run/plans/006-04_upside-squeeze-break-continuation.b1_wide-range-breakout-continuation.g2_ten-day-momentum-continuation_1d.md`
Record: `steps_cards/04_backtest/night_006_run/backtests/006-04_upside-squeeze-break-continuation.b1_wide-range-breakout-continuation.g2_ten-day-momentum-continuation_1d`
Measure: `measure.py`
