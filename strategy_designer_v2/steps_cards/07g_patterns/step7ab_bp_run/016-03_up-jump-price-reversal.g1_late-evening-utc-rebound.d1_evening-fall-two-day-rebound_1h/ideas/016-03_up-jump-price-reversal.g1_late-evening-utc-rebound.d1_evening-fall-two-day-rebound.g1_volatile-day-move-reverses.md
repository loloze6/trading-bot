---
brief: 016_grind-versus-jump-moves
source-idea: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d1_evening-fall-two-day-rebound
line: 7.g patterns
backtest: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d1_evening-fall-two-day-rebound_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The more a coin has fallen over its last 24 hours, the more it rises over the next day, and the more it has risen, the more it falls; the reversal grows with the coin's hourly volatility over the past week.
Consequence: After a large 24-hour move in a volatile week, a trader leans against it for a day instead of following it, and refuses to chase it.
Why:
- F1: Across all hours, a coin's 24-hour return is followed by its opposite over the next day and the next two days, pooled over 6 coins. The slope of the next-24-hour excess return on the standardised 24-hour return has t -11.7 on 16238 non-overlapping cases (t -5.1 on the grid shifted by 12 hours). Over 48 hours the slope's t is -6.8 on 8003 cases (-2.3 on the shifted grid). The lowest fifth of 24-hour returns is followed by +47 bps of unusual move over 24 hours (t 4.4; total +59 bps) and +52 bps over 48 hours (t 2.8; total +75 bps). The highest fifth is followed by -32 bps over 24 hours (t -3.3).
- F2: This 24-hour reversal holds coin by coin and year by year. Over 48 hours the slope's t is negative on all 6 coins, from -0.7 (XRP) to -5.2 (XMR). It is negative in 7 of 8 years, at -2.5 or below in 2018, 2021, 2022 and 2023. The exception is 2024, at t +2.0.
- F3: The 24-hour reversal comes from the most volatile periods. Split by the coin's past-week hourly volatility, the 48-hour slope's t is -7.7 in the highest third (2669 cases), against +2.1 and +1.8 in the lowest and middle thirds.
- F6: The tested evening idea is too small to pay. Its slope's t is 1.70. Its unusual move is +0.10 % per case, 0.5 times the 0.19 % cost of a round trip. The book trails holding the coin on every coin: 2.8 to 5.9 bps a day against 6.7 to 15.5 for holding, and in 6 of 8 years.
