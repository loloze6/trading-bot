---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility
line: 7.g patterns
backtest: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The higher a coin's 24-hour volatility is against its own past 30 days, the more its 1-day return, measured against that volatility, is followed by a move the opposite way over the next 1 day.
Consequence: In turbulent stretches a trader would fade a coin's large daily move with a position held about a day, which brings turnover far below that of hourly trading.
Why:
- F1: The hourly reversal sits almost entirely in high-volatility hours. When 24-hour volatility is ranked against its own past 30 days, the 1-hour slope is 6.20 bp per unit of forecast (t 11.0) in the top quintile, against -0.38 bp (t -1.49) in the bottom quintile, and it rises steadily through the quintiles in between (0.72, 0.87, 1.97 bp).
- F2: The same high-volatility condition holds at longer horizons and gets stronger with them, on non-overlapping samples. Over 4 hours the top quintile gives 13.6 bp (t 6.34, n 19,193), and over 24 hours it gives 64.2 bp (t 5.77, n 3,168). In the bottom quintile the move instead continues: -3.57 bp (t -3.07) over 4 hours and -18.6 bp (t -2.11) over 24 hours.
- F4: The high-volatility reversal holds on every coin and in 7 of 8 years.
- F5: The book loses because of turnover, not because the signal is wrong.
