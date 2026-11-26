---
plan: 031-01.g1.g1.g2.g1_thursday-close-trend-into-weekend_1d
idea: 031-01.g1.g1.g2.g1_thursday-close-trend-into-weekend
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of the 2-bar forward return minus the coin's mean 2-bar return, regressed on the forecast, on Thursday-close bars: 0.000570132; t of the OLS slope, clustered by Thursday date: 2.74183 (threshold: confirm: slope > 0 with t >= 2; reject: slope < 0 with t <= -2; over at least 100 distinct Thursdays)
- Supporting check: none
- Counts: distinct Thursdays: 411, cases (coin-Thursdays): 2465
- Decided by: The slope is positive with t >= 2 over at least 100 distinct Thursdays (the plan's confirm rule).
- Reading: A Thursday-close bar is a bar whose next daily bar starts on a Friday (UTC); the expected side is the sign of the recorded 14-bar return (recomputed from closes where not recorded); the coin's mean 2-bar return is taken on the non-overlapping grid of all its windows; every Thursday-close bar with a recorded forecast (zero included) and an in-window 2-bar return is a case; the t is an OLS slope t with standard errors clustered by Thursday date (small-sample correction G/(G-1)*(N-1)/(N-2)); fewer than 100 distinct Thursdays gives 'not observable'.
- Size: unusual move +0.51 % (t 2.25, the cases of one day together: 411 days) per case over 2 bars, 0.073 of the coin's usual move (6.58 %); normal drift in its direction -0.00 %, total +0.51 %; 2122 cases
Plan: `steps_cards/03_test_plan/night6_yearlow_run/plans/031-01.g1.g1.g2.g1_thursday-close-trend-into-weekend_1d.md`
Record: `steps_cards/04_backtest/night6_yearlow_run/backtests/031-01.g1.g1.g2.g1_thursday-close-trend-into-weekend_1d`
Measure: `measure.py`
