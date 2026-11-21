---
brief: 018_daily-condition-caught-on-the-hour
source-idea: 018-04_hourly-surge-multiday-continuation.b1_hourly-surge-within-weekly-rise
line: 7.d not profitable
backtest: 018-04_hourly-surge-multiday-continuation.b1_hourly-surge-within-weekly-rise_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The larger a coin's 30-day return, read at an hourly close, the more its price rises over the next 5 days compared with its usual 5-day return.
Consequence: A trader holds a coin long in proportion to its past month's rise and stays out after a falling month, which avoids the long shared declines that set this book's deepest fall.
Why:
- F2: The idea is too small to pay on its own. Its unusual move is +0.12 % per case over 5 days, a strength of 0.007, which is 0.6 times the 0.19 % round-trip cost. The total move (+0.76 %) is 3.9 times the cost, so almost all of the book's gain is the coin's normal drift.
- F3: The book earns almost nothing while a coin's 30-day return is negative. Long bars in that state earn 0.145 bps per hour (t 0.9, 116,284 bars), against 1.121 bps (t 5.0, 147,459 bars) when the 30-day return is positive. On the coin itself, the next hour returns 0.37 bps after a falling 30 days and 1.04 bps after a rising one.
- F4: The gain grows with the 30-day return:
- F8: The book also gains when the coin's 3-day return is strongest. Bars with a 3-day return above 5.2 % earn 1.45 bps per hour, with +0.96 bps of timing. Bars with a 3-day return between −4.8 % and +1.4 % have −0.49 and −0.40 bps of timing.
