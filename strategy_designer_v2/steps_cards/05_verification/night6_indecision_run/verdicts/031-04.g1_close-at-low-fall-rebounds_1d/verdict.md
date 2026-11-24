---
plan: 031-04.g1_close-at-low-fall-rebounds_1d
idea: 031-04.g1_close-at-low-fall-rebounds
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of next-day excess return on near_low post-pipeline value: 0.00191179; t of the slope, clustered by day: 2.60483 (threshold: confirm if t >= 2 (with supporting check), reject if t <= -2)
- Supporting check: mean unusual next-day move (long) of cases with forecast >= 2: 0.00723052, passed: True
- Counts: sharp-down-day cases: 492, days: 200, cases with forecast >= 2: 478
- Decided by: The slope's t is 2 or more and the mean unusual move of the cases with forecast >= 2 is above 0.
- Reading: The situation is a 1-day return at or below -2 times the std (ddof 1) of the last 20 daily returns of the window, taking either the std including or excluding the bar, and active bars of a window's first 20 bars where it cannot be computed are left out of the agreement; cases are bars with regime mean_reversion and a next-day return inside the window, the slope t is OLS with standard errors clustered by UTC day (small-sample corrected), and the supporting check uses the forecast column >= 2.
- Size: unusual move +0.60 % (t 1.10, the cases of one day together: 194 days) per case over 1 bars, 0.128 of the coin's usual move (4.78 %); normal drift in its direction +0.12 %, total +0.72 %; 457 cases
Plan: `steps_cards/03_test_plan/night6_indecision_run/plans/031-04.g1_close-at-low-fall-rebounds_1d.md`
Record: `steps_cards/04_backtest/night6_indecision_run/backtests/031-04.g1_close-at-low-fall-rebounds_1d`
Measure: `measure.py`
