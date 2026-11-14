---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma
line: 7.g patterns
backtest: 002-03_price-cross-above-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: A coin's daily bar stamped Saturday rises more than its average day, and the Friday bar does too.
Consequence: A trader would hold or tilt long into the Friday and Saturday bars and would put new longs on before them rather than mid-week.
Why:
- F2: Saturday-stamped daily returns averaged +0.44% (t=5.41, n=2433) and Friday +0.32% (t=3.41), while Tuesday (-0.09%) and Thursday (-0.18%) were negative. The Saturday mean was positive in all six coins (t from 1.40 to 2.92) and in 7 of 8 years, with t above 1.9 in 2019, 2020, 2021, 2024 and 2025. It was near zero only in 2018, 2022 and 2023.
