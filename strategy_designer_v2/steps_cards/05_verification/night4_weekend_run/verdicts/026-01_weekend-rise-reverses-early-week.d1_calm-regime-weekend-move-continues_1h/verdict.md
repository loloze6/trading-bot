---
plan: 026-01_weekend-rise-reverses-early-week.d1_calm-regime-weekend-move-continues_1h
idea: 026-01_weekend-rise-reverses-early-week.d1_calm-regime-weekend-move-continues
fit: exact
status: confirmed
---
Situation check: 99 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of (forecast/10) x (48-bar return minus coin's mean 48-bar return) over the bets: 0.00694393; t of the mean: 3.12648 (threshold: confirm: mean > 0 with t >= 2 over >= 100 cases; reject: mean < 0 with t <= -2 over >= 100 cases)
- Supporting check: none
- Counts: bets (trending, |forecast| >= 2): 1263, cases with a full 48 bars left inside their window: 1238
- Decided by: The mean is positive with t = 3.13 >= 2 over 1238 >= 100 cases (confirm rule).
- Reading: The bar 'closing at Monday 00:00 UTC' is the bar whose start timestamp plus one hour is Monday 00:00; the calm-volatility part of the situation is taken from the recorded regime ('trending') because the 720/4320-bar volatility ratio cannot be rebuilt inside one window; the side is the sign of the recorded 48-bar raw return (prices where missing); the coin's mean 48-bar return is taken on the non-overlapping grid of all its windows; cases are all trending bars with |forecast| >= 2 having 48 bars left in their window, each counted once.
- Size: unusual move +0.72 % per case over 48 bars, 0.101 of the coin's usual move (6.56 %); normal drift in its direction +0.03 %, total +0.75 %; 1230 cases
Plan: `steps_cards/03_test_plan/night4_weekend_run/plans/026-01_weekend-rise-reverses-early-week.d1_calm-regime-weekend-move-continues_1h.md`
Record: `steps_cards/04_backtest/night4_weekend_run/backtests/026-01_weekend-rise-reverses-early-week.d1_calm-regime-weekend-move-continues_1h`
Measure: `measure.py`
