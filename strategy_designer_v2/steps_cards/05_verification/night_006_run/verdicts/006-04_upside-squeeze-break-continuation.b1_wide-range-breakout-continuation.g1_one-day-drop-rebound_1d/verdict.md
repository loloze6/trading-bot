---
plan: 006-04_upside-squeeze-break-continuation.b1_wide-range-breakout-continuation.g1_one-day-drop-rebound_1d
idea: 006-04_upside-squeeze-break-continuation.b1_wide-range-breakout-continuation.g1_one-day-drop-rebound
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of next-day excess return on forecast (forecast > 0 bars, pooled): 0.000497696; OLS slope t: 5.93064 (threshold: confirm: slope > 0 with t >= 2 and timing gain > 0; reject: slope < 0 with t <= -2; at least 300 bars with forecast > 0)
- Supporting check: timing gain (book mean daily return minus market-rise gain): 0.000319833, passed: True
- Counts: bars with forecast > 0: 8514
- Decided by: The slope is positive with t >= 2 and the timing gain is above 0 (confirm rule).
- Reading: The slope is an ordinary least-squares fit with intercept of every forecast > 0 bar's next-day excess return (coin mean over all its within-window daily returns) on its forecast, its t being slope over the fit's standard error, and the plan's 'fewer than 300 is inconclusive' is reported as 'not observable' per the workflow's minimum-count rule.
- Size: unusual move +0.18 % per case over 1 bars, 0.038 of the coin's usual move (4.78 %); normal drift in its direction +0.12 %, total +0.30 %; 5650 cases
Plan: `steps_cards/03_test_plan/night_006_run/plans/006-04_upside-squeeze-break-continuation.b1_wide-range-breakout-continuation.g1_one-day-drop-rebound_1d.md`
Record: `steps_cards/04_backtest/night_006_run/backtests/006-04_upside-squeeze-break-continuation.b1_wide-range-breakout-continuation.g1_one-day-drop-rebound_1d`
Measure: `measure.py`
