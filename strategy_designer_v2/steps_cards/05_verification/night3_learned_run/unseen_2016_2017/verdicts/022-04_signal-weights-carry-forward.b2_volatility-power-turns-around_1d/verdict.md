---
plan: 022-04_signal-weights-carry-forward.b2_volatility-power-turns-around_1d
idea: 022-04_signal-weights-carry-forward.b2_volatility-power-turns-around
fit: exact
status: not observable
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean timing gain per case, 5-bar non-overlapping grid, before costs: -0.00129735; ordinary t of the mean: -0.377126 (threshold: confirm: mean > 0 with t >= 2 (and supporting check); reject: mean < 0 with t <= -2)
- Supporting check: mean timing gain positive in at least 4 of the 6 coins: 1, passed: False
- Counts: non-overlapping cases across all coins and windows: 211, cases BTCUSD: 117, cases ETHUSD: 43, cases LTCUSD: 51, coins with positive mean timing gain: 1
- Decided by: Only 211 non-overlapping cases, below the plan's minimum of 300.
- Reading: A case is a grid bar (positions 0,5,10,... of each window) with non-zero post-trade position and a full 5-bar forward return inside the window; the coin's mean 5-bar return is the mean over the same grid in all its windows; a coin with no cases counts as not positive; the plan's 'fewer than 300 cases' is reported as not observable, per the workflow's rule on minimum counts; the situation check counts active bars with non-zero raw value whose forecast sign is opposite to it.
- Size: unusual move +0.07 % (t 0.06, the cases of one day together: 114 days) per case over 5 bars, 0.061 of the coin's usual move (17.00 %); normal drift in its direction -0.42 %, total -0.35 %; 128 cases
Plan: `steps_cards/03_test_plan/night3_learned_run/plans/022-04_signal-weights-carry-forward.b2_volatility-power-turns-around_1d.md`
Record: `steps_cards/04_backtest/night3_learned_run/unseen_2016_2017/backtests/022-04_signal-weights-carry-forward.b2_volatility-power-turns-around_1d`
Measure: `measure.py`
