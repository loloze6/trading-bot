---
plan: 010-03_rsi-above-streak-continuation.e1_rsi-side-predicts-next-week_1d
idea: 010-03_rsi-above-streak-continuation.e1_rsi-side-predicts-next-week
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of forecast/10 x (coin 7-bar return - coin mean 7-bar return), non-overlapping cases: 0.0148203; ordinary t of the mean: 4.78984 (threshold: confirm: positive with t >= 2 and supporting difference positive; reject: negative with t <= -2 and supporting difference negative)
- Supporting check: mean excess 7-bar return forecast>0 minus forecast<0 (Welch t), same sign as main: 0.0275265, passed: True
- Counts: independent cases: 4382, cases AAVEUSD: 238, cases ADAUSD: 357, cases AVAXUSD: 187, cases DOGEUSD: 289, cases INJUSD: 204, cases LINKUSD: 306, cases LTCUSD: 407, cases NEARUSD: 170, cases ONDOUSD: 68, cases SOLUSD: 221, cases SUIUSD: 119, cases TAOUSD: 68, cases TRXUSD: 272, cases UNIUSD: 255, cases XMRUSD: 407, cases XRPUSD: 407, cases ZECUSD: 407, cases forecast > 0: 2019, cases forecast < 0: 2363
- Decided by: The main measure is positive with t >= 2 and the supporting difference is positive.
- Reading: Non-overlapping cases are positions 0,7,14,... of each window with close[t+7] inside the window; each coin's mean 7-bar return is taken over these same cases in all its windows; cases with forecast 0 stay in the main measure (product 0) and are left out of both groups of the supporting check; the 300-case minimum counts all cases across coins.
- Size: unusual move +1.09 % (t 2.72, the cases of one day together: 1371 days) per case over 7 bars, 0.063 of the coin's usual move (14.35 %); normal drift in its direction -0.07 %, total +1.02 %; 4018 cases
- Direction check on folds A, D (the years step 7 does not explore): not judged: too few cases on the check folds (68 cases, None days)
Plan: `steps_cards/03_test_plan/hold_paying_run/plans/010-03_rsi-above-streak-continuation.e1_rsi-side-predicts-next-week_1d.md`
Record: `steps_cards/04_backtest/paying_rerun_run/unseen_coins/backtests/010-03_rsi-above-streak-continuation.e1_rsi-side-predicts-next-week_1d`
Measure: `measure.py`
