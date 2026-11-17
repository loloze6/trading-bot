---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.g1_high-volatility-fall-reversal
line: 7.g patterns
backtest: 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.g1_high-volatility-fall-reversal_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin, Monday's daily return, measured in its 20-day daily standard deviations, continues over the next 1 day: the larger Monday's move, the larger Tuesday's move in the same direction.
Consequence: Do not fade a large Monday move into Tuesday; lean with it, harder the larger the move.
Why:
- F2: A day's move continues into the next day only when that day is a Monday: the slope of next-day excess return on the day's return in 20-day standard deviations is +0.0023 (t 2.76, n 2052) for Monday bars, positive in all 6 coins (t 0.88 to 2.04), but negative on every other day (Tue to Thu −0.0022 to −0.0025, t −2.3 to −2.8; Saturday −0.0043, t −4.19; Sunday −0.0044, t −3.45). The Monday sign is not steady across years (+0.015, t 5.6 in 2018 and +0.009, t 3.3 in 2021, but −0.003 to +0.0004 from 2022 to 2025).
