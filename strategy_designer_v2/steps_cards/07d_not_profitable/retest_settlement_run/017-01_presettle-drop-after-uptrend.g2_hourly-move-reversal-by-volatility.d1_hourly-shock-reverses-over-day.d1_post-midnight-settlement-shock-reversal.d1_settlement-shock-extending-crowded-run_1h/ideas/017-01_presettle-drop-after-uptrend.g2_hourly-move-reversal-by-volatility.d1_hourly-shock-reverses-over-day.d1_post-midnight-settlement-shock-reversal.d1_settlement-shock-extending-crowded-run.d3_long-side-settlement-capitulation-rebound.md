---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.d1_settlement-shock-extending-crowded-run
line: 7.d confirmed, not profitable
backtest: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.d1_settlement-shock-extending-crowded-run_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When the coin's return in the first hour after the 00:00 UTC funding settlement is a fall that extends its fall over the previous 23 hours, the larger that hour's fall relative to its 24-hour volatility, the more the coin rises over the next 24 hours.
Consequence: A trader would buy the post-settlement hour that extends a crowded down-run, sized by the move, and leave out the short fade of an extended up-run, which carried the falls against the coin's drift.
Why:
- F1: The check failed on Calmar (0.481 against 0.75) because of deep falls rather than a lack of gain. The book earned +15.8 % a year with a Sharpe of 0.74, but its deepest fall was −32.8 %, lasting 361 days from w11 to w14 and bottoming in 2018 while the coins fell 32.0 %. The next falls were −28.3 % (w5–w6, 2023, while the coins rose 20.4 %), −19.3 % (w21, 2024) and −17.5 % (w8–w9, 2019). Across all days the book's correlation with holding is only 0.04.
- F5: The long side carries the book and the short side carries the falls.
- F6: Within its cases the effect is graded on both of the idea's measures. By quartile of |forecast| the 24-hour fade rises from +0.31 % (t 2.63) to +0.66 % (t 5.63). By quartile of the scaled 23-hour run it rises from +0.27 % to +0.62 % (t 5.43). Each quartile holds about 2040 cases.
