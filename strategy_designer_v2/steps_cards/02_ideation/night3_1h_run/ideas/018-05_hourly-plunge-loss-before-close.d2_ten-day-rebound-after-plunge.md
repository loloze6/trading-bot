---
brief: 018_daily-condition-caught-on-the-hour
source-idea: 018-05_hourly-plunge-loss-before-close
line: 7.d not profitable
backtest: 018-05_hourly-plunge-loss-before-close_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's 24-hour return, read at an hourly close, falls by several times its 30-day average absolute daily return, the coin rises over the next 10 days more than its normal drift, and the larger its 30-day return before the drop, the larger the rise.
Consequence: A trader who holds the rebound after a sharp drop for about ten days captures a move several times the cost of a round trip, which a short held for one day gives back.
Why:
- F4: After such a drop the coin rebounds over the following days instead: on cases kept at least 5 days apart, the excess return after a drop of 1 to 1.5 times the usual size was +65 bps over 3 days (t 3.0, 1582 cases) and +164 bps over 10 days (t 3.7), that is 3.4 and 8.6 times the cost of a round trip.
- F5: The rebound grows with the coin's prior 30-day return: across quartiles of the volatility-scaled 30-day return the excess 3-day return after a drop was +32, -28, +99 and +183 bps (the top quartile t 3.9, 470 cases), and the 10-day return was +149, -87, +183 and +410 bps (top quartile t 4.2).
- F7: The book trades far more than its edge allows: 24,461 trades with a median length of 29 hours lost 0.97 % each before fees and 1.07 % after, with turnover of 0.33 to 0.54 of the book per day.
