---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.g1_high-volatility-fall-reversal
line: 7.g patterns
backtest: 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.g1_high-volatility-fall-reversal_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin, Sunday's daily return, measured in its 20-day daily standard deviations, is reversed over the next 1 day: the larger Sunday's move, the larger Monday's move against it, and the reversal is larger on Sundays with higher volume.
Consequence: After a large Sunday move, lean against it into Monday, harder the larger the move and the heavier the Sunday volume.
Why:
- F2: A day's move continues into the next day only when that day is a Monday: the slope of next-day excess return on the day's return in 20-day standard deviations is +0.0023 (t 2.76, n 2052) for Monday bars, positive in all 6 coins (t 0.88 to 2.04), but negative on every other day (Tue to Thu −0.0022 to −0.0025, t −2.3 to −2.8; Saturday −0.0043, t −4.19; Sunday −0.0044, t −3.45). The Monday sign is not steady across years (+0.015, t 5.6 in 2018 and +0.009, t 3.3 in 2021, but −0.003 to +0.0004 from 2022 to 2025).
- F3: Weekend moves reverse more than midweek moves: the weekend slope is negative in all 6 coins (−0.0011 to −0.0078, t −0.59 to −3.37) and in 7 of 8 years, and weekend minus Tue to Thu slope is −0.0022 (t −2.04, n 8398). The weekend reversal is strongest after high-volume weekend days (slope −0.0050, t −4.17), not low-volume ones (−0.0051, t −1.92), which is the opposite of the brief's volume claim.
