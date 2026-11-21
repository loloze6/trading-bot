---
plan: 013-01_nearness-to-high-predicts-gains_1d
idea: 013-01_nearness-to-high-predicts-gains
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled slope of demeaned 30-bar forward return on forecast: 0.00470903; OLS slope t: 0.946734 (threshold: t >= 2 confirms (with timing gain > 0); t <= -2 rejects; otherwise inconclusive; >= 300 non-overlapping cases)
- Supporting check: book timing gain (mean daily, before costs): 9.79641e-05, passed: True
- Counts: non-overlapping 30-bar cases: 526
- Decided by: The slope's t lies between -2 and 2.
- Reading: Coin's mean 30-bar return taken as the mean of that coin's non-overlapping 30-bar samples over all its windows; slope is OLS with intercept on pooled samples at positions 0,30,60,90 with t+30 inside the window; timing gain uses position x next-bar return averaged across coins per date; the forecast's expected sign is rebuilt as the equal-weight mean of the components' post-pipeline values, since the 364-bar standardisation history is not in the record.
- Size: unusual move +6.26 % per case over 30 bars, 0.200 of the coin's usual move (25.51 %); normal drift in its direction +1.06 %, total +7.32 %; 214 cases
Plan: `steps_cards/03_test_plan/night_013_run/plans/013-01_nearness-to-high-predicts-gains_1d.md`
Record: `steps_cards/04_backtest/night_013_run/backtests/013-01_nearness-to-high-predicts-gains_1d`
Measure: `measure.py`
