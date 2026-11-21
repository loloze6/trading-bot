---
brief: 018_daily-condition-caught-on-the-hour
source-idea: 018-05_hourly-plunge-loss-before-close
line: 7.d not profitable
backtest: 018-05_hourly-plunge-loss-before-close_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's 24-hour return, read at an hourly close, falls by several times its 30-day average absolute daily return while its 30-day return is positive, the coin rises over the next 3 days more than its normal drift, and the larger its 30-day return in multiples of its usual 30-day move, the larger the rise.
Consequence: A sharp one-day drop inside a month-long rise is a reason to buy the dip for a few days rather than to short it, and more so the stronger the month's rise.
Why:
- F1: The book loses because it is short a coin that rises: it held a short on 64 to 77 % of bars on every coin (mean position -0.25 to -0.37) while the coins' mean daily return was +0.119 %, and the book's mean daily return was -0.119 %, the mirror of holding (Sharpe -1.21, 1.77 below holding's).
- F3: The same-day fall the idea bets on is not there: after a first 24-hour drop of 1 to 1.5 times the 30-day average absolute daily move, the excess return over the next 6 hours was +6 bps (t 1.8, 5800 coin-days) and over 24 hours +1 bps (t 0.2); after 1.5 to 3 times it was -5 to -31 bps over 6 hours with t no larger than 1.5 in size, against a round trip of 19 bps.
- F4: After such a drop the coin rebounds over the following days instead: on cases kept at least 5 days apart, the excess return after a drop of 1 to 1.5 times the usual size was +65 bps over 3 days (t 3.0, 1582 cases) and +164 bps over 10 days (t 3.7), that is 3.4 and 8.6 times the cost of a round trip.
- F5: The rebound grows with the coin's prior 30-day return: across quartiles of the volatility-scaled 30-day return the excess 3-day return after a drop was +32, -28, +99 and +183 bps (the top quartile t 3.9, 470 cases), and the 10-day return was +149, -87, +183 and +410 bps (top quartile t 4.2).
- F6: The size of the drop does not grade the rebound: the correlation of the drop's multiple with the 3-day excess return was -0.02, and the 3-day means by drop size were +65, +108 and +102 bps with falling t (3.0, 2.0, 0.7) as the cases thin from 1582 to 274 to 23.
