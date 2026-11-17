---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.g1_high-volatility-fall-reversal.g1_sunday-move-reverses-monday
line: 7.g patterns
backtest: 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.g1_high-volatility-fall-reversal.g1_sunday-move-reverses-monday_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin, a daily fall measured in its 20-day daily standard deviations is followed by a rebound over the next 1 day: the larger the scaled fall, the larger the next day's rise.
Consequence: After a large scaled daily fall, lean long for the next day, larger the deeper the fall.
Why:
- F6: The reversal comes from falls, not rises. On down days the next-day slope is −0.00314 (t −3.61, n 7151); on up days it is +0.00088 (t 1.12, n 7349). The lowest quintile of scaled moves is followed by +0.40% excess the next day (t 4.13, n 2894).
- F1: Across all six coins, a day's return scaled by its 20-day standard deviation is reversed the next day much more after weekend days than after weekdays: slope −0.00446 (t −5.03, n 4138) for weekend signal days against −0.00100 (t −2.29, n 10362) for weekday signal days.
