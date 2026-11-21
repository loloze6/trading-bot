---
brief: 018_daily-condition-caught-on-the-hour
source-idea: 018-06_hourly-plunge-multiday-continuation.d1_hourly-plunge-next-day-rebound.c1_deep-plunge-next-day-rebound
line: 7.g patterns
backtest: 018-06_hourly-plunge-multiday-continuation.d1_hourly-plunge-next-day-rebound.c1_deep-plunge-next-day-rebound_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's 24-hour return, read at an hourly close, is a drop several times its 30-day average absolute daily return while that 30-day average itself is high relative to the coin's own past year, the price rises over the next 1 day by more than its normal 1-day drift. The deeper the drop in multiples and the higher the 30-day average stands against the past year, the larger the rise.
Consequence: A trader should buy a deep hourly plunge for a day mainly when the coin is already in a volatile spell, because the rebound there is many times the cost of a trade, and treat the same plunge in a calm spell as no reason to trade.
Why:
- F1: The deeper the hourly plunge, the larger the next-day rebound, but only when the coin is already volatile against its own history. For a drop beyond 3 multiples of its 30-day mean absolute daily move, the next 24 hours, net of drift, are +956 bps (t 5.7, 55 independent cases, strength 1.95) when that 30-day level is over 1.4 times the coin's median, +173 bps (t 2.3, 85) between 1.0 and 1.4 times, and +13 bps (t 0.4, 236) below its median; drops of 2 to 3 multiples follow the same order (+215, +21, −3 bps).
- F2: Ranking drops of more than 1 multiple by depth times relative volatility, which is close to the drop in percent over the coin's long-run usual daily move, only the top fifth stands out. It gives +196 bps over 24 hours (t 5.6, 615 cases, strength 0.39), about 10 times the 19 bps cost of a round trip. The other four fifths give −9 to +34 bps (t ≤ 1.6).
- F3: The volatile-plunge rebound holds on every coin but not in every year. Drops of more than 1 multiple at relative volatility above 1.4 rebound +96 to +259 bps over 24 hours on all 6 coins (t 2.3 to 2.5 on five, 1.1 on XMR). By year they are positive in 2018 to 2021 and 2025 (+122 to +292 bps) and flat or negative in 2022 to 2024 (−32 to +2 bps).
- F4: The tested idea's weak overall size (0.020 strength, t 1.92) comes from mixing a strong tail with a dead middle. Drops beyond 3 multiples rebound +187 bps (t 4.6, 376 cases), while drops of 2 to 3 multiples give +39 bps (t 1.7). Measured by year, the beyond-3 group is −85 bps in 2022 and about 0 in 2023 and 2024, the calm years.
- F6: The book's worst days are the coin's crash days, and the coin rises the day after. In the book's worst decile of days, the book returns −393 bps while the coin falls −663 bps, and the coin then gains +79 bps the next day. This matches the idea buying into falls that are still under way.
