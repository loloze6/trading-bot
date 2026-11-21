---
brief: 018_daily-condition-caught-on-the-hour
source-idea: 018-04_hourly-surge-multiday-continuation.d1_surge-near-monthly-high
line: 7.b inconclusive
backtest: 018-04_hourly-surge-multiday-continuation.d1_surge-near-monthly-high_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's 24-hour return, read at an hourly close, first reaches several times its 30-day average absolute daily return on the upside, the price keeps rising over the next 5 days by more than the coin's usual 5-day return, only while the close stands near its 30-day high: the closer the close to its 30-day high at that hour, the larger the rise.
Consequence: A trader would take the surge only when it happens at or near the month's high, and refuse surges that are rebounds inside a month-long decline, which are most of the book's exposure during the coins' shared falls.
Why:
- F1: The tested result is on the side the idea predicts but short of the bar. The mean unusual move over 120 hours is +0.38 % per case (t 1.58, 2364 cases, strength 0.036), about 1.9 times the 0.19 % round-trip cost. At 240 hours the same cases show +0.79 % (t 2.15, 2270 cases, strength 0.050), so the plan's 5-day horizon cuts the move short; this matches the earlier finding that paying moves outlast their stated horizon.
- F5: The effect is spread across coins and is not carried by one of them. Over 120 hours all six coins show a positive mean unusual move, from +0.12 % (XMR) to +0.62 % (ZEC), each with roughly 380 to 410 cases and t between 0.29 and 1.02. On these coins the cases are too noisy to reach t 2, so more coins rather than fewer cases are the way to a clear answer. The 13 other coins have data in folds A and D and in part of B and C.
