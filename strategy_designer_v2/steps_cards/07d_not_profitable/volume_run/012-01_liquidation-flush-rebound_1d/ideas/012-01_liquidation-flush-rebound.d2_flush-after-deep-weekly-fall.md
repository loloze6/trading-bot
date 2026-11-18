---
brief: 012_liquidation-flush-partial-rebound
source-idea: 012-01_liquidation-flush-rebound
line: 7.d not profitable
backtest: 012-01_liquidation-flush-rebound_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a bar closes sharply lower on volume far above its own 30-day average volume and leaves a long lower wick below its close, price rises over the next 3 days, the more so the deeper the coin's own 5-day fall into that bar. The more extreme the volume burst and the longer the wick, the larger that rise.
Consequence: A trader would size the rebound trade by how far the coin has already fallen over 5 days, putting most of the book in flushes that end a deep fall and little in flushes after a flat week.
Why:
- F5: The rebound is strongest when the coin has already fallen over 5 days: the lowest 5-day-return tercile has a 3-day excess of 0.0159 (t 2.82, n 312), the middle tercile -0.0001 (t -0.02), and the held gain is 0.0080 in the deepest 5-day-fall quartile (median -16.8%) against 0.0015 to 0.0035 elsewhere.
- F4: The rebound sits in the extreme forecasts: the top forecast quartile has a 3-day excess of 0.0208 (t 3.09, n 243), while the other three quartiles give 0.0063, 0.0009 and 0.0069 with t between 0.19 and 1.31.
- F1: The book earns a mean daily return of 0.000387, below the 0.0005 floor, against 0.00118 for holding the coins, with a deepest fall of -28.5% (Calmar 0.40), and it is in a position on only 18.0% of bars at a mean allocation of 0.84.
