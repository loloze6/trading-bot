---
brief: 024_exhaustion-after-an-extended-run
source-idea: 024-01_fading-volume-uprun-giveback-size.d1_up-streak-continuation-by-size
line: 7.g patterns
backtest: 024-01_fading-volume-uprun-giveback-size.d1_up-streak-continuation-by-size_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: The larger a coin's 7-day return measured in its usual 4-hour moves over the past 30 days, the further it moves in the same direction over the next 3 days, beyond its normal drift.
Consequence: A strong 7-day run, up or down, is a reason to trade with it for three days rather than against it.
Why:
- F1: A coin's 7-day return, measured in its usual moves, predicts its excess return over the next 3 days in the same direction. The pooled slope has t 3.85 on 5148 non-overlapping cases. The top quintile minus the bottom quintile is +0.122 standard deviations (Welch t 2.52), the top quintile alone is +0.098 (t 2.77), and the slope is positive in 5 of 6 coins (XRP t 3.33) and in 7 of 8 years (2022 t -1.45).
- F3: In up-streaks, fading volume makes no difference to the next 3 days: rising minus fading is +0.039 standard deviations (t 0.70, n 1323). The brief's give-back after up-runs on fading volume does not appear, and neither does the tested continuation: the main t is 1.21 and the unusual move is -0.09 % per case, -0.4 times the 0.19 % cost of a trade.
