---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-01_learned-combined-signal-score
line: 7.d not profitable
backtest: 022-01_learned-combined-signal-score_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's four signals are combined into one score, the coin's return over the next 5 days is higher the higher that score is. The four signals are its 28-day return, minus its last 1-day return, its closeness to its 90-day high, and minus its 30-day volatility. Each signal is weighted equally in the direction its effect is known for, instead of by how well it predicted that coin's own 5-day returns over the past 365 days.
Consequence: The weak effects should be combined with fixed, known directions, because weights learned from the past year point the wrong way in the year that follows.
Why:
- F1: The learned weights do not carry forward from one year to the next. Across 40 coin-year pairs, a signal's rank correlation with the coin's excess 5-day return in one year correlates with the previous year's at -0.115 for the 28-day return, -0.196 for the 1-day return, -0.021 for nearness to the 90-day high and 0.133 for 30-day volatility. The sign repeats in only 35 % to 55 % of pairs. This matches the brief's own condition for the theory being wrong.
- F2: Because the weights look back over the past 365 days, the score ends up pointing against what follows. The forecast's rank correlation with the excess 5-day return is -0.037 pooled, and it is negative on 5 of 6 coins (BTC -0.073, ZEC -0.053) and in 7 of 8 years.
- F3: Both sides lose. Long cases earn -0.56 % excess per 5 days (t -2.10, 1535 cases) and short cases -0.49 % (t -1.83, 1743 cases). The two most negative forecast quintiles are followed by +0.67 % and +0.63 % excess moves, and the fourth quintile by -1.19 %.
- F4: The book's loss is timing, not exposure. Its gain before costs is -0.063 % per bar; -0.054 % of that is timing and -0.009 % comes from the market's own rise. It is short on 51 % of bars.
