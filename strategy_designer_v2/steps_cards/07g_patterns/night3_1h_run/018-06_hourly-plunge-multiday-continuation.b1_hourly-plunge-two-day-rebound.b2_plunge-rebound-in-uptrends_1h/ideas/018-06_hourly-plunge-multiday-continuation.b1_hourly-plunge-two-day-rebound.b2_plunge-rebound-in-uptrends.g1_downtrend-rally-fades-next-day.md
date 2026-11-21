---
brief: 018_daily-condition-caught-on-the-hour
source-idea: 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends
line: 7.g patterns
backtest: 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's 24-hour return, read at an hourly close, rises by a large multiple of its 30-day average absolute daily return while its 30-day return is negative, its price falls over the next 24 hours below the coin's usual 24-hour drift, and the larger that multiple, the larger the fall.
Consequence: A sharp one-day rally in a coin that has fallen over the past month is a reason to sell it, or to refuse buying it, for the next day, more so the sharper the rally.
Why:
- F1: When a coin's 24-hour return is up by at least 1 times its 30-day mean absolute 24-hour return while its 30-day return is negative, the next 24 hours fall short of the coin's drift by 60.85 bps (t -4.19, 974 non-overlapping cases); the shortfall grows with the rise: -45 bps (t -2.64) for 1 to 2 times, -84 bps (t -2.66) for 2 to 3 times, -117 bps (t -2.20) beyond 3 times. Over all positive 24-hour returns in a falling month, Spearman rho is -0.069 (p 0.0002, n 2912). Per coin the mean is negative in 6 of 6 (t -0.77 to -2.93), and it is negative in 6 of 8 years. The move is about 3.2 times the 19 bps cost of a round trip.
- F2: The same rise in a rising month shows nothing over 24 hours: -10, +11 and +2 bps for 1 to 2, 2 to 3 and above 3 times (t within ±0.7; Spearman rho -0.032, p 0.051). The fade belongs to falling months only.
