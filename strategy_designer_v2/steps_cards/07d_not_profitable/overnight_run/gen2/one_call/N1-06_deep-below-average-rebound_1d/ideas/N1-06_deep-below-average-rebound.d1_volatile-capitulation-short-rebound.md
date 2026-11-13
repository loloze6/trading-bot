---
brief: 002_moving-average-cross-trend-persistence
source-idea: N1-06_deep-below-average-rebound
line: 7.d not profitable
backtest: N1-06_deep-below-average-rebound_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's close falls to an extreme distance below its 200-day average while its recent daily volatility is above its usual level (a capitulation), its price rises over the next one to two weeks more than its normal drift.
Consequence: Buy only extreme, high-volatility plunges below the long average and refuse the calm, moderate-depth cases that make up most of the current exposure.
Why:
- F3: The forecast barely separates outcomes. On non-overlapping 10-bar returns minus each coin's mean, every active bucket from forecast 0 to 10 is negative: -0.73 % (n=386, t=-1.01), -0.97 % (n=168, t=-0.94), -0.80 % (n=69) and -0.51 % (n=99). Only forecast 10–20 is positive, at +2.44 % (n=102, t=1.37).
- F5: The rebound appears only in the volatile state. Active bars with 20-day volatility above its 200-day median earn +0.74 % excess over 10 bars (n=140, t=0.68), while calm active bars lose -0.58 % (n=701, t=-1.07).
- F1: The book is long-only and fees are not what hurts it: 1030 trades earn a mean of +2.13 % before fees against 0.23 % commission, +2.03 % after fees, and 68.8 % of them win before fees.
