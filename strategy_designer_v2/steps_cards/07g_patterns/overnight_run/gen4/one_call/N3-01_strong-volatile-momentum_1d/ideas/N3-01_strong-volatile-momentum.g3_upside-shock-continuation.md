---
brief: 002_moving-average-cross-trend-persistence
source-idea: N3-01_strong-volatile-momentum
line: 7.g patterns
backtest: N3-01_strong-volatile-momentum_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: After a daily up move larger than twice the coin's recent daily volatility, the coin's next 5 days rise more than its average, because late buyers chase the visible jump.
Consequence: A trader can treat an outsized up day as an entry for a short long hold, but must expect losing years.
Why:
- F3: After a daily up move of more than 2 times the prior 20-day volatility, the 5-bar excess return is +0.0150 (t=2.42, n=361 non-overlapping events). The mean is positive in all 6 coins. It changes sign by year: 2021 +0.047 (t=3.12), 2024 +0.048 (t=2.94), but 2023 -0.016 (t=-2.56) and 2022 -0.043 (t=-1.90). After down shocks of the same size the 5-bar excess is -0.0070 (t=-1.26, n=387).
