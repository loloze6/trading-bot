---
brief: 023_range-reversion-when-no-trend
source-idea: 023-03_flatter-range-stronger-reversion.d1_flat-range-breakout-continuation.d1_flat-range-upside-breakout-continuation
line: 7.g patterns
backtest: 023-03_flatter-range-stronger-reversion.d1_flat-range-breakout-continuation.d1_flat-range-upside-breakout-continuation_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's latest 1-day rise relative to its 20-day volatility of daily returns, the larger its rise over the next 5 days.
Consequence: A day up by many times the coin's usual daily move is a reason to buy for the following 5 days rather than fade it.
Why:
- F4: A large day relative to the coin's 20-day volatility is followed by a higher 5-day return above drift.
- F3: The tested forecast's edge is confined to 2018–2021. Its yearly slopes are 0.029 to 0.055 there (t 1.29 to 2.79), and −0.007 to −0.013 in each of 2022–2025 (t −0.74 to −0.78). The net-move slope does the same: 2018–21 0.0154 (t 3.00, 1278 cases), 2022–25 −0.0012 (t −0.28, 1277 cases).
