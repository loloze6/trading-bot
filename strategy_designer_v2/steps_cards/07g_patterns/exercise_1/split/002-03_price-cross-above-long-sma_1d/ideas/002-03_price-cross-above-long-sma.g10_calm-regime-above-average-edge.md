---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma
line: 7.g patterns
backtest: 002-03_price-cross-above-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin closes above its 200-day average while its 20-day volatility is in its low or middle range, it rises more over the next 20 bars than when it is below the average at the same volatility.
Consequence: A trader should rely on the above-average condition only when the coin's recent volatility is not elevated.
Why:
- F9: The long-versus-flat edge disappears in high volatility. Next-20-bar return for long bars minus flat bars was +2.25 points in the low 20-day-vol tercile and +2.56 points in the middle tercile, but −0.01 points in the high tercile (3.20% vs 3.21%). Even so, the book's mean daily return on long high-vol bars was the largest of the three (+0.40% vs +0.15% in the low tercile).
