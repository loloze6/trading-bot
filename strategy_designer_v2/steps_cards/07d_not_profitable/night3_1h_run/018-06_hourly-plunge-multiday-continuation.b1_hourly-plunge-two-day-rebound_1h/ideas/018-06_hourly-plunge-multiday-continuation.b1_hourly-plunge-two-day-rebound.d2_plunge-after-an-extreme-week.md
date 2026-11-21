---
brief: 018_daily-condition-caught-on-the-hour
source-idea: 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound
line: 7.d not profitable
backtest: 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's 24-hour return, read at an hourly close, falls by a large multiple of its 30-day average absolute daily return, the price rises over the next 2 days by more than the coin's usual 2-day drift. The larger the 24-hour drop in those multiples, and the larger the coin's 7-day return in either direction against its usual 7-day move, the larger the rise.
Consequence: A trader buys a plunge that comes after a week of large moves either way, and does not buy one that interrupts a quiet week.
Why:
- F7: The past week's move shows the same split. Plunges after the largest 7-day falls rebound +0.75 % (t 2.94), and after the largest 7-day rises +1.02 % (t 3.98). Plunges after middling weeks lose -0.39 % (t -2.15) and -0.28 % (t -1.71). The 30-day return shows the same U shape (+0.55 % and +0.61 % at the ends, -0.58 % at t -3.07 just below zero).
- F2: The rebound after a plunge depends on how violent the coin's last week has been against its last month. The measure is the 7-day to 30-day hourly-volatility ratio at the case bar; 6118 cases over 48 hours.
- F8: Taken unconditionally, the idea is about the size of one trade's cost.
