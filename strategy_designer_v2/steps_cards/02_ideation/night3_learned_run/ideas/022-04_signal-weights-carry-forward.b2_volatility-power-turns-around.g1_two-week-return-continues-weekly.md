---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-04_signal-weights-carry-forward.b2_volatility-power-turns-around
line: 7.g patterns
backtest: 022-04_signal-weights-carry-forward.b2_volatility-power-turns-around_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: For a coin, the higher its 14-day return, the higher its return over the next 7 days.
Consequence: A coin that has risen most over two weeks is a reason to hold it long for the following week, and one that has fallen most a reason to stay out or short.
Why:
- F2: A coin's 14-day return predicts its next 7 days in the same direction, and the effect is graded. The slope of strength on the coin's own rank is +0.31 (t 3.97, 1916 non-overlapping cases), positive in 6 of 6 coins. The top 20 % of 14-day returns are followed by an unusual move of +2.6 % (strength 0.20) and a total move of +3.8 %, about 20 times the cost of a round trip.
- F3: This continuation is carried mostly by the later windows, so it may not be stable.
- F4: The continuation fades as the past period and the horizon lengthen.
- F1: The tested idea is real but far too small to pay for a trade. Its unusual move is +0.12 % per case over 5 days, a strength of 0.004, about a tenth of the usual 0.05 (findings F10). Its total move is +0.07 %, which is 0.4 times the 0.19 % cost of a round trip. The book earns 0.044 % a day against the 0.05 % required, with a Calmar of 0.26.
