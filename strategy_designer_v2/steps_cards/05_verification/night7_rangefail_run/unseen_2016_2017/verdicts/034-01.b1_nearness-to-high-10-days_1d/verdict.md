---
plan: 034-01.b1_nearness-to-high-10-days_1d
idea: 034-01.b1_nearness-to-high-10-days
fit: exact
status: not observable
---
Situation check: 99 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled slope of excess 10-bar return on forecast, profile bars, non-overlapping grid: 0.0116983; OLS slope t: 2.51791 (threshold: slope t >= 2 (with top-minus-bottom > 0) confirms; t <= -2 rejects; at least 300 grid cases and 100 distinct grid days)
- Supporting check: mean excess return, top third minus bottom third by forecast: 0.121346, passed: True
- Counts: grid cases inside the profile: 174, distinct grid days: 66
- Decided by: Minimum count not reached: 174 grid cases inside the profile (300 needed) and 66 distinct grid days (100 needed).
- Reading: The coin's mean 10-bar return is the mean over all its non-overlapping grid cases in all windows (profile or not), the profile is bars with regime 'unknown' where near_high is recorded, the thirds are the n//3 lowest and highest grid cases by forecast (stable sort), and the expected side is the sign of the forecast rebuilt from raw component values (post-pipeline values where a window lacks a full standardise history).
- Size: unusual move +7.21 % (t 2.79, the cases of one day together: 142 days) per case over 10 bars, 0.310 of the coin's usual move (30.80 %); normal drift in its direction +5.27 %, total +12.49 %; 177 cases
Plan: `steps_cards/03_test_plan/night7_rangefail_run/plans/034-01.b1_nearness-to-high-10-days_1d.md`
Record: `steps_cards/04_backtest/night7_rangefail_run/unseen_2016_2017/backtests/034-01.b1_nearness-to-high-10-days_1d`
Measure: `measure.py`
