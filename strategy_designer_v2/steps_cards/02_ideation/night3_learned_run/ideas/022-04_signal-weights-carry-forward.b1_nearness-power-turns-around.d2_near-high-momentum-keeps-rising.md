---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around
line: 7.d not profitable
backtest: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The nearer a coin's close sits to its 90-day high and the larger its 20-day return, the higher its return over the next 5 days.
Consequence: A trader should hold a coin longer, and refuse shorts, the closer it is to its 90-day high after a strong 20-day rise.
Why:
- F3: Over all windows, shorting near the 90-day high is the book's worst cell. It loses 0.97 % per coin-day over 1235 coin-days and takes away 19 % of the book's total gain, while longs in the same quintile earn 1.17 % per coin-day over 1137.
- F4: The forecast leans against the coin most often exactly where the coin keeps rising. In the top nearness quintile it is short in 55 % of the non-overlapping 5-day cells (41 % in the bottom quintile). Yet the coin's next 5-day return there is +1.28 % (t 2.44, 502 cases).
- F5: The same loss shows on the 20-day return. In the top quintile of the prior 20-day return, shorts lose 0.50 % per coin-day (1375 coin-days) while longs earn 0.85 % (1054 coin-days). The next 5-day return after the top two quintiles of the 20-day return is +1.96 % (t 3.85, 501 cases) and +1.33 % (t 2.37, 502 cases).
- F6: The book's edge sits on its long side. Longs earn 0.137 % per coin-day over 7518 coin-days and shorts lose 0.016 % over 6689. The idea's whole move is only 1.5 times the 0.19 % cost of a round trip (0.29 % per case over 5 days). So a short side that bleeds near highs leaves little room for the falls to shrink.
