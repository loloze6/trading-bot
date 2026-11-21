---
brief: 018_daily-condition-caught-on-the-hour
source-idea: 018-05_hourly-plunge-loss-before-close.d1_sharp-dip-in-uptrend-rebounds.b1_deeper-dip-larger-rebound
line: 7.d not profitable
backtest: 018-05_hourly-plunge-loss-before-close.d1_sharp-dip-in-uptrend-rebounds.b1_deeper-dip-larger-rebound_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's 24-hour return, read at an hourly close, falls by several times its 30-day average absolute daily return while its 30-day return is positive, the coin rises over the next 3 days more than its normal drift, and the closer the coin's close is to its 30-day high, the larger the rise.
Consequence: A sharp drop taken near the month's high is a reason to buy for a few days, while one taken far below the high is a reason to hold back, because those dips carry most of the deep losses.
Why:
- F1: The check fails on Calmar alone (0.60 against 0.75). The chained book's deepest fall is −33.0 % against a yearly return of +19.9 %, and that fall runs 217 days from w1 to w3, while holding the coins lost 65.9 % over the same stretch. Book returns were −6.6 %, −13.9 % and −8.0 % in w1, w2 and w3, and its deepest falls inside one window are −23.8 % (w3), −21.9 % (w14) and −20.6 % (w18), all windows where holding lost (−10 %, −49 %, −22 %).
- F4: Losses cluster in dips taken far below the coin's 30-day high.
