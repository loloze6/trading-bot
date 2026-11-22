---
brief: 023_range-reversion-when-no-trend
source-idea: 023-03_flatter-range-stronger-reversion.d1_flat-range-breakout-continuation.d1_flat-range-upside-breakout-continuation
line: 7.g patterns
backtest: 023-03_flatter-range-stronger-reversion.d1_flat-range-breakout-continuation.d1_flat-range-upside-breakout-continuation_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's net 30-day move up relative to its 30-day closing range, the larger its rise over the next 5 days.
Consequence: A close at the end of a month that climbed steadily across its range is a reason to buy for the next 5 days, and a month that went nowhere gives no such reason.
Why:
- F1: The flatness factor adds nothing to the forecast. Splitting range position into a flat part and a trending part gives similar coefficients (flat 0.0122, t 1.55; trending 0.0065, t 1.34). The least flat fifth of 30-day ranges, mean flatness 0.085, is followed by the largest 5-day move above the coin's drift (+1.44 %, t 2.61, 515 cases). The flattest fifth gets −0.53 % (t −1.39).
- F2: The net 30-day move as a share of the 30-day closing range predicts the 5-day return above drift with a positive slope (0.0077, t 2.26, 2555 non-overlapping cases). Its top fifth (net/range +0.84) gets +0.98 % (t 1.76), and the second-lowest fifth −1.18 % (t −2.83). This is continuation of the month's direction, not reversion.
- F3: The tested forecast's edge is confined to 2018–2021. Its yearly slopes are 0.029 to 0.055 there (t 1.29 to 2.79), and −0.007 to −0.013 in each of 2022–2025 (t −0.74 to −0.78). The net-move slope does the same: 2018–21 0.0154 (t 3.00, 1278 cases), 2022–25 −0.0012 (t −0.28, 1277 cases).
