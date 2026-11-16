---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.g1_one-day-move-reversal
line: 7.g patterns
backtest: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.g1_one-day-move-reversal_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin trades below its 50-day average, the larger its one-day move relative to its usual daily move over the past 20 days, the larger the opposite move over the next day.
Consequence: A trader would fade sharp one-day moves in a coin trading under its 50-day average, rather than chase them.
Why:
- F6: The reversal is stronger below a coin's 50-day average (slope t -5.01, n 6732) than above it (t -1.52, n 6472).
- F1: The next-day reversal is concentrated in high-volatility days. In each coin's top tercile of 20-day volatility, the pooled slope of next-day excess return on the volatility-scaled one-day move is -0.00709 (t -8.26, n 5315). In the middle tercile it is t -0.62, and in the bottom tercile it is +0.00127 (t +2.70). The continuous move × volatility-rank interaction has t -9.32 (n ≈ 15,940).
