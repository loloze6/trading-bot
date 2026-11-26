---
plan: 054-01_deep-reclaimed-low-pierce-rebound_1d
idea: 054-01_deep-reclaimed-low-pierce-rebound
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 5-bar move of the cases (return minus coin's normal 5-bar drift): 0.0159134; t of the mean, cases of one day taken together: 0.916514 (threshold: mean > 0 with t >= 2 (confirm, with positive depth slope); mean < 0 with t <= -2 (reject))
- Supporting check: OLS slope of the unusual 5-bar move on the forecast at the signal bar: 0.0119329, passed: True
- Counts: cases: 75, distinct days: 50
- Decided by: The t of the mean unusual move lies between -2 and 2, which the plan calls inconclusive.
- Reading: Cases are long bets (forecast rise >= 2 points from its lowest level since the last bet, reset at flat), the first per 5-bar grid cell counted from each window's first row, with the 5-bar return inside the window minus the coin's mean non-overlapping 5-bar return over all its windows; the t sums deviations per signal day (cluster standard error with D/(D-1)); the situation check reads the agitated part of the profile from the recorded regime since a 365-bar percentile cannot be rebuilt inside a window.
- Size: unusual move +1.59 % (t 0.93, the cases of one day together: 50 days) per case over 5 bars, 0.151 of the coin's usual move (10.60 %); normal drift in its direction +0.64 %, total +2.23 %; 75 cases
Plan: `steps_cards/03_test_plan/pilot_panic_run/plans/054-01_deep-reclaimed-low-pierce-rebound_1d.md`
Record: `steps_cards/04_backtest/pilot_panic_run/backtests/054-01_deep-reclaimed-low-pierce-rebound_1d`
Measure: `measure.py`
