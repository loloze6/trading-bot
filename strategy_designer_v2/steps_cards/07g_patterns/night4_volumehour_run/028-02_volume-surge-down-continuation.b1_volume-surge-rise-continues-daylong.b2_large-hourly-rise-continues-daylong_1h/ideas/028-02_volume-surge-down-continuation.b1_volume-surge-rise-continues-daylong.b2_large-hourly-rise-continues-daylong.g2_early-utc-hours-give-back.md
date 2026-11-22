---
brief: 028_volume-confirmed-hourly-moves-continue
source-idea: 028-02_volume-surge-down-continuation.b1_volume-surge-rise-continues-daylong.b2_large-hourly-rise-continues-daylong
line: 7.g patterns
backtest: 028-02_volume-surge-down-continuation.b1_volume-surge-rise-continues-daylong.b2_large-hourly-rise-continues-daylong_1h
instruments: BTC, ETH
bar: 1h
period: folds A, B, C, D
---
Idea: Each coin falls more than its usual hourly drift over the 00:00–03:00 UTC hours. The larger its rise over the preceding 20:00–00:00 UTC hours, the larger that fall.
Consequence: A trader would avoid entering longs just after midnight UTC and would time exits of long trades before those hours rather than after.
Why:
- F4: The opposite holds around the start of the UTC day. Hour 2 averages −0.032 % (t −3.35), hour 1 −0.023 % (t −2.22) and hour 0 −0.023 % (t −1.97). Only hour 2 clears the bar for 24 hours tested.
- F1: Hourly returns between 20:00 and 22:00 UTC beat the coin's mean hourly return in both coins. Hour 20 averages +0.045 % (t 4.00) and hour 21 +0.040 % (t 3.69), about 5,840 hours each. These are the only two of 24 hours with a t above 3, so they stand out even after testing every hour. Pooled over both hours, BTC averages +0.037 % (t 3.81, 5,837 hours) and ETH +0.048 % (t 3.92, 5,837 hours).
