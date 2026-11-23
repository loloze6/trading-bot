---
line: 7.d confirmed, not profitable
backtest: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.d1_settlement-shock-extending-crowded-run_1h
idea tested: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.d1_settlement-shock-extending-crowded-run
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4716 USD
---
## Findings
- **F1:** The check failed on Calmar (0.481 against 0.75) because of deep falls rather than a lack of gain. The book earned +15.8 % a year with a Sharpe of 0.74, but its deepest fall was −32.8 %, lasting 361 days from w11 to w14 and bottoming in 2018 while the coins fell 32.0 %. The next falls were −28.3 % (w5–w6, 2023, while the coins rose 20.4 %), −19.3 % (w21, 2024) and −17.5 % (w8–w9, 2019). Across all days the book's correlation with holding is only 0.04.
- **F2:** The fade's effect depends on the coin's 7-day volatility, and the vol-target sizing bets most where the effect is absent. In the lowest quartile of 7-day volatility (per coin) the case fade earns −0.06 % over 24 hours (t −0.68, n 1893); in the top quartile it earns +1.30 % (t 7.95, n 1944). Yet the mean absolute position is 0.62 in the lowest quartile and 0.35 in the top.
- **F3:** The deepest fall (w11–w14) came from the calm cases. There, the position-weighted 24-hour results by 7-day-volatility quartile were −0.75 % (t −3.06, n 93), −0.47 % (t −2.36, n 142) and −0.28 % (t −2.32, n 371), against +0.29 % (t 2.92, n 733) in the top quartile. A fee-free proxy book (positions held 24 hours from each case, chained by window) shows the effect of leaving out the calmest quartile: deepest fall −22.1 % against −26.0 %, Calmar 1.53 against 1.07, Sharpe 1.51 against 1.15.
- **F4:** The fade is larger when the coin's 24-hour volatility is high against its 7-day volatility, and this condition alone does not earn. Aligned cases earn +0.78 % (t 5.80, n 1901) in the top quartile of that ratio against +0.25 % (t 2.29, n 1908) in the bottom. The same fade on non-aligned 00:00 hours in the top quartile earns only +0.15 % (t 1.41, n 2158). The proxy book restricted to the upper half of the ratio has a deepest fall of −15.3 % against −26.0 %, and a Calmar of 1.23 against 1.07.
- **F5:** The long side carries the book and the short side carries the falls.
- **F6:** Within its cases the effect is graded on both of the idea's measures. By quartile of |forecast| the 24-hour fade rises from +0.31 % (t 2.63) to +0.66 % (t 5.63). By quartile of the scaled 23-hour run it rises from +0.27 % to +0.62 % (t 5.43). Each quartile holds about 2040 cases.

## Ideas
- `017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.d1_settlement-shock-extending-crowded-run.d1_settlement-fade-scaled-by-turbulence` (from F1, F2, F3, F6): When the coin's return in the first hour after the 00:00 UTC funding settlement runs the same way as its return over the previous 23 hours, the larger that hour's return relative to its 24-hour volatility, the more the coin's return over the next 24 hours runs the opposite way, and the reversal is larger the higher the coin's volatility over the past 7 days.
- `017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.d1_settlement-shock-extending-crowded-run.d2_settlement-fade-in-volatility-bursts` (from F1, F4, F6): When the coin's return in the first hour after the 00:00 UTC funding settlement runs the same way as its return over the previous 23 hours, the larger that hour's return relative to its 24-hour volatility, the more the coin's return over the next 24 hours runs the opposite way, only while the coin's 24-hour volatility is raised against its 7-day volatility, and more so the higher that ratio.
- `017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.d1_settlement-shock-extending-crowded-run.d3_long-side-settlement-capitulation-rebound` (from F1, F5, F6): When the coin's return in the first hour after the 00:00 UTC funding settlement is a fall that extends its fall over the previous 23 hours, the larger that hour's fall relative to its 24-hour volatility, the more the coin rises over the next 24 hours.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
