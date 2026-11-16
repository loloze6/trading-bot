---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma
line: 7.g patterns
backtest: 002-03_price-cross-above-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's one-day fall relative to its own past 20-day daily volatility, the more it rises above its average return over the next 1 to 3 days.
Consequence: Do not sell into, and if anything buy, a coin's outsized one-day drop, sizing the bet with how many volatility units it fell, while refusing short-horizon shorts after such drops.
Why:
- F1: A coin's next-day excess return falls steadily as its one-day move, scaled by its prior 20-day volatility, rises. The bottom decile of scaled moves is followed by +0.55% (t=3.67, n=1378, hit 58.5%) and the second decile by +0.26% (t=2.08). Deciles 3 to 9 are flat to negative (−0.22% at decile 7, t=−1.91). The regression slope of the next-day return on the scaled move is −0.0014 (p=0.00008, about 9,600 bars).
- F2: The rebound after the largest scaled falls appears in every coin, though only XMR is individually significant: BTC +0.17% (t=0.92), ETH +0.30%, LTC +0.33%, XMR +0.76% (t=3.70), XRP +0.39% and ZEC +0.48% (t=1.76). It is positive in 6 of 8 years and strongest in 2020 (+1.21%, t=3.30) and 2021 (+1.12%, t=3.38). It fades to zero in 2024 (+0.00%) and 2025 (−0.03%).
- F3: The rebound after the bottom two deciles of scaled falls is larger when the close is below its 200-day SMA (+0.54%, t=4.13, n=1543) than above it (+0.24%, t=1.61, n=1213). A 3-day version on the non-overlapping 3-day grid still shows +0.86% after bottom-decile falls (t=2.08, n=452).
