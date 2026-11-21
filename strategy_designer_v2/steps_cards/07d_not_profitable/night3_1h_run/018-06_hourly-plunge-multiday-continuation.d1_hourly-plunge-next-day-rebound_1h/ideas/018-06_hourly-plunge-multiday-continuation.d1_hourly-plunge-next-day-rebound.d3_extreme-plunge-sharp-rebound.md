---
brief: 018_daily-condition-caught-on-the-hour
source-idea: 018-06_hourly-plunge-multiday-continuation.d1_hourly-plunge-next-day-rebound
line: 7.d not profitable
backtest: 018-06_hourly-plunge-multiday-continuation.d1_hourly-plunge-next-day-rebound_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin falls in 24 hours by many times its 30-day average absolute daily return, and the fall comes while its 3-day hourly volatility is high against its 30-day hourly volatility, the price rises over the next 1 day. The larger the fall in those multiples, the larger the rise.
Consequence: A trader can treat an extreme plunge in an agitated market as a rare, large rebound trade worth many times the cost of a trade, and stay out the rest of the time.
Why:
- F1: The rebound sits almost entirely in the largest drops. After a drop of 3 or more multiples of the 30-day average absolute daily return, the next 24 hours end 0.38 of a usual 1-day move above the drift (+2.0 % raw, 376 cases). After drops of 1 to 3 multiples they end only 0.07 to 0.08 above (+0.46 % to +0.62 % raw, 2696 cases). The book traded all of them, so the idea's average unusual move is +0.11 % per case, 0.6 times the 0.19 % cost of a trade.
- F2: The rebound holds only when hourly volatility is already raised. Here that means the coin's 3-day hourly volatility is high against its 30-day volatility.
- F6: The rebound is done within a day. Hot drops of 3 or more multiples are +2.65 % above drift at 24 hours and +2.76 % at 72 hours, so a longer holding adds almost nothing.
