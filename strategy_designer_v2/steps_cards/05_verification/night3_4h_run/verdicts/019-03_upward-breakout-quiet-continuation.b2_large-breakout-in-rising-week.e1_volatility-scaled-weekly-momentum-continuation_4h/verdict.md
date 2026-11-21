---
plan: 019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.e1_volatility-scaled-weekly-momentum-continuation_4h
idea: 019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.e1_volatility-scaled-weekly-momentum-continuation
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of 18-bar forward return minus coin mean, regressed on forecast: 0.000314826; OLS t of slope: 3.34185 (threshold: t >= 2 over at least 300 non-overlapping cases confirms (with timing gain > 0); t <= -2 rejects)
- Supporting check: book's timing gain before costs (mean daily): 0.000635517, passed: True
- Counts: non-overlapping cases: 5724
- Decided by: The slope's t is 2 or more over at least 300 non-overlapping cases and the timing gain before costs is above 0.
- Reading: The regression is OLS with an intercept on all grid bars (forecast zero included), the coin's mean 18-bar return is taken over its grid samples of all windows, and the gross daily book return compounds each bar's position gain between consecutive days' last bars, with the market part as the day's mean position times the coin's mean daily return over all windows.
- Size: unusual move +0.17 % per case over 18 bars, 0.017 of the coin's usual move (8.17 %); normal drift in its direction +0.01 %, total +0.18 %; 5544 cases
Plan: `steps_cards/03_test_plan/night3_4h_run/plans/019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.e1_volatility-scaled-weekly-momentum-continuation_4h.md`
Record: `steps_cards/04_backtest/night3_4h_run/backtests/019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.e1_volatility-scaled-weekly-momentum-continuation_4h`
Measure: `measure.py`
