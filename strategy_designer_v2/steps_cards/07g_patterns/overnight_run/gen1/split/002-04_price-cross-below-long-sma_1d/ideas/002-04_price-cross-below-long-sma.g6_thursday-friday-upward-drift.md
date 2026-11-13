---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-04_price-cross-below-long-sma
line: 7.g patterns
backtest: 002-04_price-cross-below-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: A coin's return from Thursday's close and from Friday's close to the next close tends to be positive and larger than on other weekdays.
Consequence: A trader would hold longs over Thursday and Friday, or delay shorts until after Friday.
Why:
- F10: Thursday and Friday are the strongest weekdays. Next-day mean returns on those two days are +0.34% (t 3.66) and +0.43% (t 5.24). Monday is -0.09% and Wednesday -0.18%. The Thursday-Friday premium holds in both 2018-2021 and 2022-2025 and in all six coins, for example LTC +0.61% vs -0.15% on other days.
