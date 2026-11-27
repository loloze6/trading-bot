---
plan: 010-03_rsi-above-streak-continuation.e1_rsi-side-predicts-next-week_1d
idea: 010-03_rsi-above-streak-continuation.e1_rsi-side-predicts-next-week
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of forecast/10 x (coin 7-bar return - coin mean 7-bar return), non-overlapping cases: 0.0146162; ordinary t of the mean: 6.18191 (threshold: confirm: positive with t >= 2 and supporting difference positive; reject: negative with t <= -2 and supporting difference negative)
- Supporting check: mean excess 7-bar return forecast>0 minus forecast<0 (Welch t), same sign as main: 0.0240599, passed: True
- Counts: independent cases: 7849, cases AAVEUSD: 272, cases ADAUSD: 391, cases ALGOUSD: 306, cases ATOMUSD: 357, cases AVAXUSD: 221, cases BCHUSD: 442, cases BTCUSD: 544, cases CRVUSD: 272, cases DOGEUSD: 323, cases DOTUSD: 289, cases ETHUSD: 543, cases FILUSD: 272, cases GRTUSD: 272, cases INJUSD: 238, cases LDOUSD: 187, cases LTCUSD: 543, cases NEARUSD: 187, cases ONDOUSD: 102, cases PEPEUSD: 136, cases SUIUSD: 153, cases TAOUSD: 85, cases TRXUSD: 306, cases XMRUSD: 475, cases XRPUSD: 458, cases ZECUSD: 475, cases forecast > 0: 3524, cases forecast < 0: 4325
- Decided by: The main measure is positive with t >= 2 and the supporting difference is positive.
- Reading: Non-overlapping cases are positions 0,7,14,... of each window with close[t+7] inside the window; each coin's mean 7-bar return is taken over these same cases in all its windows; cases with forecast 0 stay in the main measure (product 0) and are left out of both groups of the supporting check; the 300-case minimum counts all cases across coins.
- Size: unusual move +1.08 % (t 3.03, the cases of one day together: 1927 days) per case over 7 bars, 0.069 of the coin's usual move (14.68 %); normal drift in its direction -0.03 %, total +1.05 %; 7124 cases
- Direction check on folds A, D (the years step 7 does not explore): not judged: no check fold (the plan has none, or the backtest did not run on its folds)
Plan: `steps_cards/03_test_plan/hold2_rerun_run/plans/010-03_rsi-above-streak-continuation.e1_rsi-side-predicts-next-week_1d.md`
Record: `steps_cards/04_backtest/paying_rerun_run/common/backtests/010-03_rsi-above-streak-continuation.e1_rsi-side-predicts-next-week_1d`
Measure: `measure.py`
