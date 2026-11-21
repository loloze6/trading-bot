---
plan: 010-03_rsi-above-streak-continuation.e1_rsi-side-predicts-next-week_1d
idea: 010-03_rsi-above-streak-continuation.e1_rsi-side-predicts-next-week
fit: exact
status: not observable
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of forecast/10 x (coin 7-bar return - coin mean 7-bar return), non-overlapping cases: 0.0141339; ordinary t of the mean: 1.15233 (threshold: confirm: positive with t >= 2 and supporting difference positive; reject: negative with t <= -2 and supporting difference negative)
- Supporting check: mean excess 7-bar return forecast>0 minus forecast<0 (Welch t), same sign as main: 0.0222478, passed: True
- Counts: independent cases: 90, cases BTCUSD: 45, cases ETHUSD: 45, cases forecast > 0: 44, cases forecast < 0: 46
- Decided by: Only 90 independent cases across the coins, below the plan's minimum of 300.
- Reading: Non-overlapping cases are positions 0,7,14,... of each window with close[t+7] inside the window; each coin's mean 7-bar return is taken over these same cases in all its windows; cases with forecast 0 stay in the main measure (product 0) and are left out of both groups of the supporting check; the 300-case minimum counts all cases across coins.
Plan: `steps_cards/03_test_plan/hold2_rerun_run/plans/010-03_rsi-above-streak-continuation.e1_rsi-side-predicts-next-week_1d.md`
Record: `steps_cards/04_backtest/hold2_rerun_run/unseen_2026/backtests/010-03_rsi-above-streak-continuation.e1_rsi-side-predicts-next-week_1d`
Measure: `measure.py`
