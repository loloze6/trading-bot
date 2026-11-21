---
brief: 018_daily-condition-caught-on-the-hour
source-idea: 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound
line: 7.d not profitable
backtest: 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's 24-hour return, read at an hourly close, falls by a large multiple of its 30-day average absolute daily return, the price rises over the next 2 days by more than the coin's usual 2-day drift. The larger the 24-hour drop in those multiples, and the higher the coin's hourly volatility over the past 7 days against its past 30 days, the larger the rise.
Consequence: A trader buys an hourly plunge only in proportion to how turbulent the coin's last week has been against its last month, and stays out of plunges in calm weeks, where the rebound is absent.
Why:
- F2: The rebound after a plunge depends on how violent the coin's last week has been against its last month. The measure is the 7-day to 30-day hourly-volatility ratio at the case bar; 6118 cases over 48 hours.
- F3: The book's gain sits almost entirely in high-ratio bars.
- F4: Outside w12 to w16 the volatility gradient is steep. Mean excess return rises from -0.17 % to -0.30 %, +0.07 %, +0.84 % (t 3.59) and +1.37 % (t 5.20, n 740) across the ratio fifths, and the Spearman of forecast against outcome rises from 0.01 to 0.10.
- F6: Among high-ratio cases (ratio above 1), the rebound grows with the drop: +0.01 %, +0.73 % (t 3.49), +0.42 % and +1.98 % (t 4.22, n 331) across the forecast bands. For the full-size forecast band over all cases it is +0.88 % (n 678).
- F8: Taken unconditionally, the idea is about the size of one trade's cost.
