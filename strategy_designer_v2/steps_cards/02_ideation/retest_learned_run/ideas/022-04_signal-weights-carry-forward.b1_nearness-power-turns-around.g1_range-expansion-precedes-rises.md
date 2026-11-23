---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around
line: 7.g patterns
backtest: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The wider a coin's daily high-low range is relative to its average range over the past 30 days, the higher that coin's return over the next 5 days.
Consequence: A trader should favour the long side of a coin after its daily range has expanded well beyond its recent norm, and be more reluctant to short it then.
Why:
- F3: A wide day predicts the next 5 days. The larger a day's high-low range against its own 30-day average, the higher the coin's excess return over the next 5 days: the second quintile is followed by -0.90 % (t -2.15) and the top quintile by +0.78 % (t 1.64), with the pooled rank correlation of the raw range at 0.051 (t 2.80, 3042 cases).
- F4: The range effect in F3 holds coin by coin and year by year: its rank correlation is positive in all six coins (0.041 to 0.144) and in 7 of 8 years (-0.020 in 2019, 0.214 in 2024). In a joint regression with the forecast, however, the range term falls to t 0.16 while the forecast keeps t 2.07, so part of the effect overlaps the tested forecast.
- F2: The book's worst 2 % of coin-days (310, mean -8.40 %) come on days the coin rose on average (+1.03 %, only 50 % of them down days), so its largest losses are mostly short positions caught in rallies. Its best 2 % (mean +8.59 %) come on days the coin rose +2.95 %.
