---
brief: 006_range-compression-precedes-expansion
source-idea: 006-04_upside-squeeze-break-continuation.g2_capitulation-volume-rebound.g1_volume-surge-predicts-weekly-return
line: 7.g patterns
backtest: 006-04_upside-squeeze-break-continuation.g2_capitulation-volume-rebound.g1_volume-surge-predicts-weekly-return_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: For a coin, the larger its 5-day return relative to its own 20-day daily volatility, the higher its return over the next 7 days; a strong recent week is followed by further gains and a weak one by further losses.
Consequence: A trader would lean long a coin after a strong week measured against its own volatility, and would refuse to hold one after a weak week, before trusting any signal from volume.
Why:
- F1: Across all coins and windows, a coin's 5-day return scaled by its 20-day daily volatility predicts its excess return over the next 7 days: pooled slope 0.0119 with t = 4.23 on 2011 non-overlapping 7-day cases, and the raw 5-day return gives slope 0.099 with t = 3.79.
- F2: The bottom two quintiles of the raw 5-day return are followed by excess 7-day returns of -1.25% (t = -1.98) and -1.20% (t = -2.20), against +0.98% (t = 1.96) in the middle quintile and +0.90% in the top quintile.
- F3: The 5-day momentum holds in every volatility tercile, slope t = 4.08 (n = 672) in the calmest, 1.39 (n = 667) in the middle and 2.14 (n = 672) in the most volatile; by year it is strongest in 2020 (t = 3.80) and 2022 (t = 4.00) and negative in 2018, 2019 and 2023 (t from -0.34 to -1.81).
- F4: The tested volume-ratio forecast itself is weak and uneven: its pooled quintiles are not monotone (-0.18%, -0.86%, -0.45%, +0.85%, +0.64% excess 7-day return), and its slope reaches t ≥ 2 only in XRPUSD (t = 2.90) and in 2024 (t = 3.90), with the other coins between t = -1.22 and 1.15.
