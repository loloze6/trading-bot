---
brief: 018_daily-condition-caught-on-the-hour
source-idea: 018-04_hourly-surge-multiday-continuation.b1_hourly-surge-within-weekly-rise
line: 7.d not profitable
backtest: 018-04_hourly-surge-multiday-continuation.b1_hourly-surge-within-weekly-rise_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's 24-hour return, read at an hourly close, first reaches several times its 30-day average absolute daily return on the upside, the price keeps rising over the next 5 days by more than the coin's usual 5-day return, only while its 30-day return is positive. The larger that 30-day return, the larger the rise.
Consequence: A trader buys the hour a large up move first appears only when the coin has risen over the past month, and refuses surges inside a falling month, which is where the book's deepest fall was built.
Why:
- F1: The Calmar fails because of one long fall across the first three windows: the book's deepest fall is 58.5 % over 271 days from w1 to w3, while the coins' average chain fell 62.4 % over the same days. The book lost 16 %, 32 % and 21 % in w1, w2 and w3, against a yearly return of 35.2 %. The next falls are 38 % (w16), 38 % (w19) and 35 % (w21).
- F3: The book earns almost nothing while a coin's 30-day return is negative. Long bars in that state earn 0.145 bps per hour (t 0.9, 116,284 bars), against 1.121 bps (t 5.0, 147,459 bars) when the 30-day return is positive. On the coin itself, the next hour returns 0.37 bps after a falling 30 days and 1.04 bps after a rising one.
- F4: The gain grows with the 30-day return:
- F5: Trades show the same split. Trades entered after a 30-day return below −4.4 % net 1.45 % and 1.94 % on average, with a 10th percentile of −14.9 % in the lowest quintile. Trades in the middle and upper quintiles net 6.09 %, 4.45 % and 2.33 %.
- F6: The tested idea's own gradients are absent:
