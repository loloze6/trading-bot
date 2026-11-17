---
brief: 010_rsi-midline-regime-direction
source-idea: 010-03_rsi-above-streak-continuation
line: 7.b inconclusive
backtest: 010-03_rsi-above-streak-continuation_1d
instruments: BTC, ETH, BNB
bar: 1d
period: folds A, B, C, D
---
Idea: The longer a coin's 14-day RSI has stayed above 50 without a break, measured in days up to the current close, the higher the coin's return over the next 7 days.
Consequence: A long unbroken stretch of RSI above 50 is a reason to hold the coin long for about a week, and a short or absent one is a reason not to.
Why:
- F3: The effect is clearer at shorter horizons on the same bars. At 3 days the slope t is 2.14 on 1,907 non-overlapping cases (on-minus-off Welch t 2.67). At 7 days it is 1.92 on 815 cases (Welch t 2.59). At 21 and 28 days it is 0.94 and 1.73.
- F2: Noise drowns the effect: the excess 14-day return's standard deviation is about 0.16 in every forecast bin, against a spread of about 0.05 between the bins' means (−0.024 to +0.027).
