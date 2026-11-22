---
brief: 028_volume-confirmed-hourly-moves-continue
source-idea: 028-02_volume-surge-down-continuation.b1_volume-surge-rise-continues-daylong.b1_volume-surge-rise-more-coins
line: 7.d not profitable
backtest: 028-02_volume-surge-down-continuation.b1_volume-surge-rise-continues-daylong.b1_volume-surge-rise-more-coins_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: After an hour in which the coin rises far more than its typical hourly move over the past 30 days, on volume several times its average hourly volume over the past 30 days, the price keeps rising over the next 24 hours, only while the coin's hourly volatility over the past 7 days is high against its past 30 days. The larger that hour's rise times its relative volume, and the higher that 7-day volatility against the 30-day, the larger the further rise.
Consequence: A trader would buy only right after a surging-volume rise in a coin whose last week has been unusually volatile, and stay out the rest of the time instead of holding the coin through its falls.
Why:
- F1: The book barely differs from holding the coins. It is in a position on 87–93 % of bars for every coin, with mean allocations from 0.53 (ZEC) to 1.03 (BTC). Its 16 980 trades last 103.5 hours on average, and its daily returns correlate 0.89 with holding's. So it inherits holding's falls (deepest fall −71.4 %, Calmar 0.18) with a Sharpe below holding's (0.50 against 0.55).
- F3: The idea's own situation does carry a move. An hour more than 2 usual moves up on more than 2 times the 30-day volume is followed by an unusual +0.32 % over 24 hours (t 2.96, 3 624 cases), which is +0.46 % in total, about 2.4 times the cost. The same rise on ordinary volume (under 1.2 times) gives −0.05 % (t −0.35, 1 829 cases).
- F4: The move grows with the rise times its volume ratio, though not evenly. The lowest quartile of such hours gives +0.15 % (t 0.82) and the highest quartile +0.56 % (t 2.35), 906 cases each.
- F6: The continuation is strongest when the coin's last 7 days are wild against its 30 days. In the top tercile of 7-day over 30-day hourly volatility the move is +0.66 % (t 2.83), against +0.17 % (t 1.15) in the calm tercile and +0.13 % (t 0.74) in the middle tercile, 1 208 cases each.
