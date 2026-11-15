---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma
line: 7.b inconclusive
backtest: 002-03_price-cross-above-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: After a coin's close crosses above its long moving average, the price keeps rising over the following bars more often and further than after random bars.
Consequence: Price crossing above the long average starts an uptrend that persists, because late buyers extend the move.
Why:
- F1: The main measure leans the way the idea predicts but falls short of the bar: block mean +0.126 with t 1.73 over 811 non-overlapping 20-bar blocks (502 with a position), and 8 of 24 windows have a positive block mean (t across windows 0.88).
- F2: The positive mean rests on a few very large blocks rather than a steady drift: the block sums have median 0 and skew 7.6, the top 10 blocks sum to 132.7 against 102.4 for all 811, and without those 10 the block mean is -0.038 (t -0.92).
- F5: The result swings with the market regime. Active 20-day excess is -0.132 (t -2.76, n 21) in 2018 and -0.173 (t -3.12, n 10) in 2022, and about +0.02 to +0.04 in 2020, 2021, 2024 and 2025. Across coins it ranges from -0.022 (XRP) to +0.059 (ZEC), and no coin reaches |t| 0.7.
