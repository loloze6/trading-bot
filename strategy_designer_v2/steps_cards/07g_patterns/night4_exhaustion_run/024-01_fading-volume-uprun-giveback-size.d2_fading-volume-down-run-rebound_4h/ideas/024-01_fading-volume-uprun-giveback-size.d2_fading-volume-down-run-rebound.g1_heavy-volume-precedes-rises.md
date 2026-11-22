---
brief: 024_exhaustion-after-an-extended-run
source-idea: 024-01_fading-volume-uprun-giveback-size.d2_fading-volume-down-run-rebound
line: 7.g patterns
backtest: 024-01_fading-volume-uprun-giveback-size.d2_fading-volume-down-run-rebound_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: The higher a coin's traded volume over the past 3 days relative to its own 30-day norm, the more the coin rises over the next 3 days, and the lower it is, the more the coin lags.
Consequence: Unusually heavy 3-day volume is a reason to be long the coin for 3 days, and unusually thin volume a reason to refuse longs.
Why:
- F1: The level of volume predicts the next 3 days. Cases were read once per 18-bar cell on each coin's grid. When a coin's 3-day mean log volume, against its 30-day norm, is in its top fifth, its unusual 18-bar move is +0.97 % (t 3.13, 1062 cases). In its bottom fifth it is −0.85 % (t −3.44, 1062 cases). The single-bar volume gives the same split: top fifth +1.02 % (t 3.23, strength 0.109), bottom fifth −0.60 % (t −2.64), 1059 cases each.
- F2: The high-volume effect is broad but not universal. Over years, the top volume fifth's unusual move is positive in 6 of 8: 2020 +2.50 % (t 2.98), 2023 +0.99 % (t 1.94), 2024 +2.18 % (t 2.06), 2025 +2.11 % (t 1.93), against 2018 −1.52 % (t −1.65). Over coins, it is positive in 5 of 6, from +0.16 % (BTC) to +2.38 % (XRP), with ETH at −0.28 %. Its +1.0 % per case is about 5 times the 0.19 % cost of a trade.
- F5: Active markets keep rising. The top fifth of 3-day realised activity (mean |return| against usual) gives +0.97 % (t 3.10), against −0.69 % (t −2.78) in the bottom fifth. The top fifth of bar range gives +0.78 % (t 2.43), against −0.67 % (t −2.97) in the bottom fifth. Both overlap with the volume effect: in the top activity fifth, the top volume fifth gives +1.75 %.
