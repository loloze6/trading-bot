---
line: 7.g patterns
backtest: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d3_large-weekend-fall-rebound.b1_turbulent-weekend-fall-rebound_1d
idea tested: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d3_large-weekend-fall-rebound.b1_turbulent-weekend-fall-rebound
step 5: confirmed
step 6: profitable enough
mode: one call
explorations: 3
cost: 0.8410 USD
---
## Findings
- **F1:** On days other than Sunday, a coin's 3-day unusual move after a fall rises with the fall's depth (its daily return over its 20-day usual move) multiplied by its 20-day usual move against its 60-day mean. The slope is positive in 17 of 17 coins (per-coin t up to 3.2: DOGE 3.21, XMR 3.19, LTC 3.05), and the slope on date means is 0.0079 with t 2.26 over 1,234 dates; the tested Sunday-only idea does not account for this.
- **F2:** The same weekday falls (of at least 1.5 usual daily moves, Sundays excluded, t counted over dates) split by turbulence: those in the calmest third continue down by -1.15 % over 3 days (t -1.99, 368 cases on 163 dates), and those in the most turbulent third rebound by +1.09 % (t 1.79, 368 cases on 143 dates). The rebound is graded by turbulence and spread over Monday, Wednesday and Thursday (+1.46 %, +2.29 %, +1.51 %), not concentrated after the weekend.
- **F3:** On Sundays, a coin's own Sunday move predicts its next 3 days with a negative slope in 15 of 17 coins (pooled slope -0.0077, t -5.42 over 3,753 cases; on date means -0.0126, t -2.61 over 351 dates). After Sunday rises of at least 1 usual move, the mean unusual move is negative in 14 of 17 coins, so the reversal also holds on the rising side that the long-only book never trades.
- **F4:** Inside Sunday rises, the reversal is deepest when the Sunday bar's volume is low against its 20-day mean: -1.66 % over 3 days in the lowest volume third (t -1.70, 144 cases on 79 dates), -0.86 % in the middle third and +0.01 % in the highest. This is graded the way the brief predicts, but it does not clear chance alone.
- **F5:** The book's gain sits in a few days and years. Its mean daily return is +0.094 % on Mondays and +0.087 % on Wednesdays, against -0.009 % on Tuesdays. Its trades earned +13.9 % per trade in 2021 against -3.3 % in 2018, and the top forecast quartile earned +3.79 % per trade against +2.30 % for the lowest.
- **F6:** Within the same date, how a coin's Sunday move compares with other coins' Sunday moves predicts nothing (slope 0.0007, t 0.46). The Sunday reversal of F3 therefore comes from the move the coins share that day, not from the coin's own part of it.

## Ideas
- `011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d3_large-weekend-fall-rebound.b1_turbulent-weekend-fall-rebound.g1_turbulent-daily-fall-rebound` (from F1, F2): A coin that fell on any day by a large multiple of its usual daily move rises over the next 3 days, more the deeper the fall and the higher its 20-day usual move stands against its 60-day usual move. In calm stretches, the same fall is followed by further decline.
- `011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d3_large-weekend-fall-rebound.b1_turbulent-weekend-fall-rebound.g2_thin-sunday-rally-reverses` (from F3, F4, F6): A coin that rose on Sunday (its Sunday close-to-close return) by a large multiple of its usual daily move falls over the next 3 days. The fall is larger the larger the Sunday rise and the lower Sunday's volume stands against its 20-day mean.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
