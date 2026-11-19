---
brief: 001_rsi-extremes-predict-next-move
source-idea: 001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-trend-continuation
line: 7.g patterns
backtest: 001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-trend-continuation_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The further a coin's price has fallen over the past 24 hours, the more it rises above its usual move over the next 1 day.
Consequence: Treat a sharp 1-day fall in these coins as a reason to buy for a 1-day rebound, and refuse to chase the fall with shorts.
Why:
- F1: The 1-day reversal after a large 1-day fall is the strongest pattern found and the tested idea does not explain it: on a non-overlapping 24-hour grid, bars in each coin's lowest decile of past 24-hour return were followed by a next-day return of +0.94% above the coin's usual move (t = 5.64, n = 1713); the highest decile was followed by −0.35% (t = −2.19, n = 1713) and the ninth by −0.22% (t = −2.01); the middle deciles were all within |t| < 1.6.
