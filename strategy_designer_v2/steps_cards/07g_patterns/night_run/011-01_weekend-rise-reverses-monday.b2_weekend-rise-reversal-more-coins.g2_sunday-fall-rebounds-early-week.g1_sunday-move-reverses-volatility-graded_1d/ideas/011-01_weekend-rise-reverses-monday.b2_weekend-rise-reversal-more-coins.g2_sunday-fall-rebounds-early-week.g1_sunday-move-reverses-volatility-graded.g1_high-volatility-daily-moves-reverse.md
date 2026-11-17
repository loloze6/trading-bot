---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.g2_sunday-fall-rebounds-early-week.g1_sunday-move-reverses-volatility-graded
line: 7.g patterns
backtest: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.g2_sunday-fall-rebounds-early-week.g1_sunday-move-reverses-volatility-graded_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: A coin's 1-day return, measured in units of its own 20-day daily volatility, is followed by a move the opposite way over the next 1 to 3 days on any weekday. The reversal is larger the larger the move and the higher the coin's 20-day volatility relative to its own 90-day volatility.
Consequence: A trader can fade large vol-scaled daily moves every day of the week when the coin is in an unusually volatile period, sizing with how volatile that period is, rather than waiting for Sunday.
Why:
- F1: Daily moves reverse only when the coin's own 20-day volatility is high, and the effect is graded. In the top volatility tercile, the excess next-day return taken against the sign of the day's vol-scaled move averages +0.46% (t 6.43, n 10814), and the slope of next-day excess return on the move is −0.0058 (t −7.8). In the bottom tercile the same fade averages −0.10% (t −2.65). The high-volatility reversal also holds on non-overlapping grids: +0.49% over 2 days (t 3.21, n 5333) and +0.75% over 3 days (t 3.53, n 3592).
- F2: Volatility measured against the coin's own past sorts the reversal the same way. When the 20-day/90-day volatility ratio is in its top tercile, the next-day fade averages +0.29% (t 4.73, n 8259). In the bottom tercile it averages −0.03% (t −0.51).
- F3: The high-volatility reversal is not specific to Sunday. Within the top volatility tercile, the fade is positive on all seven weekdays (t 1.13 to 4.03; mean +0.15% to +0.75%). Sunday versus the other days gives a Welch t of only 1.65. Weekend bars as a whole fade more than weekday bars (Welch t 4.48).
- F6: The high-volatility reversal has weakened over time. Its yearly t is 4.75 in 2018, 3.50 in 2020, 3.60 in 2022, 1.23 in 2023, 1.03 in 2024 and 0.39 in 2025. The Sunday-only fade is also −0.06% (t −0.29) in 2025.
- F7: The book earns only on its Monday hold, at +0.090% mean daily return. Its Sharpe of 0.41 is 0.20 below holding the coins, and its mean daily return of 0.0137% fails the 0.05% bar. The Sunday-only regime leaves the stronger high-volatility reversal on the other six days unused.
