---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.d3_settlement-reversal-in-raised-volatility
line: 7.d confirmed, not profitable
backtest: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.d3_settlement-reversal-in-raised-volatility_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The larger a coin's 1-hour return in the first hour after the 00:00 UTC funding settlement relative to its 24-hour volatility, the more its return over the next 24 hours runs the opposite way, and more so the higher its 24-hour volatility stands against its 30-day volatility, with the reversal growing faster than the shock itself so that the largest settlement-hour moves carry most of the 24-hour give-back.
Consequence: A trader would put nearly all the position on the largest settlement-hour shocks in raised volatility and stay out of the market on ordinary days, cutting the always-in exposure that builds the deep falls.
Why:
- F2: Every window had a fall from peak of at least 10 %, and nine windows had falls deeper than 30 % (w3, w4, w6, w7, w8, w9, w10, w12, w13, w14 range from −31 % to −44 %). The book was in a position on 98 % of coin-days, because a 24-hour hold is re-entered at each 00:00 bar. It therefore carries every case, including the weak ones.
- F3: The gain per case rises steeply with the size of the settlement-hour move. By quintile of |forecast| (about 3,404 independent cases each), the mean 24-hour fade return was +0.15 % (t 1.99), +0.13 % (t 1.46), +0.21 % (t 2.62), +0.41 % (t 4.87) and +0.63 % (t 6.31). The two weakest quintiles earn less than the 0.19 % a trade costs, yet the book still holds them at a mean allocation of 0.11 and 0.24.
- F4: On hour-0 bars split in three by the size of the hour's move against each coin's median move, the fade earned +0.06 % (t 0.63, 2,059 cases) on small moves with raised 24-hour volatility. On large moves with raised volatility it earned +0.66 % (t 5.92, 3,358 cases). Raised volatility pays only when the settlement-hour move itself is large.
- F5: By quintile of the volatility ratio (about 3,087 cases each), the fade earned +0.08 % (t 0.93) in the lowest quintile, rising to +0.43 % (t 3.90) in the highest. The lowest-ratio fifth earns well under the 0.19 % cost.
