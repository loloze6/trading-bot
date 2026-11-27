---
plan: 074-01.b1.g2_calm-downtrend-relief-fade_1d
idea: 074-01.b1.g2_calm-downtrend-relief-fade
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean short-signed next-day return minus the coin's mean daily return, on forecast < 0 bars: 0.00628636; t of the mean, cases of one day pooled: 2.38868 (threshold: confirm: mean > 0 with t >= 2 over at least 30 case-days; reject: mean < 0 with t <= -2)
- Supporting check: OLS slope of short-signed excess next-day return on depth last_history_value: 0.00548263, passed: True
- Counts: case-days: 286, cases: 465
- Decided by: The main mean is positive with t >= 2 over at least 30 case-days and the supporting slope is above 0.
- Reading: Situation checked from prices as an up close after at least 2 down closes inside the window, with short side (forecast < 0); the falling-calm profile is not recomputed (its 365-day volatility percentile needs history before each window) and active bars in a window's first 3 rows are left out of the check; case-days are distinct UTC dates, the t is clustered by day (deviations summed per day), the slope is OLS over all cases, and fewer than 30 case-days gives 'not observable' as the workflow's minimum-count rule requires.
- Size: unusual move +0.63 % (t 2.39, the cases of one day together: 286 days) per case over 1 bars, 0.134 of the coin's usual move (4.73 %); normal drift in its direction -0.13 %, total +0.50 %; 465 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.002493 on the check folds against +0.006286 on every fold
Plan: `steps_cards/03_test_plan/night9_fallcalmfade_run/plans/074-01.b1.g2_calm-downtrend-relief-fade_1d.md`
Record: `steps_cards/04_backtest/night9_fallcalmfade_run/backtests/074-01.b1.g2_calm-downtrend-relief-fade_1d`
Measure: `measure.py`
