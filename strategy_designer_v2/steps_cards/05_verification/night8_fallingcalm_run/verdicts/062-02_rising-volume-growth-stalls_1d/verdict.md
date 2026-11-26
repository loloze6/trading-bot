---
plan: 062-02_rising-volume-growth-stalls_1d
idea: 062-02_rising-volume-growth-stalls
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of 5-day forward return minus coin drift on forecast (non-overlapping grid, non-zero forecast): 7.05547e-05; slope t, clustered by day: 0.181387 (threshold: confirm: slope > 0 with t >= 2; reject: slope < 0 with t <= -2; else inconclusive; at least 200 cases)
- Supporting check: none
- Counts: non-overlapping in-profile cases: 1345, days: 409
- Decided by: The slope's t lies between -2 and +2, with at least 200 cases.
- Reading: The rising profile is the recorded regime 'unknown' (the config's only strategy regime); cases are the grid bars at positions 0,5,10,... of each window with a full 5-bar forward return in the window and a non-zero forecast; the coin's drift is the mean of all its grid 5-day returns over all windows; the slope comes from OLS with an intercept and its t uses standard errors clustered by UTC day.
- Size: unusual move +0.20 % (t 0.43, the cases of one day together: 646 days) per case over 5 bars, 0.019 of the coin's usual move (10.60 %); normal drift in its direction +0.00 %, total +0.20 %; 878 cases
Plan: `steps_cards/03_test_plan/night8_fallingcalm_run/plans/062-02_rising-volume-growth-stalls_1d.md`
Record: `steps_cards/04_backtest/night8_fallingcalm_run/backtests/062-02_rising-volume-growth-stalls_1d`
Measure: `measure.py`
