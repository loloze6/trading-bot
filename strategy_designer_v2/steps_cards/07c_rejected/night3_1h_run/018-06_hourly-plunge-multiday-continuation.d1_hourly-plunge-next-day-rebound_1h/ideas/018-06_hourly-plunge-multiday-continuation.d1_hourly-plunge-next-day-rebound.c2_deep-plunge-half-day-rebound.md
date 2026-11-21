---
brief: 018_daily-condition-caught-on-the-hour
source-idea: 018-06_hourly-plunge-multiday-continuation.d1_hourly-plunge-next-day-rebound
line: 7.c rejected
backtest: 018-06_hourly-plunge-multiday-continuation.d1_hourly-plunge-next-day-rebound_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's 24-hour return, read at an hourly close, is a drop of several times its 30-day average absolute daily return, the price rises over the next 12 hours by more than the coin's normal 12-hour drift. The larger the drop in those multiples, the larger the rise.
Consequence: A trader buying a deep hourly plunge can expect most of the rebound within half a day, which is a reason to refuse shorting it over that time.
Why:
- F2: The next-day rebound grows with the size of the drop. On non-overlapping 24-hour cases the unusual move is -21 bps (t -3.08, 4991 cases) after drops below 1 multiple, then +37 bps for 1 to 2 multiples (t 3.32), +25 for 2 to 2.5 (t 0.84), +72 for 2.5 to 3 (t 1.87), +150 for 3 to 4 (t 3.55) and +247 beyond 4 (t 3.05); the Spearman rank correlation of drop size against the unusual move is 0.054 beyond 1 multiple.
- F6: The rebound shows at every horizon from 6 hours to 2 days and is clearest over 1 day. After drops of 3 to 4 multiples it is +74 bps over 12 hours (t 2.82), +150 over 24 hours (t 3.55) and +289 over 48 hours (t 3.47). Beyond 3 multiples it is +51 bps over 6 hours (t 4.05). Over 7 days the drop buckets are noisy and not graded (drops of 1.5 to 2 multiples give -207 bps, drops of 2 to 3 multiples give +286).
- F3: The test's own cases diluted the effect: its 8426 cases, mostly mild drops, average +11 bps unusual (0.6 times the 19 bps cost), while the 376 cases of drops beyond 3 multiples average +187 bps unusual and +201 bps total over 24 hours (t 4.62), about 10 times the cost of a trade.
