---
line: 7.g patterns
backtest: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.g2_sunday-fall-rebounds-early-week_1d
idea tested: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.g2_sunday-fall-rebounds-early-week
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4505 USD
---
## Findings
- **F1:** Across all coins, Sunday's return scaled by its 20-day volatility predicts the next 2 days' excess return with a negative slope of -0.0062 (t -4.80, n 4600, one case per week so none overlap). This is the strongest of the seven weekdays: Monday's moves give t -1.55 and Thursday's give +0.86. The same Sunday-scaled return still gives t -2.00 over 5 days.
- **F2:** The Sunday reversal grows with the coin's volatility level. The slope is -0.0015 (t -0.84, n 1535) in the lowest third of the coin's own volatility, -0.0062 (t -2.98, n 1542) in the middle third and -0.0115 (t -4.10, n 1502) in the highest third.
- **F3:** The Sunday reversal is stronger when Sunday volume is low against its 20-day mean. The slope is -0.0106 (t -3.14) in the lowest volume tercile and -0.0095 (t -3.54) in the middle one, against -0.0042 (t -2.43) in the highest, with about 1526 cases each.
- **F4:** The Sunday slope is negative in 7 of 8 years, with 2022 the exception at +0.0047 (t 1.48). It is significant in 2020 (t -3.17), 2024 (t -2.76) and 2025 (t -3.87). It is negative in 17 of 19 coins, most strongly LINK (t -3.00), SUI (-2.45), NEAR (-2.16) and XMR (-2.03).
- **F5:** The reversal comes from the sign of Sunday's move, not its size within one side. The slope is only +0.0024 (t 0.91, n 2268) among Sunday rises and +0.0009 (t 0.31, n 2302) among Sunday falls. This fits the tested falls-only idea being inconclusive (t 1.12) and the book earning 8.968e-05 a day, Sharpe 0.36.
- **F6:** Across all weekdays (non-overlapping 2-day grid), the 1-day scaled move reverses over 2 days in the coin's highest volatility tercile (slope -0.0058, t -3.61, n 5319). It continues in the lowest tercile (slope +0.0026, t 3.36, n 5321). The high-volatility reversal is negative in 7 of 8 years, with t -2.2 to -3.2 in 2018, 2019, 2020 and 2025.
- **F7:** The weekend's combined Saturday+Sunday 2-day move does not reverse over the next 2 days (slope -0.0007, t -0.52, n 4579). The reversal is tied to Sunday's own day, not the whole weekend.

## Ideas
- `011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.g2_sunday-fall-rebounds-early-week.g1_sunday-move-reverses-volatility-graded` (from F1, F2, F4, F5): A coin's Sunday return, measured in units of its own 20-day daily volatility, is followed by a move the opposite way over the next 2 days. The reversal is larger the larger the Sunday move, and larger still when the coin's recent volatility is high.
- `011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.g2_sunday-fall-rebounds-early-week.g2_thin-volume-sunday-moves-fade` (from F1, F3): The 2-day reversal after a coin's Sunday move, scaled by its 20-day volatility, is larger the lower Sunday's volume is relative to the coin's 20-day average volume.
- `011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.g2_sunday-fall-rebounds-early-week.g3_high-volatility-daily-moves-reverse` (from F6): When a coin's 20-day volatility is high relative to its own history, its 1-day return, scaled by that volatility, is followed by an opposite move over the next 2 days, and the larger the move, the larger the reversal.
- `011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.g2_sunday-fall-rebounds-early-week.g4_calm-period-daily-moves-continue` (from F6): When a coin's 20-day volatility is low relative to its own history, its 1-day return, scaled by that volatility, is followed by a move in the same direction over the next 2 days, and the larger the move, the larger the follow-through.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
