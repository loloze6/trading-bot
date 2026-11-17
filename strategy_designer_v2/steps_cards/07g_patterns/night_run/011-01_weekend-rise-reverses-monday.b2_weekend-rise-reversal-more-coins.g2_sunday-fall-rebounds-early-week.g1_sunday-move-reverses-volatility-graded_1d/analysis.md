---
line: 7.g patterns
backtest: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.g2_sunday-fall-rebounds-early-week.g1_sunday-move-reverses-volatility-graded_1d
idea tested: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.g2_sunday-fall-rebounds-early-week.g1_sunday-move-reverses-volatility-graded
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4625 USD
---
## Findings
- **F1:** Daily moves reverse only when the coin's own 20-day volatility is high, and the effect is graded. In the top volatility tercile, the excess next-day return taken against the sign of the day's vol-scaled move averages +0.46% (t 6.43, n 10814), and the slope of next-day excess return on the move is −0.0058 (t −7.8). In the bottom tercile the same fade averages −0.10% (t −2.65). The high-volatility reversal also holds on non-overlapping grids: +0.49% over 2 days (t 3.21, n 5333) and +0.75% over 3 days (t 3.53, n 3592).
- **F2:** Volatility measured against the coin's own past sorts the reversal the same way. When the 20-day/90-day volatility ratio is in its top tercile, the next-day fade averages +0.29% (t 4.73, n 8259). In the bottom tercile it averages −0.03% (t −0.51).
- **F3:** The high-volatility reversal is not specific to Sunday. Within the top volatility tercile, the fade is positive on all seven weekdays (t 1.13 to 4.03; mean +0.15% to +0.75%). Sunday versus the other days gives a Welch t of only 1.65. Weekend bars as a whole fade more than weekday bars (Welch t 4.48).
- **F4:** The high-volatility reversal is lopsided toward falls. On non-Sunday high-volatility bars, the bottom quintile of vol-scaled moves (mean z −1.24) is followed by a +1.18% excess next-day return. The top quintile (mean z +1.46) is followed by only −0.27%. On Sundays, the top quintile is followed by −0.45% and the bottom by +0.61%.
- **F5:** In calm periods moves continue rather than reverse. In the lowest volatility tercile, the next-day fade has t −3.40, −3.95 and −3.71 on Wednesday, Thursday and Friday bars. The overall slope of next-day return on the move in that tercile is +0.0013 (t 3.6).
- **F6:** The high-volatility reversal has weakened over time. Its yearly t is 4.75 in 2018, 3.50 in 2020, 3.60 in 2022, 1.23 in 2023, 1.03 in 2024 and 0.39 in 2025. The Sunday-only fade is also −0.06% (t −0.29) in 2025.
- **F7:** The book earns only on its Monday hold, at +0.090% mean daily return. Its Sharpe of 0.41 is 0.20 below holding the coins, and its mean daily return of 0.0137% fails the 0.05% bar. The Sunday-only regime leaves the stronger high-volatility reversal on the other six days unused.
- **F8:** In the Sunday bars, the fade grows with that day's volume relative to its 20-day mean. It is +0.26% (t 2.04) in the low-volume tercile and +0.68% (t 4.01) in the high-volume tercile, with a Welch t of 1.95. This is the opposite of the brief's claim that thin volume drives the reversal.

## Ideas
- `011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.g2_sunday-fall-rebounds-early-week.g1_sunday-move-reverses-volatility-graded.g1_high-volatility-daily-moves-reverse` (from F1, F2, F3, F6, F7): A coin's 1-day return, measured in units of its own 20-day daily volatility, is followed by a move the opposite way over the next 1 to 3 days on any weekday. The reversal is larger the larger the move and the higher the coin's 20-day volatility relative to its own 90-day volatility.
- `011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.g2_sunday-fall-rebounds-early-week.g1_sunday-move-reverses-volatility-graded.g2_volatile-period-falls-rebound` (from F1, F4): When a coin's 20-day volatility is high, a fall measured in units of that volatility is followed by a rebound over the next day. The rebound is larger the deeper the fall.
- `011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.g2_sunday-fall-rebounds-early-week.g1_sunday-move-reverses-volatility-graded.g3_calm-period-moves-continue` (from F1, F5): When a coin's 20-day volatility is low, its 1-day return in units of that volatility is followed by a move the same way over the next day. The continuation is larger the larger the move.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
