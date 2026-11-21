---
plan: 001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-uptrend-continuation_1h
idea: 001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-uptrend-continuation
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of slope of excess 240-bar forward return on forecast, trending grid bars pooled: 3.39753; OLS slope t: 3.39753 (threshold: confirm: slope > 0 with t >= 2 and top-third check passes; reject: slope < 0 with t <= -2)
- Supporting check: mean excess 240-bar return of top-third forecast cases > 0: 0.0321349, passed: True
- Counts: independent trending cases: 841
- Decided by: The slope is positive with t >= 2 and the top-third mean excess return is above 0.
- Reading: Cases are rows at positions 0, 240, 480, ... of each window with regime 'trending' and a full 240-bar forward return inside the window; the coin's mean 240-bar return is the mean over all such grid bars of all its windows; the top third is the n//3 cases with the largest forecast; the plan's 'fewer than 100 cases' is reported as not observable; the situation check reads RSI as 50 minus the raw component value.
- Size: unusual move +1.04 % per case over 240 bars, 0.063 of the coin's usual move (14.43 %); normal drift in its direction +0.47 %, total +1.51 %; 1111 cases
Plan: `steps_cards/03_test_plan/retest_1h_run/plans/001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-uptrend-continuation_1h.md`
Record: `steps_cards/04_backtest/retest_1h_run/backtests/001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-uptrend-continuation_1h`
Measure: `measure.py`
