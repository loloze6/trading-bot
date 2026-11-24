---
plan: 031-02.b1.b1.b1.g2_wide-day-after-long-climb_1d
idea: 031-02.b1.b1.b1.g2_wide-day-after-long-climb
fit: adapted
status: not observable
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of the slope of excess 3-bar return on forecast (day-clustered): 0.807097; day-clustered OLS slope t: 0.807097 (threshold: confirm if t >= 2 (with forecast-weighted mean excess > 0); reject if t <= -2)
- Supporting check: forecast-weighted mean excess 3-bar return > 0: 0.00774016, passed: True
- Counts: cases: 167, distinct days: 55
- Decided by: Minimum counts not reached: 167 cases (need 100) and 55 distinct days (need 60).
- Reading: Situation recomputed as (high-low) of bar t over the mean high-low of the 20 bars ending at t inside each window, on the active bars where it can be computed, with the expected side long and the raw 20-day rise positive where recorded; the slope's t is an OLS slope (with intercept) of excess 3-bar return on forecast with standard errors clustered by calendar day (scores summed per day, small-sample corrected), and the coin's mean 3-bar return is the mean over its non-overlapping 3-bar grid returns of all its windows.
- Size: unusual move +1.18 % (t 1.12, the cases of one day together: 125 days) per case over 3 bars, 0.137 of the coin's usual move (6.81 %); normal drift in its direction +0.10 %, total +1.28 %; 312 cases
Plan: `steps_cards/03_test_plan/night6_indecision_run/plans/031-02.b1.b1.b1.g2_wide-day-after-long-climb_1d.md`
Record: `steps_cards/04_backtest/night6_indecision_run/unseen_2026/backtests/031-02.b1.b1.b1.g2_wide-day-after-long-climb_1d`
Measure: `measure.py`
