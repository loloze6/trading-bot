---
plan: 010-03_rsi-above-streak-continuation.e1_rsi-side-predicts-next-week_1d
idea: 010-03_rsi-above-streak-continuation.e1_rsi-side-predicts-next-week
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of forecast/10 x (coin 7-bar return - coin mean 7-bar return), non-overlapping cases: 0.0134365; ordinary t of the mean: 2.92925 (threshold: confirm: positive with t >= 2 and supporting difference positive; reject: negative with t <= -2 and supporting difference negative)
- Supporting check: mean excess 7-bar return forecast>0 minus forecast<0 (Welch t), same sign as main: 0.0200565, passed: True
- Counts: independent cases: 815, cases BTCUSD: 408, cases ETHUSD: 407, cases forecast > 0: 410, cases forecast < 0: 405
- Decided by: The main measure is positive with t >= 2 and the supporting difference is positive.
- Reading: Non-overlapping cases are positions 0,7,14,... of each window with close[t+7] inside the window; each coin's mean 7-bar return is taken over these same cases in all its windows; cases with forecast 0 stay in the main measure (product 0) and are left out of both groups of the supporting check; the 300-case minimum counts all cases across coins.
Plan: `steps_cards/03_test_plan/night_rsi_run/plans/010-03_rsi-above-streak-continuation.e1_rsi-side-predicts-next-week_1d.md`
Record: `steps_cards/04_backtest/night_rsi_run/backtests/010-03_rsi-above-streak-continuation.e1_rsi-side-predicts-next-week_1d`
Measure: `measure.py`
