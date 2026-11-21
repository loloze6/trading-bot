---
brief: 018_daily-condition-caught-on-the-hour
source-idea: 018-06_hourly-plunge-multiday-continuation.d1_hourly-plunge-next-day-rebound.c1_deep-plunge-next-day-rebound
line: 7.b inconclusive
backtest: 018-06_hourly-plunge-multiday-continuation.d1_hourly-plunge-next-day-rebound.c1_deep-plunge-next-day-rebound_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin whose 30-day return is positive has a 24-hour return, read at an hourly close, that is a drop of several times its 30-day average absolute daily return, the price rises over the next 5 days by more than the coin's normal 5-day drift. The larger the coin's 30-day rise before the drop, the larger the rebound.
Consequence: A trader should treat a sharp one-day drop inside a rising coin as a reason to buy for several days, where the move is several times a trade's cost, and refuse to buy the same drop in a falling coin.
Why:
- F4: Most of the rebound comes from coins that were rising over the prior 30 days.
- F5: Inside the rising coins, the 5-day gain grows with the 30-day rise, not with the depth of the drop. By 30-day return tercile, the gain is -0.37 %, +1.56 % (t 3.09) and +1.58 % (t 2.45). The correlation of the 5-day gain with the 30-day return is 0.12, and with the forecast -0.02. The gain also swings by year: 2018 -5.35 %, 2021 +5.99 %, 2022 -1.47 %.
- F7: The book does not beat holding the coins: its Sharpe is 0.53, 0.02 below holding's, and its Calmar is 0.25. This fits a 24-hour unusual move smaller than a trade's cost (the earlier findings F11 and F2).
