---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma
line: 7.d not profitable
backtest: 002-03_price-cross-above-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin trading above its 200-day average is in a high-volatility stretch, measured by its recent daily return spread, the following days rise more than in calm stretches above the average.
Consequence: Favour the long while the trend comes with high recent volatility, and give less weight to calm drifts above the average.
Why: F6: On bars with a positive forecast, the effect is strongest when the coin is volatile. The gross daily return is 0.004720 in the top tercile of 20-day volatility (mean daily volatility 0.070), against 0.001658 and 0.001651 in the calmer two terciles.
