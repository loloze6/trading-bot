---
brief: 028_volume-confirmed-hourly-moves-continue
source-idea: 028-02_volume-surge-down-continuation.b1_volume-surge-rise-continues-daylong.b1_volume-surge-rise-more-coins
line: 7.d not profitable
backtest: 028-02_volume-surge-down-continuation.b1_volume-surge-rise-continues-daylong.b1_volume-surge-rise-more-coins_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: After an hour in which the coin falls far more than its typical hourly move over the past 30 days, on volume several times its average hourly volume over the past 30 days, the price rises over the next 24 hours. The larger that hour's fall times its relative volume, the larger the rise.
Consequence: A trader would buy after a sharp fall on surging volume and hold for about a day, and refuse to short such hours.
Why:
- F7: A fall on surging volume reverses rather than continues. An hour more than 2 usual moves down on more than 2 times the volume is followed by a rise of 0.38 % above drift over 24 hours (t 3.67 against the fall's direction, 3 932 cases). The rise is 0.35 % (t 2.36) when the coin's 30-day return is positive.
- F1: The book barely differs from holding the coins. It is in a position on 87–93 % of bars for every coin, with mean allocations from 0.53 (ZEC) to 1.03 (BTC). Its 16 980 trades last 103.5 hours on average, and its daily returns correlate 0.89 with holding's. So it inherits holding's falls (deepest fall −71.4 %, Calmar 0.18) with a Sharpe below holding's (0.50 against 0.55).
