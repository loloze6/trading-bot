---
line: 7.g patterns
backtest: 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.g1_high-volatility-fall-reversal_1d
idea tested: 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.g1_high-volatility-fall-reversal
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.5512 USD
---
## Findings
- **F1:** The tested idea's own gain sits mostly in its deepest falls: on bars with forecast > 0, the top forecast quartile earns a mean next-day excess return of 0.0092 (t 4.08, n 809) against 0.0019 to 0.0033 (t 0.98 to 1.79) in the other three quartiles, and down days in the highest third of volatility relative to its recent level earn 0.0056 (t 4.52, n 1886).
- **F2:** A day's move continues into the next day only when that day is a Monday: the slope of next-day excess return on the day's return in 20-day standard deviations is +0.0023 (t 2.76, n 2052) for Monday bars, positive in all 6 coins (t 0.88 to 2.04), but negative on every other day (Tue to Thu −0.0022 to −0.0025, t −2.3 to −2.8; Saturday −0.0043, t −4.19; Sunday −0.0044, t −3.45). The Monday sign is not steady across years (+0.015, t 5.6 in 2018 and +0.009, t 3.3 in 2021, but −0.003 to +0.0004 from 2022 to 2025).
- **F3:** Weekend moves reverse more than midweek moves: the weekend slope is negative in all 6 coins (−0.0011 to −0.0078, t −0.59 to −3.37) and in 7 of 8 years, and weekend minus Tue to Thu slope is −0.0022 (t −2.04, n 8398). The weekend reversal is strongest after high-volume weekend days (slope −0.0050, t −4.17), not low-volume ones (−0.0051, t −1.92), which is the opposite of the brief's volume claim.
- **F4:** In the high-volatility third, up days are followed by underperformance: mean next-day excess return −0.0039 (t −3.39, n 2036), negative in 5 of 6 coins. It is not graded by the size of the rise (slope t 0.56, rho −0.009), it is concentrated in 2018 (−0.019, t −4.78) and 2019 (−0.0099, t −3.57), and it fades to about zero from 2020 on.
- **F5:** Volume on a down day adds nothing once the fall's size is known: the top volume quintile of down days earns 0.0051 (t 2.99) against about 0.0008 elsewhere, but in a regression with the fall in standard deviations the log-volume coefficient has t 1.05.
- **F6:** The book earns mostly from signals taken on Tuesday and Thursday bars, which pay out on Wednesday and Friday: book daily return on Wednesday is 0.00118 (t 3.82) and on Friday 0.00094 (t 3.76), against −0.00002 to 0.00034 (t 0.13 to 1.36) on the other days.

## Ideas
- `011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.g1_high-volatility-fall-reversal.g1_sunday-move-reverses-monday` (from F2, F3): In a coin, Sunday's daily return, measured in its 20-day daily standard deviations, is reversed over the next 1 day: the larger Sunday's move, the larger Monday's move against it, and the reversal is larger on Sundays with higher volume.
- `011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.g1_high-volatility-fall-reversal.g2_monday-move-continues-tuesday` (from F2): In a coin, Monday's daily return, measured in its 20-day daily standard deviations, continues over the next 1 day: the larger Monday's move, the larger Tuesday's move in the same direction.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
