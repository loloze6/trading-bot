---
plan: 032-02_choppy-downside-break-rebounds_1d
idea: 032-02_choppy-downside-break-rebounds
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 5-bar move over the cases (long): -0.0239138; t of the mean, cases clustered by day: -1.26509 (threshold: confirm: mean > 0 with day-clustered t >= 2 and slope on forecast > 0; reject: mean < 0 with t <= -2)
- Supporting check: OLS slope of unusual move on forecast: -0.00098423, passed: False
- Counts: cases: 50, distinct days: 36
- Decided by: t lies between -2 and 2: inconclusive by the plan.
- Reading: Situation = recorded depth raw value (or its recomputation from prior 20 lows) below 0 on a bar whose regime is not the 'chop' veto, long side; a case is the first bet (forecast rise of >= 2 points from its lowest long level since the last bet, reset at flat) in each 5-bar grid cell of a window counted from its first row, needing close 5 bars later in the same window; drift = mean of the coin's non-overlapping 5-bar grid returns over all windows; t clusters cases by UTC day with a G/(G-1) correction.
- Size: unusual move -2.39 % (t -1.28, the cases of one day together: 36 days) per case over 5 bars, -0.266 of the coin's usual move (10.60 %); normal drift in its direction +0.57 %, total -1.82 %; 50 cases
Plan: `steps_cards/03_test_plan/night7_rangefail_run/plans/032-02_choppy-downside-break-rebounds_1d.md`
Record: `steps_cards/04_backtest/night7_rangefail_run/backtests/032-02_choppy-downside-break-rebounds_1d`
Measure: `measure.py`
