---
plan: 067-02_choppy-down-stretch-keeps-falling_1d
idea: 067-02_choppy-down-stretch-keeps-falling
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of 10-bar forward return net of drift on -forecast (grid, forecast < 0): 0.000693431; OLS slope t: 0.435208 (threshold: confirm if slope t <= -2 (with supporting check); reject if slope t >= +2; else inconclusive)
- Supporting check: mean unusual move in the short direction (-(10-bar return - drift)) > 0: 0.00722773, passed: True
- Counts: grid cases with forecast < 0: 200
- Decided by: the slope t lies between -2 and +2
- Reading: Situation = raw stretch_below < 0 with forecast < 0; grid = bars 0,10,20,... of each window with a full 10-bar forward return; drift = coin's mean 10-bar return on that grid over all its windows; pooled OLS across coins and windows with the ordinary slope t; fewer than 30 cases is reported as not observable.
- Size: unusual move +0.32 % (t 0.44, the cases of one day together: 324 days) per case over 10 bars, 0.030 of the coin's usual move (14.49 %); normal drift in its direction -1.15 %, total -0.82 %; 424 cases
Plan: `steps_cards/03_test_plan/night9_chopstretch_run/plans/067-02_choppy-down-stretch-keeps-falling_1d.md`
Record: `steps_cards/04_backtest/night9_chopstretch_run/backtests/067-02_choppy-down-stretch-keeps-falling_1d`
Measure: `measure.py`
