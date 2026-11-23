---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.d1_settlement-shock-extending-crowded-run
line: 7.d confirmed, not profitable
backtest: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.d1_settlement-shock-extending-crowded-run_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When the coin's return in the first hour after the 00:00 UTC funding settlement runs the same way as its return over the previous 23 hours, the larger that hour's return relative to its 24-hour volatility, the more the coin's return over the next 24 hours runs the opposite way, only while the coin's 24-hour volatility is raised against its 7-day volatility, and more so the higher that ratio.
Consequence: A trader would fade the aligned settlement hour when the last day has been unusually turbulent for the coin, and hold back when it has been quiet, which cuts the depth of the falls.
Why:
- F1: The check failed on Calmar (0.481 against 0.75) because of deep falls rather than a lack of gain. The book earned +15.8 % a year with a Sharpe of 0.74, but its deepest fall was −32.8 %, lasting 361 days from w11 to w14 and bottoming in 2018 while the coins fell 32.0 %. The next falls were −28.3 % (w5–w6, 2023, while the coins rose 20.4 %), −19.3 % (w21, 2024) and −17.5 % (w8–w9, 2019). Across all days the book's correlation with holding is only 0.04.
- F4: The fade is larger when the coin's 24-hour volatility is high against its 7-day volatility, and this condition alone does not earn. Aligned cases earn +0.78 % (t 5.80, n 1901) in the top quartile of that ratio against +0.25 % (t 2.29, n 1908) in the bottom. The same fade on non-aligned 00:00 hours in the top quartile earns only +0.15 % (t 1.41, n 2158). The proxy book restricted to the upper half of the ratio has a deepest fall of −15.3 % against −26.0 %, and a Calmar of 1.23 against 1.07.
- F6: Within its cases the effect is graded on both of the idea's measures. By quartile of |forecast| the 24-hour fade rises from +0.31 % (t 2.63) to +0.66 % (t 5.63). By quartile of the scaled 23-hour run it rises from +0.27 % to +0.62 % (t 5.43). Each quartile holds about 2040 cases.
