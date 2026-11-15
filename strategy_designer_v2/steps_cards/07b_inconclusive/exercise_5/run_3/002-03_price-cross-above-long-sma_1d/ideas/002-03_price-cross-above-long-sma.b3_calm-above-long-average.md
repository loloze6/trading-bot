---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma
line: 7.b inconclusive
backtest: 002-03_price-cross-above-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's close is above its 200-day simple moving average, the further it sits above, the more it rises beyond its usual drift over the next 20 days, only while its 60-day volatility is low compared with its own past.
Consequence: A trader should trust a position above the long average more in calm conditions than in turbulent ones.
Why:
- F5: Only the largest forecasts lean positive: the top forecast quartile gives +0.072 (t 1.34, n 100) and the bottom −0.035 (t −1.81, n 100), and low-volatility active bars do best (+0.027, t 1.19) against high-volatility ones (−0.011).
- F1: The effect is weak and mostly carried by a few large blocks: the block-mean excess is 0.126 with t 1.73 over 811 blocks, but the median block is 0.0 and only 23.4% of blocks are positive; on the 399 active 20-day grid bars the mean excess is +0.0052 (t 0.32) against −0.0002 on 412 flat bars (active minus flat +0.0053, Welch t 0.27), and only 40.6% of active bars beat the coin's average.
