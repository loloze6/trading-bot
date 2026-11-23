---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.d1_settlement-shock-extending-crowded-run
line: 7.d confirmed, not profitable
backtest: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.d1_settlement-shock-extending-crowded-run_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When the coin's return in the first hour after the 00:00 UTC funding settlement runs the same way as its return over the previous 23 hours, the larger that hour's return relative to its 24-hour volatility, the more the coin's return over the next 24 hours runs the opposite way, and the reversal is larger the higher the coin's volatility over the past 7 days.
Consequence: A trader would size the fade of an aligned post-settlement hour up with the coin's 7-day volatility, not down with it, and take little position in a calm week, where the fade carried the deepest fall.
Why:
- F1: The check failed on Calmar (0.481 against 0.75) because of deep falls rather than a lack of gain. The book earned +15.8 % a year with a Sharpe of 0.74, but its deepest fall was −32.8 %, lasting 361 days from w11 to w14 and bottoming in 2018 while the coins fell 32.0 %. The next falls were −28.3 % (w5–w6, 2023, while the coins rose 20.4 %), −19.3 % (w21, 2024) and −17.5 % (w8–w9, 2019). Across all days the book's correlation with holding is only 0.04.
- F2: The fade's effect depends on the coin's 7-day volatility, and the vol-target sizing bets most where the effect is absent. In the lowest quartile of 7-day volatility (per coin) the case fade earns −0.06 % over 24 hours (t −0.68, n 1893); in the top quartile it earns +1.30 % (t 7.95, n 1944). Yet the mean absolute position is 0.62 in the lowest quartile and 0.35 in the top.
- F3: The deepest fall (w11–w14) came from the calm cases. There, the position-weighted 24-hour results by 7-day-volatility quartile were −0.75 % (t −3.06, n 93), −0.47 % (t −2.36, n 142) and −0.28 % (t −2.32, n 371), against +0.29 % (t 2.92, n 733) in the top quartile. A fee-free proxy book (positions held 24 hours from each case, chained by window) shows the effect of leaving out the calmest quartile: deepest fall −22.1 % against −26.0 %, Calmar 1.53 against 1.07, Sharpe 1.51 against 1.15.
- F6: Within its cases the effect is graded on both of the idea's measures. By quartile of |forecast| the 24-hour fade rises from +0.31 % (t 2.63) to +0.66 % (t 5.63). By quartile of the scaled 23-hour run it rises from +0.27 % to +0.62 % (t 5.43). Each quartile holds about 2040 cases.
