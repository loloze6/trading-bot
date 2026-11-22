---
brief: 028_volume-confirmed-hourly-moves-continue
source-idea: 028-02_volume-surge-down-continuation.d2_heavy-volume-surge-continues-upward.b1_true-volume-surges-continue-up
line: 7.d not profitable
backtest: 028-02_volume-surge-down-continuation.d2_heavy-volume-surge-continues-upward.b1_true-volume-surges-continue-up_1h
instruments: BTC, ETH
bar: 1h
period: folds A, B, C, D
---
Idea: After an hour in which the coin falls far more than its typical hourly move over the past 30 days, on volume several times its average hourly volume over the past 30 days, the price rebounds over the next four hours. The larger that hour's fall relative to its typical 30-day hourly move times its volume relative to its 30-day average, the larger the rebound.
Consequence: A heavy-volume hourly plunge is a reason to buy for about four hours rather than sell into it, since in its most extreme cases the rebound is several times the cost of a trade.
Why:
- F4: The opposite side carries a graded effect: after down hours, the 4-hour excess return rises with the hour's (fall in usual moves × volume ratio), from -0.7 bp (n 7605) in the bottom half to +16.9 bp (t 1.38, n 456) in the 95–98 % band and +66.2 bp (t 1.91, n 153) in the top 1 %; that last figure is about 0.4 of the 4-hour usual move (1.42 % for BTC, 1.82 % for ETH) and 6 times the cost of a trade.
- F5: The same rebound shows over 2 hours, at +15.5 bp (t 2.24, n 911) in the 95–98 % band and +26.6 bp (t 1.87, n 304) in the top 1 %; down hours with z<-3 and volume ratio>3 give +20.1 bp at 2 hours (t 1.81, n 432) and +47.0 bp at 4 hours (t 1.88, n 230).
- F6: The rebound after the top 5 % of heavy-volume down hours holds on both coins, BTC at +22.5 bp (t 1.62, n 373) and ETH at +26.8 bp (t 1.58, n 388), and is positive in 5 of 8 years (2021 +149.6 bp, t 2.75; 2023 +25.8 bp, t 2.20), but it is negative in 2025 (-22.7 bp, t -1.32), and its rank correlation with the surge's size among down hours with a volume ratio above 2 is only 0.057.
- F1: The tested effect is not in the data: on up hours, the 4-hour excess return barely changes across the hour's (rise in usual moves × volume ratio) quantiles, from -1.9 bp (t -1.23, n 7694) in the bottom half to +10.6 bp (t 0.44, n 154) in the top 1 %, and up hours with z>3 and volume ratio>3 give -3.5 bp at 4 hours (t -0.18, n 203), so the move per case (total +0.01 %) is 0.1 times the 0.11 % cost of a trade.
