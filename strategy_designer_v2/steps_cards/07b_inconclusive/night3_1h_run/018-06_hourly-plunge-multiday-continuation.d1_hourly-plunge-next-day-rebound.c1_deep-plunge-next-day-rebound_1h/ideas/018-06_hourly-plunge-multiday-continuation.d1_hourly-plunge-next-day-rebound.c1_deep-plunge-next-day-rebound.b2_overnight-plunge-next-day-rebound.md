---
brief: 018_daily-condition-caught-on-the-hour
source-idea: 018-06_hourly-plunge-multiday-continuation.d1_hourly-plunge-next-day-rebound.c1_deep-plunge-next-day-rebound
line: 7.b inconclusive
backtest: 018-06_hourly-plunge-multiday-continuation.d1_hourly-plunge-next-day-rebound.c1_deep-plunge-next-day-rebound_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's 24-hour return, read at an hourly close, is a drop of several times its 30-day average absolute daily return, the price rises over the next 1 day by more than the coin's normal 1-day drift, only while that hourly close falls in the late evening or early hours UTC (18:00 to 06:00). The larger the drop in those multiples, the larger the rise.
Consequence: A trader should buy a deep fresh plunge for a day when it is read overnight in UTC, and refuse the same plunge when it is read in the European morning.
Why:
- F2: The effect is graded as the idea says and lives in the deepest drops. At 24 hours, forecast 20 cases (drops of 2 multiples or more) gain +0.58 % (t 2.46, 693 cases), forecast 10 to 20 gain +0.19 % (t 1.21, 1167), forecast 4 to 10 gain +0.17 % (t 1.66, 2733), and forecast up to 4 lose -0.04 % (t -0.55, 3833). The shallow cases make up 45 % of the sample and dilute the mean.
- F6: The 24-hour rebound depends on the hour of the signal's close, and the pattern is stable across both halves of the data.
