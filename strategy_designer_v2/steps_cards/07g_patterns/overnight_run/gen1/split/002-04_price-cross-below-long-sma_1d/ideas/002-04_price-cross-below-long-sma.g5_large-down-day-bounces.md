---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-04_price-cross-below-long-sma
line: 7.g patterns
backtest: 002-04_price-cross-below-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: After a daily drop larger than 1.5 times the coin's 20-day daily volatility, the next day tends to close up.
Consequence: A trader would avoid opening a short on the close of a large down day, and could take a one-day long instead.
Why:
- F9: Large down days are followed by up days. Daily moves below -1.5 sigma (20-day volatility) are followed by next-day returns of +0.43% (t 2.14, 61% up) and +0.89% (t 1.69, 61% up). Moves above +2.5 sigma are followed by a next day with only 41% up days, while their 10-bar return is still +5.39% (t 2.98).
- F8: The book's worst days follow sharp upside reversals while it is deeply short. On its 171 worst days (mean book return -19.3%), the coin rose +12.7% that day, with mean allocation -1.31 and SMA distance -32%. Its 171 best days came on -11.1% coin days after a -21.7% 10-day slide, at distance -46%.
