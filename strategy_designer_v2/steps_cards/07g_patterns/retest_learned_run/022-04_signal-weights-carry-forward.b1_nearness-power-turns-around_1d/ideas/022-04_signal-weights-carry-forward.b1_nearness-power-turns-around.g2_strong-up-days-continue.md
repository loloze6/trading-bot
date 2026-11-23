---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around
line: 7.g patterns
backtest: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's daily rise is relative to its volatility over the past 30 days, the higher that coin's return over the next 5 days.
Consequence: A trader should treat an unusually strong up day as a reason to hold or add longs over the following days, not to fade it.
Why:
- F5: Large days continue upward rather than reverse. Days in the top quintile of absolute move against 30-day volatility are followed by +1.07 % over 5 days (t 2.19, 482 cases; +0.147 of a usual move, t 2.36), positive in all six coins (rho 0.012 to 0.083). This comes from up days: days above +2 standard deviations are followed by +3.23 % (t 2.06, 84 cases) and days below -2 by -0.69 % (t -0.69, 58 cases).
- F2: The book's worst 2 % of coin-days (310, mean -8.40 %) come on days the coin rose on average (+1.03 %, only 50 % of them down days), so its largest losses are mostly short positions caught in rallies. Its best 2 % (mean +8.59 %) come on days the coin rose +2.95 %.
- F1: The forecast's skill sits on its long side: over 3042 non-overlapping 5-day cases, the top forecast quintile is followed by +0.88 % excess (t 1.93, 610 cases), but the bottom quintile by only -0.24 % (t -0.50), so shorts earn about 0.24 %. The pooled rank correlation is 0.054 (t 2.99), positive in five coins (0.024 to 0.081) and negative in ZEC (-0.026).
