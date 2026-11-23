---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.g1_weekend-post-settlement-shock-reversal
line: 7.g patterns
backtest: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.g1_weekend-post-settlement-shock-reversal_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: On a Saturday or Sunday, the larger a coin's 12-hour return up to 21:00 UTC, relative to its 24-hour volatility, the more its return over the next 24 hours runs the opposite way.
Consequence: A trader would fade the weekend's daytime move in the evening, sizing the fade with the move, and would refuse to fade the same move on a weekday evening.
Why:
- F1: On Saturday and Sunday, the 12-hour move to the close of the 20:00 UTC bar, scaled by 24-hour volatility, is followed by a 24-hour excess return the opposite way: the slope is 43.8 bp per unit with t 6.04 over 4854 non-overlapping cases. On weekdays at the same hour the slope is −9.7 bp (t −2.24, 12259 cases).
- F2: That weekend 12-hour fade holds on every coin, with slopes from +24 bp (BTC, t 1.81) to +56 bp (XMR, t 3.43; LTC t 3.07, XRP 2.40, ZEC 2.33, ETH 1.88). It holds on both weekend days: Saturday +59 bp (t 6.18), Sunday +31 bp (t 2.87). Monday to Friday are all between −17 and 0 bp, with |t| ≤ 1.8.
- F3: By year, the weekend 12-hour fade is positive in 7 of 8 years (2019 t 5.1, 2022 t 4.8, 2024 t 3.8), but it reverses in 2025 (−39 bp, t −2.03).
