---
plan: 022-04_signal-weights-carry-forward.b2_volatility-power-turns-around_1d
idea: 022-04_signal-weights-carry-forward.b2_volatility-power-turns-around
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean timing gain per case, 5-bar non-overlapping grid, before costs: 0.000806812; ordinary t of the mean: 0.63477 (threshold: confirm: mean > 0 with t >= 2 (and supporting check); reject: mean < 0 with t <= -2)
- Supporting check: mean timing gain positive in at least 4 of the 6 coins: 6, passed: True
- Counts: non-overlapping cases across all coins and windows: 2477, cases AAVEUSD: 228, cases ADAUSD: 396, cases AVAXUSD: 161, cases DOGEUSD: 297, cases INJUSD: 190, cases LINKUSD: 330, cases NEARUSD: 107, cases SOLUSD: 184, cases SUIUSD: 71, cases TRXUSD: 284, cases UNIUSD: 229, coins with positive mean timing gain: 6
- Decided by: t between -2 and 2.
- Reading: A case is a grid bar (positions 0,5,10,... of each window) with non-zero post-trade position and a full 5-bar forward return inside the window; the coin's mean 5-bar return is the mean over the same grid in all its windows; a coin with no cases counts as not positive; the plan's 'fewer than 300 cases' is reported as not observable, per the workflow's rule on minimum counts; the situation check counts active bars with non-zero raw value whose forecast sign is opposite to it.
- Size: unusual move +0.89 % (t 2.19, the cases of one day together: 619 days) per case over 5 bars, 0.079 of the coin's usual move (11.97 %); normal drift in its direction -0.05 %, total +0.84 %; 974 cases
Plan: `steps_cards/03_test_plan/night3_learned_run/plans/022-04_signal-weights-carry-forward.b2_volatility-power-turns-around_1d.md`
Record: `steps_cards/04_backtest/night3_learned_run/unseen_coins/backtests/022-04_signal-weights-carry-forward.b2_volatility-power-turns-around_1d`
Measure: `measure.py`
