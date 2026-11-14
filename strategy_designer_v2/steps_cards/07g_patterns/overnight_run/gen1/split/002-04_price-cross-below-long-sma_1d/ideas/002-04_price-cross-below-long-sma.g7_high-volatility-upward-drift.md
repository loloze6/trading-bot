---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-04_price-cross-below-long-sma
line: 7.g patterns
backtest: 002-04_price-cross-below-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's 20-day volatility is in the top third of its own range, its next-day return tends to be positive and higher than in calmer periods.
Consequence: A trader would refuse shorts during a coin's high-volatility periods, and lean long in them instead.
Why:
- F11: The book's losses concentrate in high volatility. Mean daily book return is -0.22% (t -3.17) in each coin's top 20-day-volatility tercile, against +0.04% (t 1.41) in the low tercile. Next-day coin returns are highest in that same tercile, +0.26% (t 3.08).
- F12: The book loses in most years, and 2018 is the only one positive on average. Mean daily book return is +0.16% in 2018, -0.31% in 2020 (t -4.30) and -0.10% in 2021 (t -3.65). In 2020 and 2021 the coin's next-day return while the book was short was +0.72% (t 3.86) and +0.68% (t 3.39), higher than while flat.
