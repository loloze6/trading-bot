---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.g1_one-day-move-reversal
line: 7.g patterns
backtest: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.g1_one-day-move-reversal_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The more a coin's 20-day volatility exceeds its 60-day volatility, the more its next-day return runs opposite to its one-day move, in proportion to that move's size against the coin's usual daily move.
Consequence: A trader would fade one-day moves more heavily when volatility is expanding and stop fading them as it contracts.
Why:
- F1: The next-day reversal is concentrated in high-volatility days. In each coin's top tercile of 20-day volatility, the pooled slope of next-day excess return on the volatility-scaled one-day move is -0.00709 (t -8.26, n 5315). In the middle tercile it is t -0.62, and in the bottom tercile it is +0.00127 (t +2.70). The continuous move × volatility-rank interaction has t -9.32 (n ≈ 15,940).
- F5: Reversal also strengthens with volatility expansion. By tercile of 20-day over 60-day volatility, the slope t goes from +0.84 (lowest) to -2.89 (middle) to -4.91 (highest), with about 4,350 bars per tercile.
