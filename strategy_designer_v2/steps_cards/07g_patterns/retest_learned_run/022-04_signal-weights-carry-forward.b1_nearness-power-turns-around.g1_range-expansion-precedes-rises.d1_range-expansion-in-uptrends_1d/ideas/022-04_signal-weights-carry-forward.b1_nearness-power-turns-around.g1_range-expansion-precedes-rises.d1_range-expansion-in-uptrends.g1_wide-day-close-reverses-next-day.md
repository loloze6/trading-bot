---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d1_range-expansion-in-uptrends
line: 7.g patterns
backtest: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d1_range-expansion-in-uptrends_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The further a coin's close sits toward the high of its day, and the wider that day's high-low range is relative to its average range over the past 30 days, the lower the coin's return over the next 1 day. The further its close sits toward the low of a wide day, the higher that return.
Consequence: A trader should fade a coin's close at the top of an unusually wide day for the next day, and not chase it. The edge is about 0.24 % per standard deviation of the signal, close to the 0.19 % a round trip costs, so it pays only on the strongest days.
Why:
- F1: Over the next 1 day the signal reverses: on 14 644 coin-days, the day's range relative to its 30-day mean range, multiplied by where the close sits in that range (from −1 at the low to +1 at the high), predicts the next day's return with a slope of −0.24 % per standard deviation and a t of −6.04. This is the only pattern of all the angles examined that stands far above chance.
- F2: The tested 5-day effect of range expansion in rising coins depends on which bars the grid starts on, so it is not robust. Within positive 20-day returns its slope t is 1.35 on the grid starting at position 0 (n=1418) and 2.96 on the grid starting at position 2 (n=1416). The range-times-close-location signal turns from t 1.38 to t −0.15 between the same two grids.
