---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.g1_high-volatility-fall-reversal.g1_sunday-move-reverses-monday
line: 7.g patterns
backtest: 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.g1_high-volatility-fall-reversal.g1_sunday-move-reverses-monday_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin, Sunday's daily return measured in its 20-day daily standard deviations is reversed over the next 3 days: the larger Sunday's move, the larger the move against it from Sunday's close to Wednesday's close.
Consequence: Hold a lean against a large Sunday move through the first days of the week, not only into Monday.
Why:
- F3: Sunday's scaled move keeps being reversed beyond Monday. Over the next 3 days the slope is −0.00746 (t −3.48, n 2021, one Sunday a week, so no overlap), against −0.00438 over the next 1 day.
- F1: Across all six coins, a day's return scaled by its 20-day standard deviation is reversed the next day much more after weekend days than after weekdays: slope −0.00446 (t −5.03, n 4138) for weekend signal days against −0.00100 (t −2.29, n 10362) for weekday signal days.
