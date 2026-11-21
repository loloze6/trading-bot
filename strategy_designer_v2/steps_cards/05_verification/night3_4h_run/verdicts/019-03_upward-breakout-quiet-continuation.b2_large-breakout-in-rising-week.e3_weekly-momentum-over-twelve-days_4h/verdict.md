---
plan: 019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.e3_weekly-momentum-over-twelve-days_4h
idea: 019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.e3_weekly-momentum-over-twelve-days
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t-statistic of the pooled slope of 72-bar drift-adjusted forward return on the forecast: 3.51008; OLS slope t: 3.51008 (threshold: confirm t >= 2 with per-coin check passing; reject t <= -2; otherwise inconclusive)
- Supporting check: coins with a positive per-coin slope (need >= 4 of 6): 6, passed: True
- Counts: grid cases with a non-zero forecast: 1403, grid cases: 1404, coins with a positive slope: 6, coins: 6
- Decided by: Pooled slope t >= 2 and the slope is positive for at least 4 of the 6 coins.
- Reading: Regression is OLS with intercept on all grid cases (forecast at the grid bar, zero forecasts included) with drift = the coin's mean non-overlapping 72-bar grid return over all its windows; the per-coin check counts coins with a positive slope against the fixed requirement of 4; grid cells without a full 72-bar forward return in the window are dropped.
- Size: unusual move +0.71 % per case over 72 bars, 0.035 of the coin's usual move (16.55 %); normal drift in its direction -0.11 %, total +0.60 %; 1393 cases
Plan: `steps_cards/03_test_plan/night3_4h_run/plans/019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.e3_weekly-momentum-over-twelve-days_4h.md`
Record: `steps_cards/04_backtest/night3_4h_run/backtests/019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.e3_weekly-momentum-over-twelve-days_4h`
Measure: `measure.py`
