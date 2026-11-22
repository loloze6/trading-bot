---
brief: 028_volume-confirmed-hourly-moves-continue
source-idea: 028-03_low-volume-up-fade.b1_quiet-up-hour-fade-wider
line: 7.d not profitable
backtest: 028-03_low-volume-up-fade.b1_quiet-up-hour-fade-wider_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: After an hour in which the coin rises far more than its typical hourly move over the past 30 days while its volume stays near its average hourly volume over the past 30 days, the price gives back part of that rise over the next twelve hours, only when that hour falls in the first four hours of the UTC day; the larger that hour's rise, the larger the giveback.
Consequence: A trader would fade large quiet rises only in the hours just after UTC midnight and hold the fade for about half a day, where the move per trade approaches or exceeds the cost.
Why:
- F1: The book cannot pay at this size: per case the total move over 6 hours is +0.004 % and the unusual move +0.038 % (t 2.10, 19 445 cases), against a cost of 0.19 % per trade, while the book's trades lose 0.29 % to 0.74 % per trade before fees on every coin (BTC −0.29 %, ZEC −0.74 %), so its mean daily return is −0.10 %.
- F3: The fade is concentrated in signals in the first four UTC hours of the day (00–04 UTC): there the unusual move is +0.106 % over 6 hours (t 2.54) and +0.209 % over 12 hours (t 3.46, 3 189 cases), while in the next block (04–08 UTC) it is −0.056 % and −0.125 %.
- F4: Inside those 00–04 UTC signals the fade is graded by the size of the rise: the two largest-rise quintiles give +0.35 % and +0.34 % over 12 hours (t 2.27 and 2.26, total move +0.28 % and +0.27 %, about 1.4 times the cost), and the smallest-rise quintile gives −0.01 %.
- F7: Beyond 12 hours the fade reverses: over 24 hours the unusual move is −0.048 % overall, and after the weakest prior 24-hour returns it is −0.27 % (t −2.87), so holding past half a day gives the gain back.
