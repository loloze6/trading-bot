---
brief: 018_daily-condition-caught-on-the-hour
source-idea: 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends.e2_monthly-rise-multiweek-continuation.e2_strong-week-keeps-rising
line: 7.d not profitable
backtest: 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends.e2_monthly-rise-multiweek-continuation.e2_strong-week-keeps-rising_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: A coin whose 7-day return is among its largest rises over the next 7 days by more than its usual 7-day drift, and the larger its 7-day return, the larger that rise, only while its 30-day return is positive.
Consequence: A strong week is a reason to stay long for the following week only when the month behind it is also up; a strong week inside a falling month is a reason to stay out.
Why:
- F1: The book fails on its falls: its deepest fall across the chained windows reaches 45 % to 52 % (w3 −45 %, w14 −52 %, w15 −49 %), and every coin on its own falls 63 % to 88 % (ZEC −88 %, LTC −76 %). Against a yearly return in the tens of percent, that gives a Calmar of 0.47.
- F2: The worst book days are days the coins crash while the book is fully long: the 15 worst book days lose 8.7 % to 15.7 % while the coins lose 7.7 % to 38.7 %. The book has no state in which it steps aside before a shared fall.
- F3: The book's gain lives where the coin's 30-day return is not negative. Long hours with a positive 30-day return earned 18.00 of the summed hourly gain over 236,105 hours (mean 0.000076 per hour). Long hours with a negative 30-day return earned 0.28 over 120,998 hours (0.000002 per hour), though they held a mean allocation of 0.67. So a third of the exposure carries risk and almost no return.
- F4: On non-overlapping 168-hour cells with a long forecast (950 cells), the unusual 7-day move depends on the 30-day return:
- F6: The idea is real only in its strong part, but the pooled measure drowns it.
- F7: A gross simulation that keeps only the long hours with a positive 30-day return cuts the deepest fall on 5 of 6 coins:
