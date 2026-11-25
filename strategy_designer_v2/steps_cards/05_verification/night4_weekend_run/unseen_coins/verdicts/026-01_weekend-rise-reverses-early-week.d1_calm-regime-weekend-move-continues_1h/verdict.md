---
plan: 026-01_weekend-rise-reverses-early-week.d1_calm-regime-weekend-move-continues_1h
idea: 026-01_weekend-rise-reverses-early-week.d1_calm-regime-weekend-move-continues
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of (forecast/10) x (48-bar return minus coin's mean 48-bar return) over the bets: -0.000321739; t of the mean: -0.148484 (threshold: confirm: mean > 0 with t >= 2 over >= 100 cases; reject: mean < 0 with t <= -2 over >= 100 cases)
- Supporting check: none
- Counts: bets (trending, |forecast| >= 2): 1259, cases with a full 48 bars left inside their window: 1240
- Decided by: The t of the mean (-0.15) lies between -2 and 2 over 1240 cases (inconclusive rule).
- Reading: The bar 'closing at Monday 00:00 UTC' is the bar whose start timestamp plus one hour is Monday 00:00; the calm-volatility part of the situation is taken from the recorded regime ('trending') because the 720/4320-bar volatility ratio cannot be rebuilt inside one window; the side is the sign of the recorded 48-bar raw return (prices where missing); the coin's mean 48-bar return is taken on the non-overlapping grid of all its windows; cases are all trending bars with |forecast| >= 2 having 48 bars left in their window, each counted once.
- Size: unusual move +0.20 % (t 0.57, the cases of one day together: 259 days) per case over 48 bars, 0.020 of the coin's usual move (7.40 %); normal drift in its direction +0.01 %, total +0.21 %; 1239 cases
Plan: `steps_cards/03_test_plan/night4_weekend_run/plans/026-01_weekend-rise-reverses-early-week.d1_calm-regime-weekend-move-continues_1h.md`
Record: `steps_cards/04_backtest/night4_weekend_run/unseen_coins/backtests/026-01_weekend-rise-reverses-early-week.d1_calm-regime-weekend-move-continues_1h`
Measure: `measure.py`
