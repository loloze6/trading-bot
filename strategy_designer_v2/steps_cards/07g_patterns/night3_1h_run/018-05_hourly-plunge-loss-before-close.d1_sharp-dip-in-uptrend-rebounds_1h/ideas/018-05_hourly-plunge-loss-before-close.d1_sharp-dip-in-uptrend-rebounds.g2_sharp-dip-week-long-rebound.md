---
brief: 018_daily-condition-caught-on-the-hour
source-idea: 018-05_hourly-plunge-loss-before-close.d1_sharp-dip-in-uptrend-rebounds
line: 7.g patterns
backtest: 018-05_hourly-plunge-loss-before-close.d1_sharp-dip-in-uptrend-rebounds_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's 24-hour return, read at an hourly close, is a fall of several of its 30-day mean absolute 24-hour returns, the coin rises over the next 7 days more than its normal drift, and the deeper the fall in those multiples, the larger the rise.
Consequence: A sharp one-day drop is a reason to hold a rebound long for about a week, not just three days.
Why:
- F3: After a sharp fall, the rebound keeps growing past the tested horizon. On the 611 deepest-fall cases the unusual move is +0.78 % over 24 hours (t 3.46), +1.12 % over 72 hours (t 3.36, strength 0.13) and +1.82 % over 168 hours (t 3.30, 589 cases).
- F4: Among falls, a deeper 24-hour fall is followed by a larger 72-hour move. The Spearman rho is 0.083 (p 0.00015, 2054 cases). Inside a positive 30-day return, the deepest quartile of falls gives +2.17 % (t 3.78, 238 cases, strength 0.26). Inside a negative 30-day return, the same quartile gives only +0.62 % (t 1.33, 276 cases).
- F7: The book's worst days are followed by recoveries. On its worst decile of days (mean -4.75 %, coin -5.67 %), the next day's coin return is +0.72 % and the book's is +0.65 %. Both are larger than after any of the middle eight deciles (at most +0.28 % and +0.19 %).
