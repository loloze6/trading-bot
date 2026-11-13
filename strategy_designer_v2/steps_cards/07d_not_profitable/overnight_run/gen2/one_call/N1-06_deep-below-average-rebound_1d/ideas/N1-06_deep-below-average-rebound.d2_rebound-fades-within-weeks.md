---
brief: 002_moving-average-cross-trend-persistence
source-idea: N1-06_deep-below-average-rebound
line: 7.d not profitable
backtest: N1-06_deep-below-average-rebound_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: After a coin plunges far below its 200-day average, the rebound comes within the first one to three weeks, and after that the price drifts back down with the prevailing decline.
Consequence: Hold a deep-discount long for only one to three weeks, and exit even if the close stays below the average, since the long holds give back the gain.
Why:
- F2: The losses come from long holds: the 332 trades held over 20 days lose -4.02 % before fees, while trades held 0–1.5, 1.5–3, 3–7 and 7–20 days earn +4.91 % (n=116), +3.51 % (n=122), +6.00 % (n=200) and +5.28 % (n=252).
- F4: Bear years drive the result. Active 10-bar excess returns are -3.95 % in 2018 (n=137, t=-2.41), -1.62 % in 2019 (n=136, t=-1.91) and -2.51 % in 2022 (n=191, t=-2.65). They are +4.91 % in 2020 (n=73, t=3.03) and +4.16 % in 2021 (n=66, t=1.76). Meanwhile the book is long on 51 % of bars and so ends level with holding (Sharpe gap -0.016, Calmar 0.23).
