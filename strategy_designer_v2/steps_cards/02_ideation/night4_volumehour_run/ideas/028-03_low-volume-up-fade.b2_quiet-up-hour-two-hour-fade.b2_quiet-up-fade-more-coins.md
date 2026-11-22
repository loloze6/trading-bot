---
brief: 028_volume-confirmed-hourly-moves-continue
source-idea: 028-03_low-volume-up-fade.b2_quiet-up-hour-two-hour-fade
line: 7.b inconclusive
backtest: 028-03_low-volume-up-fade.b2_quiet-up-hour-two-hour-fade_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: After an hour in which the coin rises far more than its typical hourly move over the past 30 days while its volume stays near its average hourly volume over the past 30 days, the price gives back part of that rise over the next two hours. The larger that hour's rise, the larger the giveback.
Consequence: A trader would refuse to chase a quiet-volume hourly rise for the next two hours, since its first hours more often slip back than extend.
Why:
- F1: The test's positive result comes from the largest quiet-volume rises only. Rises above 3 times the 30-day mean absolute hourly move, on volume 0.67–1.5 times its 30-day mean, give back 16.7 bp over 2 hours (t 2.15, 322 non-overlapping cases), 20.2 bp over 4 hours (t 1.50, 170) and 30.2 bp over 6 hours (t 1.37, 101), with strength 0.14 to 0.17. Quiet rises of 2–3 times give −4.8 bp (t −1.15, 834), and those of 1–2 times give +1.0 bp (t 0.44, 2,771).
- F3: Measured on the scaled rise itself instead of the clipped forecast, the grade is positive. Among quiet rises above 2 times, the slope over 2 hours is 11.1 bp per unit (t 2.31, 1,156 cases). Among rises above 1 times, the slope is 10.7 bp per unit over 4 hours (t 2.28, 2,019) and 14.6 bp per unit over 6 hours (t 1.97, 1,322).
