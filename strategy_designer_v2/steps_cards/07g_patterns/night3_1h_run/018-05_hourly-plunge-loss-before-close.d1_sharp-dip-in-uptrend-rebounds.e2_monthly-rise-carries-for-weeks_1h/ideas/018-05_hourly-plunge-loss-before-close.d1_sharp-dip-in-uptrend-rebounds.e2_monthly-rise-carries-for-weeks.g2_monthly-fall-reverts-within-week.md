---
brief: 018_daily-condition-caught-on-the-hour
source-idea: 018-05_hourly-plunge-loss-before-close.d1_sharp-dip-in-uptrend-rebounds.e2_monthly-rise-carries-for-weeks
line: 7.g patterns
backtest: 018-05_hourly-plunge-loss-before-close.d1_sharp-dip-in-uptrend-rebounds.e2_monthly-rise-carries-for-weeks_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's 30-day return is negative, the larger that fall in multiples of its usual 30-day move, the more the coin rises above its normal drift over the next week.
Consequence: A deep month-long fall is a reason to hold a long position for about a week rather than to stay out.
Why:
- F1: Below zero, the coin's 30-day return in multiples of its usual 30-day move reverts: regressing excess return over drift on the scaled return, on the negative side only, gives slope -0.0033 with t -3.4 over the next 24 hours (8,339 cases), slope -0.015 with t -2.4 over the next 168 hours (1,182 cases), and t -0.19 over 336 hours (557 cases). The size is small. At 24 hours the deepest bucket (at or below -1) earns only +0.10 % above drift, below the 0.19 % round trip. At 168 hours that bucket earns +0.51 % (t 0.8, 339 cases), but the next bucket (-1 to -0.3) earns -1.54 % (t -3.1, 529 cases), so the grading is not clean.
- F2: The tested idea's positive-side slope holds at shorter horizons too: t 3.1 over 24 hours (8,432 cases), t 2.9 over 168 hours (1,177 cases) and t 2.6 over 336 hours (559 cases). Only the top bucket carries it: scaled return above 1 earns +1.23 % over 168 hours (t 1.9, 542 cases), while the shallow bucket (0 to 0.3) earns -1.96 % (t -3.0, 257 cases).
