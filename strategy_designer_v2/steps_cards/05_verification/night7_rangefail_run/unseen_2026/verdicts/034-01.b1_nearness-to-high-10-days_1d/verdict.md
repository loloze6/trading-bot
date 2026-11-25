---
plan: 034-01.b1_nearness-to-high-10-days_1d
idea: 034-01.b1_nearness-to-high-10-days
fit: exact
status: not observable
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled slope of excess 10-bar return on forecast, profile bars, non-overlapping grid: 0.00352771; OLS slope t: 1.51783 (threshold: slope t >= 2 (with top-minus-bottom > 0) confirms; t <= -2 rejects; at least 300 grid cases and 100 distinct grid days)
- Supporting check: mean excess return, top third minus bottom third by forecast: 0.0567207, passed: True
- Counts: grid cases inside the profile: 178, distinct grid days: 24
- Decided by: Minimum count not reached: 178 grid cases inside the profile (300 needed) and 24 distinct grid days (100 needed).
- Reading: The coin's mean 10-bar return is the mean over all its non-overlapping grid cases in all windows (profile or not), the profile is bars with regime 'unknown' where near_high is recorded, the thirds are the n//3 lowest and highest grid cases by forecast (stable sort), and the expected side is the sign of the forecast rebuilt from raw component values (post-pipeline values where a window lacks a full standardise history).
- Size: unusual move +1.31 % (t 0.74, the cases of one day together: 100 days) per case over 10 bars, 0.070 of the coin's usual move (11.10 %); normal drift in its direction +0.31 %, total +1.62 %; 195 cases
Plan: `steps_cards/03_test_plan/night7_rangefail_run/plans/034-01.b1_nearness-to-high-10-days_1d.md`
Record: `steps_cards/04_backtest/night7_rangefail_run/unseen_2026/backtests/034-01.b1_nearness-to-high-10-days_1d`
Measure: `measure.py`
