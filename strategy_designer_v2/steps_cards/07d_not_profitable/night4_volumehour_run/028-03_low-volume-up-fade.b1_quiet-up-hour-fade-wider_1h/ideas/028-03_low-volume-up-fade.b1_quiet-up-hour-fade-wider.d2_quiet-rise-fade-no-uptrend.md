---
brief: 028_volume-confirmed-hourly-moves-continue
source-idea: 028-03_low-volume-up-fade.b1_quiet-up-hour-fade-wider
line: 7.d not profitable
backtest: 028-03_low-volume-up-fade.b1_quiet-up-hour-fade-wider_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: After an hour in which the coin rises far more than its typical hourly move over the past 30 days while its volume stays near its average hourly volume over the past 30 days, the price gives back part of that rise over the next twelve hours, only while the coin has fallen or held flat over the past 3 days; the larger that hour's rise, the larger the giveback.
Consequence: A trader would refuse to fade quiet rises inside a 3-day advance, where they carry on, and would fade them after flat or falling days.
Why:
- F2: The book is short against coins that rise, which costs it on the failing Sharpe-against-holding measure: its mean position is short on every coin (−0.11 on ZEC to −0.26 on BTC, short 40–45 % of bars), the coins' mean daily return is +0.07 % to +0.16 %, and the book's mean daily return is −0.08 % to −0.14 % per coin.
- F5: The fade over 12 hours holds only after flat or falling 3-day returns: the unusual move is +0.117 % (t 2.57) and +0.072 % (t 1.66) in the second and middle quintiles of the 3-day return, and −0.085 % (t −1.79) and −0.034 % in the two highest, where the total move of the short is −0.15 % (t −3.21) and −0.10 %.
- F1: The book cannot pay at this size: per case the total move over 6 hours is +0.004 % and the unusual move +0.038 % (t 2.10, 19 445 cases), against a cost of 0.19 % per trade, while the book's trades lose 0.29 % to 0.74 % per trade before fees on every coin (BTC −0.29 %, ZEC −0.74 %), so its mean daily return is −0.10 %.
