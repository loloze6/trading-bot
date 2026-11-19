---
brief: 016_grind-versus-jump-moves
source-idea: 016-04_down-jump-price-reversal.g1_volatile-regime-daily-move-reversal
line: 7.d not profitable
backtest: 016-04_down-jump-price-reversal.g1_volatile-regime-daily-move-reversal_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The larger a coin's 24-hour fall measured in units of its past 7-day hourly volatility, the more it rises over the next 24 hours, and the more so the higher its 7-day volatility stands above its own 30-day usual level.
Consequence: After a sharp one-day fall in an unusually volatile coin, buy for a day, and buy more the larger the fall and the higher the volatility.
Why:
- F3: The gain sits entirely in the highest third of volatility ratio (7-day volatility over its 30-day average): on the 24-hour grid that third earns +0.0077 per case, against +0.0001 for the middle third and −0.0007 for the lowest; in the hourly book it earns +0.00197 a day before fees, against −0.00083 in the lowest third.
- F4: Inside the high-volatility third, long positions after falls catch a signed 24-hour return of +0.0078 (n 2,467), against +0.0022 for short positions after rises (n 2,654); in the low-volatility third, short positions lose 0.0021 (n 2,582) because the coins drift up.
