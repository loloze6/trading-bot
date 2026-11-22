---
brief: 028_volume-confirmed-hourly-moves-continue
source-idea: 028-03_low-volume-up-fade.b1_quiet-up-hour-fade-wider
line: 7.d not profitable
backtest: 028-03_low-volume-up-fade.b1_quiet-up-hour-fade-wider_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: After an hour in which the coin rises far more than its typical hourly move over the past 30 days while its volume stays near its average hourly volume over the past 30 days, the price gives back part of that rise over the next six hours, and the giveback grows both with the size of that hour's rise and with how far that hour's volume falls below its 30-day average.
Consequence: A trader would size a fade of a large rise by how thin its volume was, and would take only a small fade when the volume came close to a surge.
Why:
- F6: The fade weakens as the hour's volume approaches the top of the ordinary band: the unusual move is +0.043 % over 1 hour (t 2.86) and +0.058 % over 6 hours (t 1.63) in the lowest volume-ratio quartile, and −0.002 % and −0.005 % in the highest (1.2 to 2.6 times average volume).
- F1: The book cannot pay at this size: per case the total move over 6 hours is +0.004 % and the unusual move +0.038 % (t 2.10, 19 445 cases), against a cost of 0.19 % per trade, while the book's trades lose 0.29 % to 0.74 % per trade before fees on every coin (BTC −0.29 %, ZEC −0.74 %), so its mean daily return is −0.10 %.
