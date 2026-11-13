---
brief: 002_moving-average-cross-trend-persistence
source-idea: N1-06_deep-below-average-rebound
line: 7.g patterns
backtest: N1-06_deep-below-average-rebound_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin trading below its 200-day average closes a day up by more than one 20-day standard deviation, the next day falls more often than an ordinary day, as rallies inside a downtrend are sold into.
Consequence: A trader should refuse to chase a sharp up close below the SMA200 with a new long, and can fade it for a day.
Why:
- F1: Across all six coins, a daily drop of 1 to 2 times the coin's 20-day volatility is followed by a next-day excess return of +0.42% (t=3.03, n=1276 one-day cases, 58% up), every bucket with a drop of 1 sigma or more rises the next day 58-61% of the time, and a rise of 1 sigma or more is followed by an up day only 41-47% of the time.
- F3: Below the SMA200 the mirror image appears: a rise of 1 sigma or more is followed by a next-day excess of -0.28% (t=-1.77, n=782, only 43% up), against +0.16% (t=1.04, n=1102) above it.
