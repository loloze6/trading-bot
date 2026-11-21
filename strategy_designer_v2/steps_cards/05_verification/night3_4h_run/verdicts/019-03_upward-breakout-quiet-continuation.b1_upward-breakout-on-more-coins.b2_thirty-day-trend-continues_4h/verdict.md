---
plan: 019-03_upward-breakout-quiet-continuation.b1_upward-breakout-on-more-coins.b2_thirty-day-trend-continues_4h
idea: 019-03_upward-breakout-quiet-continuation.b1_upward-breakout-on-more-coins.b2_thirty-day-trend-continues
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled OLS slope of the 18-bar forward return minus the coin's mean 18-bar return, on the forecast: 0.00085577; OLS slope t: 6.89291 (threshold: confirm: slope > 0 with t >= 2; reject: slope < 0 with t <= -2; at least 300 grid cases with forecast > 0)
- Supporting check: none
- Counts: grid cases with forecast > 0: 5939, grid cases: 12166
- Decided by: The slope is positive with t >= 2, over at least 300 grid cases with forecast > 0.
- Reading: The regression is pooled OLS with an intercept over all grid cases, flat cases included, with the drift taken as each coin's mean 18-bar grid return over all its windows; following the workflow, fewer than 300 grid cases with forecast > 0 is reported as 'not observable'.
- Size: unusual move +0.48 % per case over 18 bars, 0.050 of the coin's usual move (9.29 %); normal drift in its direction +0.52 %, total +1.00 %; 5050 cases
Plan: `steps_cards/03_test_plan/night3_4h_run/plans/019-03_upward-breakout-quiet-continuation.b1_upward-breakout-on-more-coins.b2_thirty-day-trend-continues_4h.md`
Record: `steps_cards/04_backtest/night3_4h_run/backtests/019-03_upward-breakout-quiet-continuation.b1_upward-breakout-on-more-coins.b2_thirty-day-trend-continues_4h`
Measure: `measure.py`
