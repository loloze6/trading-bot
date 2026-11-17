---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.d1_weekend-move-reverses-both-ways.g1_large-daily-fall-rebounds
line: 7.g patterns
backtest: 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.d1_weekend-move-reverses-both-ways.g1_large-daily-fall-rebounds_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: After a coin's daily fall, the coin rises over the next 1 day, and the rise is larger the larger the fall in units of its 20-day volatility multiplied by how high that 20-day volatility stands against its own 120-day average.
Consequence: A trader would buy sharp falls mainly when the coin is already in a turbulent stretch, and would refuse to buy the same falls in calm periods.
Why:
- F1: Large volatility-scaled falls rebound only when the coin's 20-day volatility is high against its own 120-day average. In the top fall quartile, the next-day excess return is +0.0137 (t 3.75, n 342) in the highest volatility-ratio tercile, +0.0061 (t 2.50, n 369) in the middle tercile and -0.0017 (t -0.83, n 474) in the lowest. Ranking all falls by fall size × volatility ratio gives quintiles 0–2 near zero (-0.0004 to -0.0012), quintile 3 at +0.0026 (t 1.74) and quintile 4 at +0.0081 (t 4.34, n 948).
- F4: The two conditions add up. Top-quartile falls with high volume in a high-volatility regime return +0.0159 the next day (t 3.33, n 229). The same high-volume falls in a low-volatility regime return -0.0029 (t -1.02, n 281).
- F6: The rebound depends heavily on the period. Big falls give +0.0139 (t 4.00) in 2020 and +0.0137 (t 3.97) in 2021. In 2019, 2022, 2024 and 2025 they give -0.0014 to +0.0005, with |t| < 0.7.
