---
brief: 018_daily-condition-caught-on-the-hour
source-idea: 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound
line: 7.b inconclusive
backtest: 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's 24-hour return, read at an hourly close, falls by a large multiple of its 30-day average absolute daily return while its 30-day return is negative, the price falls further over the next 4 days by more than the coin's usual 4-day drift, and the deeper the 30-day fall, the larger the further decline.
Consequence: A sharp hourly plunge in a coin that has fallen over the past month is a reason not to buy the dip, and a reason to short it for four days.
Why:
- F2: The effect depends on the coin's 30-day trend. Drops while the 30-day return is positive rebound by +0.41 % over 48 hours (t 2.68, 1946 cases), +0.67 % over 96 hours (t 3.07, 1910 cases) and +1.03 % over 168 hours (t 3.11, 1831 cases). The same drops while the 30-day return is negative keep falling: -0.27 % over 48 hours (t -1.91, 1981 cases) and -0.51 % over 96 hours (t -2.46, 1944 cases).
- F3: Mixing the two trends is what holds the overall t near 2, and the split is graded rather than a switch. Over 48 hours the excess return rises across the 30-day-return octiles from about -0.4 % to -0.6 % in octiles 2 and 3 (t -1.34, -2.20) to +0.48 %, +0.68 % and +0.69 % in octiles 6 to 8 (t 1.86, 2.19, 1.81). The Spearman of the 30-day return with the 48-hour excess is 0.038, larger than the forecast's own 0.027.
