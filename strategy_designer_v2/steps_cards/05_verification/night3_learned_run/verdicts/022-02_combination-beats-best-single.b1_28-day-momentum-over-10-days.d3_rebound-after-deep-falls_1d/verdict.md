---
plan: 022-02_combination-beats-best-single.b1_28-day-momentum-over-10-days.d3_rebound-after-deep-falls_1d
idea: 022-02_combination-beats-best-single.b1_28-day-momentum-over-10-days.d3_rebound-after-deep-falls
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled OLS slope of 10-bar forward return minus normal drift on forecast, non-overlapping 10-bar grid: -0.00100984; OLS slope t: -1.49474 (threshold: slope > 0 with t >= 2 confirms (with check); slope < 0 with t <= -2 rejects)
- Supporting check: mean unusual 10-bar move over cases (forecast rise >= 2 points, once per grid cell), long direction, > 0: -0.00916952, passed: False
- Counts: grid cells with forecast > 0: 1036, cases: 931, grid cells (all): 1691
- Decided by: The slope's t lies between -2 and 2.
- Reading: situation read as raw fall28 < 0 or raw near_low60 < 0, side long; the regression uses every grid cell (forecast zero included) at positions 0,10,20,... of each window; normal drift is the coin's mean of those non-overlapping 10-bar returns over all windows; a case is the first long bet (forecast rise >= 2 from its lowest level since the last bet, from 0 after a flat) in each grid cell, measured from its bar's close; the plan's too-few-cases rule is reported as 'not observable'.
- Size: unusual move -0.92 % per case over 10 bars, -0.055 of the coin's usual move (14.49 %); normal drift in its direction +1.17 %, total +0.26 %; 931 cases
Plan: `steps_cards/03_test_plan/night3_learned_run/plans/022-02_combination-beats-best-single.b1_28-day-momentum-over-10-days.d3_rebound-after-deep-falls_1d.md`
Record: `steps_cards/04_backtest/night3_learned_run/backtests/022-02_combination-beats-best-single.b1_28-day-momentum-over-10-days.d3_rebound-after-deep-falls_1d`
Measure: `measure.py`
