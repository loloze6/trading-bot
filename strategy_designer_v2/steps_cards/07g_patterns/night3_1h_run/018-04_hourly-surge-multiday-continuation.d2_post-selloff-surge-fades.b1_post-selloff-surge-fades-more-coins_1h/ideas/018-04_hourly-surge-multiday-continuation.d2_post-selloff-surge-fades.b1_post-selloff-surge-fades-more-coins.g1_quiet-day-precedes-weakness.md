---
brief: 018_daily-condition-caught-on-the-hour
source-idea: 018-04_hourly-surge-multiday-continuation.d2_post-selloff-surge-fades.b1_post-selloff-surge-fades-more-coins
line: 7.g patterns
backtest: 018-04_hourly-surge-multiday-continuation.d2_post-selloff-surge-fades.b1_post-selloff-surge-fades-more-coins_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1h
period: folds A, B, C, D
---
Idea: The quieter a coin's last 24 hours have been compared with its own past 30 days, the further its price falls below its usual 5-day return over the next 5 days.
Consequence: A trader would lean short, or stay out of longs, on a coin whose day has gone unusually quiet, and more so the quieter it is.
Why:
- F1: The calmer the last 24 hours compared with the coin's past 30 days, the weaker the next 5 days. The ratio used is the 24-hour standard deviation of hourly returns over the 720-hour one, split into quintiles within each coin. After the calmest fifth, the drift-removed 120-hour return has a strength of -0.111 (t -4.26, 1,327 non-overlapping cases), or -1.31 %. After the most agitated fifth it is +0.055 (t 1.81, 1,326 cases), or +0.77 %. The quintiles in between rise almost steadily (-0.048, +0.002, +0.049).
- F2: The calm-before-weakness pattern holds across coins, windows and the recent years.
- F4: The pattern is large next to the cost of a trade. The calm fifth's -1.31 % unusual move over 5 days is about 6 times the 0.22 % round trip. After removing the coin's +0.85 % normal 5-day rise, a short there would still capture about 0.46 % in total, about 2 times the cost. At 2 days the calm fifth is -0.50 % (t -3.95); at 10 days, -1.64 % (t -2.38).
