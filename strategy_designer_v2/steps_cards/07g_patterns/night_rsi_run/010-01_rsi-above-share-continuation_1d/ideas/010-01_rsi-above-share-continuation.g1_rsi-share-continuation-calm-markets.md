---
brief: 010_rsi-midline-regime-direction
source-idea: 010-01_rsi-above-share-continuation
line: 7.g patterns
backtest: 010-01_rsi-above-share-continuation_1d
instruments: BTC, ETH, BNB
bar: 1d
period: folds A, B, C, D
---
Idea: The larger the share of the past 30 days that a coin's 14-day RSI has spent above 50, the higher the coin's return over the next 14 days. This holds when the coin's 30-day volatility of daily returns is low relative to its own history.
Consequence: Follow the side RSI has held in calm markets, and give that reading little weight when the coin's recent volatility is high.
Why:
- F1: The forecast's link to the next 14 days holds only when the coin's own 30-day volatility is below its median. There the slope of next 14-day excess return on the forecast has t = 2.55 (n = 266 non-overlapping samples). In the high-volatility half it is t = -0.79 (n = 118). Pooled over all samples it is t = 1.65 (n = 384).
- F2: The book's gain is almost all timing, not the market's own rise. Mean gain per bar is 0.00102, of which the market part is 0.000032 and the timing part 0.000989, with a mean position of only 0.026.
