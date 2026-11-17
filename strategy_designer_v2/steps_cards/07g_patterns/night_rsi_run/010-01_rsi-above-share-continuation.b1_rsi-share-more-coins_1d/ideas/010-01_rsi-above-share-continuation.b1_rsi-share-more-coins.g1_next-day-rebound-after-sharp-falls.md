---
brief: 010_rsi-midline-regime-direction
source-idea: 010-01_rsi-above-share-continuation.b1_rsi-share-more-coins
line: 7.g patterns
backtest: 010-01_rsi-above-share-continuation.b1_rsi-share-more-coins_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's one-day fall, measured against its own daily volatility over the past 30 days, the higher its return over the next 1 day.
Consequence: A trader would lean long a coin for a day after an unusually sharp daily drop, and refuse to sell it into that drop.
Why:
- F1: The coin's own one-day move reverses the next day: across all six coins, the next-day excess return is +0.88% after a fall of 2 or more 30-day standard deviations (t 3.09, n 430) and +0.51% after a fall of 1 to 2 (t 3.45, n 1280), against +0.04% after one of 1 to 2 up (n 1391); the slope of the next-day excess return on the scaled move has t -4.76.
- F2: This rebound after falls of 1 or more standard deviations is positive in all six coins (XMR +1.03% t 3.64, ZEC +0.80% t 2.20, XRP +0.74% t 1.97, BTC +0.32% t 1.26) and in 7 of 8 years (2021 +1.56% t 3.42, 2020 +1.40% t 2.90, 2023 +0.56% t 2.43; 2025 -0.11% t -0.33).
