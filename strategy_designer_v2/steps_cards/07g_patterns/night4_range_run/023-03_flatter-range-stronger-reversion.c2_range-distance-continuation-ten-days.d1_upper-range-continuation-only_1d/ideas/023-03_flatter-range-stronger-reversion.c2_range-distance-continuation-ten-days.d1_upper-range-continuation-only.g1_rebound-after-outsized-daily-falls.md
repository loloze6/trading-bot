---
brief: 023_range-reversion-when-no-trend
source-idea: 023-03_flatter-range-stronger-reversion.c2_range-distance-continuation-ten-days.d1_upper-range-continuation-only
line: 7.g patterns
backtest: 023-03_flatter-range-stronger-reversion.c2_range-distance-continuation-ten-days.d1_upper-range-continuation-only_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's one-day fall, measured against its own daily volatility over the past 30 days, the more the coin rises back over the next 1 to 3 days.
Consequence: A trader should lean long on a coin for a few days after an unusually large daily drop, more so the larger the drop relative to its recent volatility, and should not read the same size of rise as a reason to short.
Why:
- F1: The next day's excess return rises the larger the day's fall measured in the coin's own 30-day daily volatility: on down days the slope of next-day excess return on the vol-scaled move is -0.00415 with t -6.0 (6332 days), and the bucket means grow with the fall, +0.08 % (t 1.1, 4755) for falls under 1, +0.29 % (t 1.6, 753) for 1 to 1.5, +0.70 % (t 2.5, 383) for 1.5 to 2, +0.54 % (t 1.9, 316) for 2 to 3 and +1.60 % (t 2.4, 137) beyond 3 volatilities.
- F2: The rebound has no mirror on up days, where the slope is -0.00022 with t -0.34 (6572 days), and up days beyond 3 volatilities are followed by -0.24 % (t -0.40, 143).
- F3: The rebound after a fall beyond 1.5 volatilities is positive in all 6 coins (XMR +1.53 % t 3.8, XRP +1.46 % t 2.5, LTC +0.65 %, ZEC +0.61 %, ETH +0.24 %, BTC +0.18 %) and in all 8 years (2020 +2.10 % t 2.9, 2025 lowest at +0.15 %), and it lasts beyond one day, with +0.86 % excess over the next 3 days (t 2.9, 826 cases, not fully independent).
