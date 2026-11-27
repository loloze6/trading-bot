---
plan: 031-02.b1.b1.b1.g2_wide-day-after-long-climb_1d
idea: 031-02.b1.b1.b1.g2_wide-day-after-long-climb
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of the slope of excess 3-bar return on forecast (day-clustered): 3.23034; day-clustered OLS slope t: 3.23034 (threshold: confirm if t >= 2 (with forecast-weighted mean excess > 0); reject if t <= -2)
- Supporting check: forecast-weighted mean excess 3-bar return > 0: 0.0251416, passed: True
- Counts: cases: 1782, distinct days: 582
- Decided by: The slope's t is >= 2 and the forecast-weighted mean excess return is above 0.
- Reading: Situation recomputed as (high-low) of bar t over the mean high-low of the 20 bars ending at t inside each window, on the active bars where it can be computed, with the expected side long and the raw 20-day rise positive where recorded; the slope's t is an OLS slope (with intercept) of excess 3-bar return on forecast with standard errors clustered by calendar day (scores summed per day, small-sample corrected), and the coin's mean 3-bar return is the mean over its non-overlapping 3-bar grid returns of all its windows.
- Size: unusual move +1.45 % (t 4.17, the cases of one day together: 1266 days) per case over 3 bars, 0.142 of the coin's usual move (9.27 %); normal drift in its direction +0.47 %, total +1.92 %; 3024 cases
- Direction check on folds A, D (the years step 7 does not explore): not judged: no check fold (the plan has none, or the backtest did not run on its folds)
Plan: `steps_cards/03_test_plan/night6_indecision_run/plans/031-02.b1.b1.b1.g2_wide-day-after-long-climb_1d.md`
Record: `steps_cards/04_backtest/night6_indecision_run/common/backtests/031-02.b1.b1.b1.g2_wide-day-after-long-climb_1d`
Measure: `measure.py`
