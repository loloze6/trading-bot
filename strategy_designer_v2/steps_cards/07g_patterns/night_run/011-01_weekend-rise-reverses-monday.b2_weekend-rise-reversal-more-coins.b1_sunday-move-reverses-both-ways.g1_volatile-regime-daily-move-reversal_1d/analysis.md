---
line: 7.g patterns
backtest: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways.g1_volatile-regime-daily-move-reversal_1d
idea tested: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways.g1_volatile-regime-daily-move-reversal
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4271 USD
---
## Findings
- **F1:** The fade's next-day gain beyond the coin's mean daily return depends mostly on the day of the move: after Sunday moves it is 0.00424 (t 4.89, n 4304), after Saturday moves 0.00177 (t 2.60, n 4303), and after Tuesday moves 0.00307 (t 3.65, n 4314), while Wednesday, Thursday and Monday sit near zero (|t| ≤ 0.33).
- **F2:** Friday moves continue rather than reverse: the fade gain after a Friday move is −0.00189 (t −2.95, n 4301), the only weekday with a significantly negative value.
- **F3:** The reversal sits only where 20-day volatility is high against its 120-day level: in the top tercile of vol20/vol120 the fade gain is 0.00296 (t 4.04, n 6056), against −0.00023 (t −0.36) and 0.00026 (t 0.41) in the lower two terciles.
- **F4:** Moves made on heavy volume reverse more, which is the opposite of the brief's thin-book claim: in the top tercile of the day's volume over its 30-day median the fade gain is 0.00170 (t 2.66, n 9145), against 0.00005 (t 0.11) in the bottom tercile.
- **F5:** The edge is real before costs but smaller than the cost of trading it: mean timing gain is 0.000452 per bar against a mean fee of 0.000647 per bar, so the book's mean daily return is −2.7e-05 (Sharpe −0.03).
- **F6:** The reversal has faded in recent years: the fade gain is positive with t above 2 in 2018, 2020, 2021 and 2023 (0.0045, 0.0040, 0.0036, 0.0018), but negative in 2024 (−0.00126, t −1.79) and 2025 (−0.00094, t −1.42), and the book's daily mean is lowest in 2024 (−0.00177, t −1.89).
- **F7:** The fade works better in falling markets: when the coin's 20-day return is negative, the fade gain is 0.00160 (t 3.35, n 15538), against 0.00048 (t 1.11, n 14584) when it is positive.

## Ideas
- `011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways.g1_volatile-regime-daily-move-reversal.g1_weekend-move-fades-monday` (from F1, F5): A coin's move over the weekend (Saturday and Sunday, UTC) is followed by a move the other way over the next day, and the larger the weekend move, the larger the move back.
- `011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways.g1_volatile-regime-daily-move-reversal.g2_friday-move-continues-saturday` (from F2): A coin's Friday move continues in the same direction over the next day, and the larger the Friday move, the larger the continuation.
- `011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways.g1_volatile-regime-daily-move-reversal.g3_vol-spike-daily-move-reversal` (from F3, F5): A coin's daily move is followed by a move the other way over the next day, and the higher its 20-day volatility relative to its 120-day volatility, the larger the move back.
- `011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways.g1_volatile-regime-daily-move-reversal.g4_high-volume-move-reverses` (from F4): A coin's daily move is followed by a move the other way over the next day, and the higher that day's volume relative to its 30-day median, the larger the move back.
- `011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways.g1_volatile-regime-daily-move-reversal.g5_downtrend-daily-move-reversal` (from F7): A coin's daily move is followed by a move the other way over the next day, and the more the coin has fallen over the past 20 days, the larger the move back.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
