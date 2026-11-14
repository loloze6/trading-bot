---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-04_price-cross-below-long-sma
line: 7.d not profitable
backtest: 002-04_price-cross-below-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: (new idea) After a coin's close has fallen sharply and far below its recent high, the coin rises over the following bars, and it rises more the deeper and faster that fall was.
Consequence: A deep, fast drop below the recent high is a reason to refuse shorts and a candidate setup for a long rebound trade.
Why:
- F3: The deepest forecasts carry the largest short and the worst result: at forecast -15 to -20 the mean allocation is -0.84, the mean gain is -0.0154 (t -1.32, n 125) and the coin's excess 10-bar return is +2.15%, a reversal. At forecast -5 to -15 the shorts gain +0.0048 (t 0.86, n 169) and +0.0028 (t 0.92, n 275).
- F4: Shorts lose after a sharp, deep fall and gain after a pause or bounce under the average. In the most negative 20-bar momentum quartile (below -15%) the gain is -0.0047 with excess +0.46%; in the two highest quartiles it is +0.0055 (t 1.29) and +0.0032 (t 1.51). When the close is more than 34% under its 60-bar high the gain is -0.0065 with excess +1.57%; between 9% and 34% under it the gain is +0.0025 and +0.0091 (t 1.39).
- F5: The losses gather in recovery years and the gains in bear years. Mean gain per block is -0.0184 in 2020 (t -3.26, n 87), -0.0108 in 2021 (t -2.65) and -0.0110 in 2023 (t -2.13). It is +0.0125 in 2018 (t 1.59), +0.0061 in 2019 (t 2.02) and +0.0080 in 2022 (t 1.42).
