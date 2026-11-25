---
plan: 034-01.b1_nearness-to-high-10-days_1d
idea: 034-01.b1_nearness-to-high-10-days
fit: exact
status: confirmed
---
Situation check: 99 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled slope of excess 10-bar return on forecast, profile bars, non-overlapping grid: 0.00391004; OLS slope t: 3.18849 (threshold: slope t >= 2 (with top-minus-bottom > 0) confirms; t <= -2 rejects; at least 300 grid cases and 100 distinct grid days)
- Supporting check: mean excess return, top third minus bottom third by forecast: 0.0286737, passed: True
- Counts: grid cases inside the profile: 1417, distinct grid days: 222
- Decided by: The slope's t is 2 or more and the top-minus-bottom difference is positive: confirm.
- Reading: The coin's mean 10-bar return is the mean over all its non-overlapping grid cases in all windows (profile or not), the profile is bars with regime 'unknown' where near_high is recorded, the thirds are the n//3 lowest and highest grid cases by forecast (stable sort), and the expected side is the sign of the forecast rebuilt from raw component values (post-pipeline values where a window lacks a full standardise history).
- Size: unusual move +1.92 % (t 2.82, the cases of one day together: 742 days) per case over 10 bars, 0.113 of the coin's usual move (16.82 %); normal drift in its direction +0.47 %, total +2.39 %; 1528 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.003 on the check folds against +0.00391 on every fold
Plan: `steps_cards/03_test_plan/night7_rangefail_run/plans/034-01.b1_nearness-to-high-10-days_1d.md`
Record: `steps_cards/04_backtest/night7_rangefail_run/backtests/034-01.b1_nearness-to-high-10-days_1d`
Measure: `measure.py`
