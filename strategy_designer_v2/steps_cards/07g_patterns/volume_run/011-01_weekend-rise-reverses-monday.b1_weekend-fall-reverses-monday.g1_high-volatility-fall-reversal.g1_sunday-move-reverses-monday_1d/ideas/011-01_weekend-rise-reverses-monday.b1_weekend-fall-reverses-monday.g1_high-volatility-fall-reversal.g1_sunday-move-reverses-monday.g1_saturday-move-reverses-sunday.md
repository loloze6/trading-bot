---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.g1_high-volatility-fall-reversal.g1_sunday-move-reverses-monday
line: 7.g patterns
backtest: 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.g1_high-volatility-fall-reversal.g1_sunday-move-reverses-monday_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin, Saturday's daily return measured in its 20-day daily standard deviations is reversed over the next 1 day: the larger Saturday's move, the larger Sunday's move against it.
Consequence: After a large Saturday move, lean against it into Sunday, harder the larger the move.
Why:
- F1: Across all six coins, a day's return scaled by its 20-day standard deviation is reversed the next day much more after weekend days than after weekdays: slope −0.00446 (t −5.03, n 4138) for weekend signal days against −0.00100 (t −2.29, n 10362) for weekday signal days.
- F2: Saturday reverses as strongly as Sunday, although the tested idea trades only Sunday. The next-day slope on the scaled move is −0.00459 (t −4.13, n 2069) after Saturday and −0.00438 (t −3.23, n 2069) after Sunday. Among weekdays, only Tuesday reaches that size, at −0.00344 (t −3.20).
