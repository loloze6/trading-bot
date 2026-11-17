---
brief: 013_anchoring-to-recent-high
source-idea: 013-03_breakout-above-high-continues.g1_near-30-day-high-continuation
line: 7.d not profitable
backtest: 013-03_breakout-above-high-continues.g1_near-30-day-high-continuation_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: Among a coin's daily closes within a few percent of the highest high of its prior 30 days or above it, the further the close sits through that high, the larger the coin's return over the next 10 days.
Consequence: A trader would concentrate long exposure on coins at or breaking their 30-day high for a 10-day hold, instead of spreading the bet into shorts on coins below the high, where the next 10 days show no graded fall.
Why:
- F1: The book barely holds the coin. Its mean position is +0.009 and its mean absolute position is about 0.14, it is short on 46% of days and flat on 8%. As a result its mean daily return is 0.000077, against 0.00119 for holding, and its daily standard deviation is 0.0079 against 0.049. Only 0.000011 of its gain comes from the market's own rise.
- F3: The forecast's information sits only at the top of the distance range. On non-overlapping 10-day samples, the sextile within 4.5% of the 30-day high or above it has an excess 10-day return of +0.031 (282 cases, 56% up). The five lower sextiles are not graded: they range from −0.014 to +0.003. So the negative forecasts below the usual distance short a coin that does not fall in a graded way.
- F2: Longs carry the whole gain and shorts lose it back. Summed daily gains are +2.13 on 4,273 long bars (mean 0.000499) and −0.63 on 4,035 short bars (mean −0.000157).
