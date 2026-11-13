---
line: 7.g patterns
backtest: N3-01_strong-volatile-momentum_1d
idea tested: N3-01_strong-volatile-momentum
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3382 USD
---
## Findings
- **F1:** The next-day return after a bar's close depends on the weekday, measured as excess over the coin's mean on non-overlapping 1-bar returns. After Thursday bars it is +0.0026 (t=2.77, n=2483) and after Friday bars +0.0035 (t=4.44, n=2479). After Monday bars it is -0.0024 (t=-2.47, n=2490) and after Wednesday bars -0.0033 (t=-2.98, n=2489).
- **F2:** The Thursday/Friday excess is positive in 7 of 8 years and significant in four of them: 2019 t=5.38, 2020 t=3.46, 2023 t=2.43, 2024 t=2.55. Only 2022 is negative (t=-1.59). It is positive in all 6 coins, from BTC +0.0009 (t=0.90) to LTC +0.0056 (t=3.50).
- **F3:** After a daily up move of more than 2 times the prior 20-day volatility, the 5-bar excess return is +0.0150 (t=2.42, n=361 non-overlapping events). The mean is positive in all 6 coins. It changes sign by year: 2021 +0.047 (t=3.12), 2024 +0.048 (t=2.94), but 2023 -0.016 (t=-2.56) and 2022 -0.043 (t=-1.90). After down shocks of the same size the 5-bar excess is -0.0070 (t=-1.26, n=387).
- **F4:** Bars with both the 20-day and the 60-day return positive are followed by a 5-bar excess of +0.0103 (t=2.35, n=600 non-overlapping). Most of this comes from bars the strategy left flat because volatility was below its threshold or the forecast was zero: +0.0163 (t=2.40, n=281). The bars it traded show only +0.0050 (t=0.88, n=319). The high-volatility filter therefore removes the better part of the trend drift.
- **F5:** After bars falling 1.5 to 2.5 recent volatilities in a day, the next day's excess return is +0.0044 (t=2.03, n=679). After falls beyond 2.5 volatilities it is +0.0059 (t=1.64, n=300). Up moves of the same size are followed by about -0.001 (t≈-0.5).
- **F6:** The book's profit comes from long holds. Trades lasting 10 to 30 days average +13.3% net and win 71% (n=272). Trades over 30 days average +48.2% (n=96). Trades of 5 days or less average -3.5% (n=332) and -3.0% (n=223), with win rates of 24% and 35%.

## Ideas
- `N3-01_strong-volatile-momentum.g1_late-week-next-day-lift` (from F1, F2): A coin's daily return on the day after a Thursday or Friday close is higher than its average daily return, because flows tied to the end of the week and the weekend lift spot crypto.
- `N3-01_strong-volatile-momentum.g2_calm-uptrend-drift` (from F4): When a coin is up over both 20 and 60 days while its 20-day volatility is in the lower half of its recent range, its next 5 days rise more than its average. Calm uptrends carry the drift better than volatile ones.
- `N3-01_strong-volatile-momentum.g3_upside-shock-continuation` (from F3): After a daily up move larger than twice the coin's recent daily volatility, the coin's next 5 days rise more than its average, because late buyers chase the visible jump.
- `N3-01_strong-volatile-momentum.g4_one-day-down-shock-bounce` (from F5): After a daily fall of more than 1.5 times the coin's recent daily volatility, the next day's return is above the coin's average, as a one-day bounce.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
