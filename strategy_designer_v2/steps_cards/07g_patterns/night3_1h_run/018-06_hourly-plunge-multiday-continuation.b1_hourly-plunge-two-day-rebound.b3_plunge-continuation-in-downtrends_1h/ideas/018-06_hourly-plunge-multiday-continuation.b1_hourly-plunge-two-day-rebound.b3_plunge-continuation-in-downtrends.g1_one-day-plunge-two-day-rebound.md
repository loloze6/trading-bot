---
brief: 018_daily-condition-caught-on-the-hour
source-idea: 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b3_plunge-continuation-in-downtrends
line: 7.g patterns
backtest: 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b3_plunge-continuation-in-downtrends_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's 24-hour return, read at an hourly close, falls by a large multiple of its 30-day average absolute daily return, the price rises over the next 2 days by more than the coin's usual 2-day drift, and the larger the fall relative to that average, the larger the rebound.
Consequence: A sharp one-day plunge is a reason to buy the dip for two days and a reason to refuse a short on it.
Why:
- F1: Large 24-hour plunges rebound instead of continuing. When the 24-hour return is at or below -2.5 times its 30-day mean absolute 24-hour return, the next 24 hours show a strength of +0.295 (t 4.67, 459 independent cases), an unusual move of +1.50 % and a total move of +1.64 %. Over the next 48 hours the strength is +0.344 (t 3.87, 222 cases), the unusual move +2.27 % and the total move +2.55 %, about 12 and 13 times the 0.19 % cost of a trade. The rebound holds whether the 30-day return is negative (24 h: +0.302, t 3.57, 314 cases) or positive (+0.279, t 3.51, 145 cases).
- F2: The rebound is graded, and it is gone by 4 days. Over all falls, the slope of the next-day strength on the size of the fall is -0.077 (t -5.9, 6327 cases), and the same over the next 2 days (-0.077, t -4.16, 3131 cases). The slope over falls is negative on all 6 coins (XRP -0.126, t -4.0; ZEC -0.121, t -3.6; ETH -0.084, t -2.5; XMR -0.075, t -2.4; BTC -0.043; LTC -0.037). At the tested 96-hour horizon the plunge cases have a strength of -0.027 (t -0.18, 106 cases), so the tested horizon sits after the rebound has ended.
- F3: The next-day plunge rebound spreads across windows and coins, but not across all years:
- F4: The tested short book lost because it shorted into the rebound. Its trades lost before fees on 5 of 6 coins (mean gross -0.48 % to -2.28 %, only BTC +0.37 %), won only 29 % to 37 % of the time, and its deepest-forecast quartile lost -1.03 % gross per trade.
