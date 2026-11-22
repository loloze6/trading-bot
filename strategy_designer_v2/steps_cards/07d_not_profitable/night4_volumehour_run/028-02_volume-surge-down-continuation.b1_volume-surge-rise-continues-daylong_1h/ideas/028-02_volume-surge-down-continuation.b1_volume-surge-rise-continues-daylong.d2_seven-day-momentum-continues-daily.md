---
brief: 028_volume-confirmed-hourly-moves-continue
source-idea: 028-02_volume-surge-down-continuation.b1_volume-surge-rise-continues-daylong
line: 7.d not profitable
backtest: 028-02_volume-surge-down-continuation.b1_volume-surge-rise-continues-daylong_1h
instruments: BTC, ETH
bar: 1h
period: folds A, B, C, D
---
Idea: The higher a coin's 7-day return, the more it keeps rising over the next 24 hours, beyond its normal drift.
Consequence: A trader would hold the coin long in proportion to its 7-day strength and step aside when that strength fades, instead of holding through every fall.
Why:
- F4: What does separate the entries is the trend before them. Entries in the top quintile of the prior 7-day return gain +0.32 % unusual over 24 hours (t 2.55, n 1091), while the middle quintiles lose -0.15 % and -0.14 %. By prior 30-day return, the second quintile loses -0.30 % (t -2.48) and the top two quintiles gain +0.19 % and +0.21 %.
- F5: The trend carries the effect on any bar, not only after a volume surge. Over all 24-hour grid cells, the top prior-7-day quintile gains +0.25 % unusual (t 1.96, n 1072) and the second and third quintiles lose -0.14 % and -0.16 %. While in position, the book earns +0.0153 % per bar when the 30-day return is positive and -0.0052 % when it is negative (52975 and 44419 bars).
- F2: The book therefore fails both measures in the same way holding fails them. Its Sharpe is 0.596 against holding's 0.636. Its deepest fall is -71 % against holding's -80 %, giving a Calmar of 0.25 against 0.27. On the 1482 of 2898 days spent more than 30 % below its peak, it lost 0.12 % a day while the coins lost 0.10 %.
