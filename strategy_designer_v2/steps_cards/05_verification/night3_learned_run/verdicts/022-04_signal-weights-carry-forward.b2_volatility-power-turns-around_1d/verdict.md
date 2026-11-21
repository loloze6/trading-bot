---
plan: 022-04_signal-weights-carry-forward.b2_volatility-power-turns-around_1d
idea: 022-04_signal-weights-carry-forward.b2_volatility-power-turns-around
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean timing gain per case, 5-bar non-overlapping grid, before costs: 0.00294351; ordinary t of the mean: 2.99013 (threshold: confirm: mean > 0 with t >= 2 (and supporting check); reject: mean < 0 with t <= -2)
- Supporting check: mean timing gain positive in at least 4 of the 6 coins: 6, passed: True
- Counts: non-overlapping cases across all coins and windows: 3068, cases BTCUSD: 561, cases ETHUSD: 565, cases LTCUSD: 536, cases XMRUSD: 510, cases XRPUSD: 397, cases ZECUSD: 499, coins with positive mean timing gain: 6
- Decided by: Mean timing gain above 0 with t >= 2 and positive in at least 4 of the 6 coins.
- Reading: A case is a grid bar (positions 0,5,10,... of each window) with non-zero post-trade position and a full 5-bar forward return inside the window; the coin's mean 5-bar return is the mean over the same grid in all its windows; a coin with no cases counts as not positive; the plan's 'fewer than 300 cases' is reported as not observable, per the workflow's rule on minimum counts; the situation check counts active bars with non-zero raw value whose forecast sign is opposite to it.
- Size: unusual move +0.12 % per case over 5 bars, 0.004 of the coin's usual move (10.60 %); normal drift in its direction -0.05 %, total +0.07 %; 1253 cases
Plan: `steps_cards/03_test_plan/night3_learned_run/plans/022-04_signal-weights-carry-forward.b2_volatility-power-turns-around_1d.md`
Record: `steps_cards/04_backtest/night3_learned_run/backtests/022-04_signal-weights-carry-forward.b2_volatility-power-turns-around_1d`
Measure: `measure.py`
