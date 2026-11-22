---
brief: 028_volume-confirmed-hourly-moves-continue
source-idea: 028-02_volume-surge-down-continuation.b1_volume-surge-rise-continues-daylong.b2_large-hourly-rise-continues-daylong
line: 7.g patterns
backtest: 028-02_volume-surge-down-continuation.b1_volume-surge-rise-continues-daylong.b2_large-hourly-rise-continues-daylong_1h
instruments: BTC, ETH
bar: 1h
period: folds A, B, C, D
---
Idea: Each coin rises more than its usual hourly drift over the 20:00–22:00 UTC hours. The further the coin fell over the past 24 hours, the larger that rise.
Consequence: A trader would lean long into the 20–22 UTC hours, more after a falling day, and avoid opening shorts just before them. Each hour adds only about 0.04–0.09 %, so this works as a timing tilt on existing trades, not as a stand-alone trade against a 0.11 % round-trip cost.
Why:
- F1: Hourly returns between 20:00 and 22:00 UTC beat the coin's mean hourly return in both coins. Hour 20 averages +0.045 % (t 4.00) and hour 21 +0.040 % (t 3.69), about 5,840 hours each. These are the only two of 24 hours with a t above 3, so they stand out even after testing every hour. Pooled over both hours, BTC averages +0.037 % (t 3.81, 5,837 hours) and ETH +0.048 % (t 3.92, 5,837 hours).
- F2: The 20–22 UTC excess return holds outside any one period. It is positive in 7 of 8 years: from +0.028 % to +0.077 %, with t 1.2 to 3.7. The exception is 2022, at −0.031 % (t −1.45). It is positive on all 7 weekdays: from +0.034 % to +0.053 %, with t 1.5 to 2.8.
- F3: The 20–22 UTC excess return is largest after the coin fell over the prior 24 hours. By quartile of the prior 24-hour return it is +0.093 % (t 4.41) in the lowest quartile, +0.035 % (t 3.01) in the second, +0.003 % (t 0.22) in the third and +0.042 % (t 2.46) in the highest. The grading is clear across the lower three quartiles and breaks in the top one.
