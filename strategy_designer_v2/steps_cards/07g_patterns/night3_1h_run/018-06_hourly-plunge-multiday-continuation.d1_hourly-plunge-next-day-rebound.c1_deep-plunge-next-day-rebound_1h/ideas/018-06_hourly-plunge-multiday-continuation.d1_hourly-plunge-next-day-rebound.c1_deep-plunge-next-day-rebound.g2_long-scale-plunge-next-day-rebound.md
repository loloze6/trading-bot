---
brief: 018_daily-condition-caught-on-the-hour
source-idea: 018-06_hourly-plunge-multiday-continuation.d1_hourly-plunge-next-day-rebound.c1_deep-plunge-next-day-rebound
line: 7.g patterns
backtest: 018-06_hourly-plunge-multiday-continuation.d1_hourly-plunge-next-day-rebound.c1_deep-plunge-next-day-rebound_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's 24-hour return, read at an hourly close, is a drop several times its average absolute daily return over the past year, the price rises over the next 1 day by more than its normal 1-day drift. The larger the drop in those multiples, the larger the rise.
Consequence: A trader should size a one-day rebound buy by how large the drop is against the coin's long-run daily move rather than its last month's, because only the drops that are large on that scale rebound by several times the cost of a trade.
Why:
- F2: Ranking drops of more than 1 multiple by depth times relative volatility, which is close to the drop in percent over the coin's long-run usual daily move, only the top fifth stands out. It gives +196 bps over 24 hours (t 5.6, 615 cases, strength 0.39), about 10 times the 19 bps cost of a round trip. The other four fifths give −9 to +34 bps (t ≤ 1.6).
- F3: The volatile-plunge rebound holds on every coin but not in every year. Drops of more than 1 multiple at relative volatility above 1.4 rebound +96 to +259 bps over 24 hours on all 6 coins (t 2.3 to 2.5 on five, 1.1 on XMR). By year they are positive in 2018 to 2021 and 2025 (+122 to +292 bps) and flat or negative in 2022 to 2024 (−32 to +2 bps).
- F4: The tested idea's weak overall size (0.020 strength, t 1.92) comes from mixing a strong tail with a dead middle. Drops beyond 3 multiples rebound +187 bps (t 4.6, 376 cases), while drops of 2 to 3 multiples give +39 bps (t 1.7). Measured by year, the beyond-3 group is −85 bps in 2022 and about 0 in 2023 and 2024, the calm years.
- F5: The rebound after a deep plunge is spread over the day rather than front-loaded. Of the +201 bps raw 24-hour move after drops beyond 3 multiples, +53 bps comes in the first 6 hours.
