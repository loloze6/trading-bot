---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d2_wide-range-days-lead-rises.b1_range-versus-norm-both-sides.d2_range-expansion-long-side-only
line: 7.g patterns
backtest: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d2_wide-range-days-lead-rises.b1_range-versus-norm-both-sides.d2_range-expansion-long-side-only_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The more a coin's daily high-low range exceeds its 30-day average range on a day it closes lower, the higher its return over the next 3 days above its usual drift.
Consequence: A trader would buy a coin after a wide down day, more the wider the day, and skip buying after wide up days, which carry the tested idea's long positions for nothing.
Why:
- F1: The idea's gain comes entirely from wide days that close down. On non-overlapping 3-day grid cases, a down day with range above 1.7 times its 30-day mean range is followed by an excess 3-day return of +2.39 % (t 3.99, n 269). The same width on an up day is followed by −0.59 % (t −0.92, n 234). Over all wide days (range ratio above 1), down days give +0.71 % (t 2.26, n 936) and up days give −0.31 % (t −1.09, n 899).
- F2: On down days the effect grows with the range's width. The excess 3-day return is −0.54 % (t −1.15, n 388) at a ratio of 1–1.3, +0.81 % (t 1.43, n 279) at 1.3–1.7 and +2.39 % (t 3.99, n 269) above 1.7. On down days, the top quartile of fall size × width gives +0.93 % (t 2.36, n 599).
- F3: Wide down days are followed by a positive excess in five of six coins. XMR gives +1.19 % (n 154), ZEC +1.28 % (n 157), XRP +0.95 % (n 152), LTC +0.61 % (n 174) and BTC +0.19 % (n 149), while ETH is flat at −0.01 % (n 150). By year the effect is uneven: 2020 gives +3.12 % (t 3.23, n 110), and 2018 (−0.34 %) and 2022 (−0.51 %) are negative.
