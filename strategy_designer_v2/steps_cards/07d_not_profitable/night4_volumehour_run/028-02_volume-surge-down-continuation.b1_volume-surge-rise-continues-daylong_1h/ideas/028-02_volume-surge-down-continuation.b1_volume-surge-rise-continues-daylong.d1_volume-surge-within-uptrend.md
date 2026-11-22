---
brief: 028_volume-confirmed-hourly-moves-continue
source-idea: 028-02_volume-surge-down-continuation.b1_volume-surge-rise-continues-daylong
line: 7.d not profitable
backtest: 028-02_volume-surge-down-continuation.b1_volume-surge-rise-continues-daylong_1h
instruments: BTC, ETH
bar: 1h
period: folds A, B, C, D
---
Idea: After an hour in which the coin rises far more than its typical hourly move over the past 30 days, on volume several times its average hourly volume over the past 30 days, the price keeps rising over the next 24 hours, only while the coin's 30-day return is positive. The larger that hour's rise times its relative volume, and the larger the 30-day return, the larger the further rise.
Consequence: A trader would buy surging up-hours only inside an established 30-day uptrend and stay out of the coin when its 30-day return is negative, avoiding the long falls the book now rides.
Why:
- F1: The book is in effect holding the coin: it is positioned on 92.4 % of bars with a mean allocation of 1.00 when in, although the forecast is positive on only 49.3 % of bars (trades last 103 hours on average against a 24-hour bet), and of its mean gain of 0.0062 % per bar, 0.0054 % comes from the market's own rise and only 0.0009 % from timing.
- F2: The book therefore fails both measures in the same way holding fails them. Its Sharpe is 0.596 against holding's 0.636. Its deepest fall is -71 % against holding's -80 %, giving a Calmar of 0.25 against 0.27. On the 1482 of 2898 days spent more than 30 % below its peak, it lost 0.12 % a day while the coins lost 0.10 %.
- F4: What does separate the entries is the trend before them. Entries in the top quintile of the prior 7-day return gain +0.32 % unusual over 24 hours (t 2.55, n 1091), while the middle quintiles lose -0.15 % and -0.14 %. By prior 30-day return, the second quintile loses -0.30 % (t -2.48) and the top two quintiles gain +0.19 % and +0.21 %.
- F5: The trend carries the effect on any bar, not only after a volume surge. Over all 24-hour grid cells, the top prior-7-day quintile gains +0.25 % unusual (t 1.96, n 1072) and the second and third quintiles lose -0.14 % and -0.16 %. While in position, the book earns +0.0153 % per bar when the 30-day return is positive and -0.0052 % when it is negative (52975 and 44419 bars).
