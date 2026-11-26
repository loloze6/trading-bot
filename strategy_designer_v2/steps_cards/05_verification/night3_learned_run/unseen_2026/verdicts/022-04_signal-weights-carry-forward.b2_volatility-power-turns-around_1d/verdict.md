---
plan: 022-04_signal-weights-carry-forward.b2_volatility-power-turns-around_1d
idea: 022-04_signal-weights-carry-forward.b2_volatility-power-turns-around
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean timing gain per case, 5-bar non-overlapping grid, before costs: 0.0034417; ordinary t of the mean: 1.06186 (threshold: confirm: mean > 0 with t >= 2 (and supporting check); reject: mean < 0 with t <= -2)
- Supporting check: mean timing gain positive in at least 4 of the 6 coins: 4, passed: True
- Counts: non-overlapping cases across all coins and windows: 352, cases BTCUSD: 50, cases ETHUSD: 62, cases LTCUSD: 58, cases XMRUSD: 61, cases XRPUSD: 62, cases ZECUSD: 59, coins with positive mean timing gain: 4
- Decided by: t between -2 and 2.
- Reading: A case is a grid bar (positions 0,5,10,... of each window) with non-zero post-trade position and a full 5-bar forward return inside the window; the coin's mean 5-bar return is the mean over the same grid in all its windows; a coin with no cases counts as not positive; the plan's 'fewer than 300 cases' is reported as not observable, per the workflow's rule on minimum counts; the situation check counts active bars with non-zero raw value whose forecast sign is opposite to it.
- Size: unusual move +0.99 % (t 1.32, the cases of one day together: 114 days) per case over 5 bars, 0.083 of the coin's usual move (8.48 %); normal drift in its direction -0.16 %, total +0.83 %; 151 cases
Plan: `steps_cards/03_test_plan/night3_learned_run/plans/022-04_signal-weights-carry-forward.b2_volatility-power-turns-around_1d.md`
Record: `steps_cards/04_backtest/night3_learned_run/unseen_2026/backtests/022-04_signal-weights-carry-forward.b2_volatility-power-turns-around_1d`
Measure: `measure.py`
