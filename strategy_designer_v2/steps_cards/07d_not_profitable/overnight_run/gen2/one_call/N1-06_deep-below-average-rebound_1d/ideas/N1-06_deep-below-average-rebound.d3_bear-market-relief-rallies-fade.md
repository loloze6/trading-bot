---
brief: 002_moving-average-cross-trend-persistence
source-idea: N1-06_deep-below-average-rebound
line: 7.d not profitable
backtest: N1-06_deep-below-average-rebound_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin is below its 200-day average and has rallied over the past 20 days, or its close has climbed back above its 50-day average, its price falls over the following ten days relative to its normal drift.
Consequence: Refuse or cut deep-discount longs once the coin has already bounced inside a bear market, because these relief rallies fade.
Why:
- F6: A bounce inside the decline does not pay. Active bars with a positive 20-day return lose -1.14 % excess over 10 bars (n=234, t=-1.25), against -0.06 % for those with a negative 20-day return (n=607). Active bars with the close above its 50-day average lose -1.33 % (n=125, t=-1.30).
- F4: Bear years drive the result. Active 10-bar excess returns are -3.95 % in 2018 (n=137, t=-2.41), -1.62 % in 2019 (n=136, t=-1.91) and -2.51 % in 2022 (n=191, t=-2.65). They are +4.91 % in 2020 (n=73, t=3.03) and +4.16 % in 2021 (n=66, t=1.76). Meanwhile the book is long on 51 % of bars and so ends level with holding (Sharpe gap -0.016, Calmar 0.23).
