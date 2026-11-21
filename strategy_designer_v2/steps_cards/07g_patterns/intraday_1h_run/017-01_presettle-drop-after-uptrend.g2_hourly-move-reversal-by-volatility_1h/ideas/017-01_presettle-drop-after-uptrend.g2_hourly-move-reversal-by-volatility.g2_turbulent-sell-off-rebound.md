---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility
line: 7.g patterns
backtest: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The larger a coin's 1-hour drop against its 24-hour volatility, the more the coin rises over the next 4 hours, and this rebound grows larger the higher its 24-hour volatility is against its past 30 days.
Consequence: A trader would buy after sharp hourly sell-offs during turbulent periods, holding for a few hours, sized by the size of the drop.
Why:
- F3: The reversal is lopsided toward drops. In the top volatility quintile, the hour after a drop larger than 1 standard deviation earns +16.9 bp above the coin's mean (t 7.65, n 8,506), while the hour after an equal rise loses only -5.5 bp (t -2.73, n 8,808). Over all bars, the bottom decile of moves is followed by +4.6 bp (t 7.1) and the top decile by only -1.6 bp (t -2.6).
- F1: The hourly reversal sits almost entirely in high-volatility hours. When 24-hour volatility is ranked against its own past 30 days, the 1-hour slope is 6.20 bp per unit of forecast (t 11.0) in the top quintile, against -0.38 bp (t -1.49) in the bottom quintile, and it rises steadily through the quintiles in between (0.72, 0.87, 1.97 bp).
- F2: The same high-volatility condition holds at longer horizons and gets stronger with them, on non-overlapping samples. Over 4 hours the top quintile gives 13.6 bp (t 6.34, n 19,193), and over 24 hours it gives 64.2 bp (t 5.77, n 3,168). In the bottom quintile the move instead continues: -3.57 bp (t -3.07) over 4 hours and -18.6 bp (t -2.11) over 24 hours.
