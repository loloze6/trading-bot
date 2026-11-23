---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d1_nearness-power-reversal-long-side
line: 7.g patterns
backtest: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d1_nearness-power-reversal-long-side_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin closes in the lower part of its 90-day range, the further below its 90-day high it closes, the higher its return over the next 5 days. The coins sitting only moderately below their high do worst, and the deepest ones rebound.
Consequence: A trader should buy a coin in a drawdown in proportion to its depth below the 90-day high, and refuse longs in coins that have only slipped part of the way down.
Why:
- F1: Closes moderately below the 90-day high do worst. On the 5-day grid, the second quintile of nearness to the 90-day high (per coin) has a mean excess 5-day return of -1.89 % (t -4.13, 466 cases). It is negative in 2018–2021 (-2.70 %, t -2.61, 125 cases) and in 2022–2025 (-1.59 %, t -3.20, 341 cases), and in 14 of 15 coins (93 %).
- F2: Closes furthest below the 90-day high recover. The deepest quintile has an excess 5-day return of +0.96 % (t 1.96, 475 cases), and it is positive in both periods (+1.01 % and +0.91 %). Inside the lower two quintiles, the rank correlation between nearness to the high and the excess 5-day return is -0.081 (p 0.013): the further below its high a coin closes, the higher its next 5 days.
- F4: The tested reversal signal carries almost nothing.
