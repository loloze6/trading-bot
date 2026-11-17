---
line: 7.d not profitable
backtest: 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.g1_high-volatility-fall-reversal.g1_sunday-move-reverses-monday_1d
idea tested: 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.g1_high-volatility-fall-reversal.g1_sunday-move-reverses-monday
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3786 USD
---
## Findings
- **F1:** The book holds a position only on the Sunday-to-Monday bar (share of non-zero positions on other days 0.000, mean |position| 0.41 on Sundays), so a real Sunday edge of 0.00129 per Sunday (t 2.51, n 2489) becomes a book mean daily return of only 0.0000562 against the 0.0005 required. Holding the coins returns 0.00118 a day with standard deviation 0.0407, a Sharpe of about 0.55 against the book's 0.16.
- **F2:** Fees cost 0.000898 per Sunday, about 70 % of the Sunday gain before fees of 0.00129, so the one-day-a-week round trip eats most of the edge.
- **F3:** The one-day reversal of a move measured in 20-day standard deviations is not specific to Sunday. The slope of the next day's excess return on minus the move is positive with t 3.47 for Wednesday's move, 5.27 for Saturday's, 3.53 for Sunday's, 2.50 for Thursday's and 2.36 for Tuesday's (n about 2270 each). Monday's move continues instead (slope -0.0022, t -2.44).
- **F4:** The Sunday reversal is lopsided:
- **F5:** The Sunday reversal fades as the coin's 60-day return rises:
- **F6:** The worst 5 % of Sundays came on large moves (mean |z| 1.26 against 0.63 for the rest) with large positions (mean |position| 0.84 against 0.39). These losses drive the 0.20 deepest fall that sets the Calmar at 0.061.
- **F7:** The Sunday reversal grows with the coin's 20-day volatility:

## Ideas
- `011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.g1_high-volatility-fall-reversal.g1_sunday-move-reverses-monday.d1_daily-vol-scaled-move-reverses` (from F1, F2, F3): In a coin, each day's daily return measured in its 20-day daily standard deviations is reversed over the next 1 day: the larger the day's move, the larger the following day's move against it, and the reversal is largest after Saturday and Sunday moves.
- `011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.g1_high-volatility-fall-reversal.g1_sunday-move-reverses-monday.d2_sunday-reversal-weakens-in-uptrend` (from F4, F5, F6): In a coin, Sunday's daily return, measured in its 20-day daily standard deviations, is reversed over the next 1 day: the larger Sunday's move, the larger Monday's move against it. The reversal is larger the lower the coin's 60-day return, so after a strong 60-day rise a large up Sunday is barely given back.
- `011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.g1_high-volatility-fall-reversal.g1_sunday-move-reverses-monday.d3_sunday-falls-reverse-more` (from F4, F6): In a coin, Sunday's daily return, measured in its 20-day daily standard deviations, is reversed over the next 1 day: the larger Sunday's move, the larger Monday's move against it. A Sunday fall is reversed more strongly than a Sunday rise of the same size.
- `011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.g1_high-volatility-fall-reversal.g1_sunday-move-reverses-monday.d4_sunday-reversal-grows-with-volatility` (from F7, F2): In a coin, Sunday's daily return, measured in its 20-day daily standard deviations, is reversed over the next 1 day: the larger Sunday's move, the larger Monday's move against it. The reversal is larger the higher the coin's 20-day daily volatility.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
