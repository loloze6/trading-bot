---
plan: 010-03_rsi-above-streak-continuation.e1_rsi-side-predicts-next-week_1d
idea: 010-03_rsi-above-streak-continuation.e1_rsi-side-predicts-next-week
fit: exact
status: not observable
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of forecast/10 x (coin 7-bar return - coin mean 7-bar return), non-overlapping cases: 0.0397942; ordinary t of the mean: 2.24779 (threshold: confirm: positive with t >= 2 and supporting difference positive; reject: negative with t <= -2 and supporting difference negative)
- Supporting check: mean excess 7-bar return forecast>0 minus forecast<0 (Welch t), same sign as main: 0.0741048, passed: True
- Counts: independent cases: 204, cases BTCUSD: 102, cases ETHUSD: 102, cases forecast > 0: 142, cases forecast < 0: 62
- Decided by: Only 204 independent cases across the coins, below the plan's minimum of 300.
- Reading: Non-overlapping cases are positions 0,7,14,... of each window with close[t+7] inside the window; each coin's mean 7-bar return is taken over these same cases in all its windows; cases with forecast 0 stay in the main measure (product 0) and are left out of both groups of the supporting check; the 300-case minimum counts all cases across coins.
Plan: `steps_cards/03_test_plan/hold2_rerun_run/plans/010-03_rsi-above-streak-continuation.e1_rsi-side-predicts-next-week_1d.md`
Record: `steps_cards/04_backtest/hold2_rerun_run/unseen_2016_2017/backtests/010-03_rsi-above-streak-continuation.e1_rsi-side-predicts-next-week_1d`
Measure: `measure.py`
