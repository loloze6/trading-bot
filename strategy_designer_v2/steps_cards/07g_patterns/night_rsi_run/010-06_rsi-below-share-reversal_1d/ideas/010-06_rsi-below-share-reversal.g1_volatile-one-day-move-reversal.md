---
brief: 010_rsi-midline-regime-direction
source-idea: 010-06_rsi-below-share-reversal
line: 7.g patterns
backtest: 010-06_rsi-below-share-reversal_1d
instruments: BTC, ETH, BNB
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's 1-day return, the more its return over the next 1 day runs the other way, and this reversal grows with the coin's 30-day realised volatility.
Consequence: After a large daily move in a volatile market, a trader would lean against that move for the next day rather than follow it.
Why:
- F1: The day after a daily move, the coin tends to reverse it: regressing the next day's coin-demeaned return on today's return gives slope -0.0715 (t -5.44, n 5746). Each coin shows it on its own (BTC -0.067, t -3.62; ETH -0.074, t -3.98, n 2873 each). It holds after cutting the 1% tails (-0.043, t -2.76). The slope is negative in all 8 years, and in 36 of 48 coin-windows (75%, binomial p 0.0007).
- F2: The reversal comes almost entirely from high-volatility periods. In the top tercile of 30-day realised volatility the slope is -0.139 (t -5.84, n 1452). In the middle tercile it is -0.008 (t -0.30), and in the low tercile +0.017 (t 0.54).
- F4: The reversal lasts one day only. Today's return against the return two days ahead gives slope +0.009 (t 0.36, n 2835). The tested 30-day RSI-below share has no clear link to the next 14 days (slope -0.00118, t -1.65, n 384). The book lost money in every year (mean daily book return between -0.0003 and -0.0017).
