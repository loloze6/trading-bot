---
brief: 018_daily-condition-caught-on-the-hour
source-idea: 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends
line: 7.b inconclusive
backtest: 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's 24-hour return, read at an hourly close, falls by a large multiple of its 30-day average absolute daily return while its 30-day return is positive, the price rises over the next 8 days by more than the coin's usual 8-day drift, and the larger the fall times the 30-day rise, the larger the rise.
Consequence: A sharp hourly plunge in a coin that has risen over the past month is a reason to buy it and hold it for about eight days, more so the deeper the plunge and the stronger the month's rise.
Why:
- F2: Below the cap the effect is graded the way the idea predicts: by quintile of the raw fall-times-rise value, the top fifth (mean raw 36.4) earns an unusual 96-hour move of +1.85 % (t 3.01, 469 cases), against -0.19 % to +0.45 % for the middle three fifths; on all 701 non-overlapping 96-hour cells with a positive fall and a positive 30-day return, the cells above the product's median beat those below by 1.34 % (Welch t 1.96, 350 against 350), with Spearman rho 0.079 (p 0.035).
- F4: Much of the gain comes from the positive 30-day trend alone, not from the plunge. Grid cells with a positive 30-day return and no 24-hour fall earn +0.77 % unusual over 96 hours (t 2.30, 899 cells). Cells with a modest fall (0 to 2 usual moves) earn between -1.75 % and +0.15 %, and only the deepest plunges, beyond 3 usual moves, earn +8.1 % (t 3.08, 17 cells).
- F5: The move outlasts the 4-day horizon. The cases' total return is +0.36 % at 24 hours (t 3.45), +0.74 % at 48 hours (t 4.83), +0.70 % at 96 hours (t 3.39) and +1.84 % at 192 hours (t 5.73, 2254 cases), as F9 of the earlier runs found for other paying books.
- F6: The idea is large enough to pay its costs. Its total move per case is 6.2 times the 0.19 % round trip and its unusual move 3.6 times; the book earns a Sharpe of 1.02, 0.47 above holding the coins.
