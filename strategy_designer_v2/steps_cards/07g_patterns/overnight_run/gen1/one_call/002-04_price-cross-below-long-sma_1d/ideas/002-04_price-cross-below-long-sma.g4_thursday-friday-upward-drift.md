---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-04_price-cross-below-long-sma
line: 7.g patterns
backtest: 002-04_price-cross-below-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: A coin's daily close-to-close return is higher on days that start from a Thursday or Friday close than on other weekdays.
Consequence: A trader can time long entries toward Thursday and Friday closes and avoid opening shorts there.
Why:
- F7: Thursday and Friday next-day returns are +0.34% (t 3.66) and +0.43% (up 55%, t 5.24), against -0.09% and -0.18% for Monday and Wednesday. The Thursday-plus-Friday excess over other days is positive in 7 of 8 years and slightly negative in 2021.
