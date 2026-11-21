---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around
line: 7.d not profitable
backtest: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: For a coin's nearness to its 90-day high, the higher that signal's predictive power for the coin's 5-day returns over the past 365 days, the lower the same signal's predictive power for that coin's 5-day returns over the following 90 days, except that the nearer the coin's close sits to its 90-day high and the larger its 20-day return, the more its 5-day return rises regardless of that past power.
Consequence: A trader leaning against recently-working nearness power should not lean short on a coin that is pressing its 90-day high after a strong month, because that is where the coin keeps rising and the falls of the book are made.
Why:
- F1: The Calmar fails because of one long fall: the deepest fall is 41.2 % against a yearly return of 22.1 % over 7.9 years. It lasted 815 days, across windows w14 to w21. Every window from w14 to w17 ended with a negative mean book return (-0.01 % to -0.07 % a day) while holding the coins rose in w15 to w17 (+0.27 % to +0.45 % a day). The second fall, 32.3 % in w1 to w8, adds to it.
- F2: Inside w14 to w21 the loss came from shorts held while the coin sat in its top quintile of nearness to the 90-day high. Those shorts lost 0.35 % per coin-day over 515 coin-days and gave -0.31 to the book's summed daily contribution, against +0.009 in the other windows. Longs in the same windows still added +0.75.
- F3: Over all windows, shorting near the 90-day high is the book's worst cell. It loses 0.97 % per coin-day over 1235 coin-days and takes away 19 % of the book's total gain, while longs in the same quintile earn 1.17 % per coin-day over 1137.
- F4: The forecast leans against the coin most often exactly where the coin keeps rising. In the top nearness quintile it is short in 55 % of the non-overlapping 5-day cells (41 % in the bottom quintile). Yet the coin's next 5-day return there is +1.28 % (t 2.44, 502 cases).
- F5: The same loss shows on the 20-day return. In the top quintile of the prior 20-day return, shorts lose 0.50 % per coin-day (1375 coin-days) while longs earn 0.85 % (1054 coin-days). The next 5-day return after the top two quintiles of the 20-day return is +1.96 % (t 3.85, 501 cases) and +1.33 % (t 2.37, 502 cases).
