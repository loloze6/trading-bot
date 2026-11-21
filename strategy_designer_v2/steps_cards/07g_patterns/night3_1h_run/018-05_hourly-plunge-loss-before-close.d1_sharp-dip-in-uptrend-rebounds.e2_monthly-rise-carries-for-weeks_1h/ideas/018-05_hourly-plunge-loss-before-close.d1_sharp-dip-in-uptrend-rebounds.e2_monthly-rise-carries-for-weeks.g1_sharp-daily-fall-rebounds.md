---
brief: 018_daily-condition-caught-on-the-hour
source-idea: 018-05_hourly-plunge-loss-before-close.d1_sharp-dip-in-uptrend-rebounds.e2_monthly-rise-carries-for-weeks
line: 7.g patterns
backtest: 018-05_hourly-plunge-loss-before-close.d1_sharp-dip-in-uptrend-rebounds.e2_monthly-rise-carries-for-weeks_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The larger a coin's 1-day fall in multiples of its usual daily move, the more the coin rises above its normal drift over the next day.
Consequence: A sharp daily fall is a reason to buy for one day, and a mild one is not.
Why:
- F3: After a day whose return is at least 2.5 times the coin's 30-day standard deviation of daily returns on the downside, the next day is +1.14 % above the coin's mean (t 2.3, 208 cases). This is about 6 times the 0.19 % round trip. The effect shrinks for smaller falls: +0.28 % for falls of 1.5 to 2.5 times (t 1.4, 562 cases) and +0.17 % for 0.5 to 1.5 times (t 1.7, 2,548 cases). It does not last a week: -1.13 % over the next 7 days for the deepest falls. This t is modest given the many angles looked at.
- F1: Below zero, the coin's 30-day return in multiples of its usual 30-day move reverts: regressing excess return over drift on the scaled return, on the negative side only, gives slope -0.0033 with t -3.4 over the next 24 hours (8,339 cases), slope -0.015 with t -2.4 over the next 168 hours (1,182 cases), and t -0.19 over 336 hours (557 cases). The size is small. At 24 hours the deepest bucket (at or below -1) earns only +0.10 % above drift, below the 0.19 % round trip. At 168 hours that bucket earns +0.51 % (t 0.8, 339 cases), but the next bucket (-1 to -0.3) earns -1.54 % (t -3.1, 529 cases), so the grading is not clean.
