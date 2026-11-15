---
brief: 001_rsi-extremes-predict-next-move
source-idea: 001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample
line: 7.c rejected
backtest: 001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The higher a coin's 14-day RSI stands above 50, the more its price rises above its usual move over the next 10 days, most strongly while its 60-day return is positive.
Consequence: Treat extreme overbought RSI on these coins as a reason to stay long or add, not to short, and refuse RSI-based shorts in uptrends.
Why:
- F1: The idea was rejected because the market did the opposite of the forecast: at the extreme high-RSI cases (forecast ≤ -5), the 5-bar return beat the coin's average by +0.0129 (t 2.26, 523 non-overlapping cases), and the 10-bar return beat it by +0.0318 (t 2.36, 254 cases); the verdict's own count was +0.0144 (t 2.58, 595 cases), with only 1 of 6 coins negative.
- F2: The effect grows with how strong the reading is: the most extreme quartile of short forecasts (mean forecast -17.6) beat the average by +0.0136 over 5 bars (t 2.08, n 355) and by +0.0346 over 10 bars (t 2.30, n 176); this falls through q2 (+0.0052 / +0.0231) to the mildest quartile (-0.0035 / -0.0075).
- F4: Continuation is clearest inside a 60-day uptrend: with the 60-day return positive and RSI above 70, the 10-bar return beat the average by +0.060 (t 2.37, n 61), while with the 60-day return negative and RSI between 40 and 50 it lagged by -0.0239 (t -2.25, n 163).
- F6: The book lost because it was short into rising coins: it was short on 72% of bars with a mean position of -0.165, and its mean daily gain of -0.000684 splits into -0.000194 from the market's own rise and about -0.00049 from timing; timing was negative in 4 of 6 coins (BTC -0.00091, XRP -0.00113), giving a Sharpe of -1.256.
