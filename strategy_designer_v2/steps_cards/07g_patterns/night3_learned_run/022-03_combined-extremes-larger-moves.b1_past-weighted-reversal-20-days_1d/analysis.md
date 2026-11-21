---
line: 7.g patterns
backtest: 022-03_combined-extremes-larger-moves.b1_past-weighted-reversal-20-days_1d
idea tested: 022-03_combined-extremes-larger-moves.b1_past-weighted-reversal-20-days
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4138 USD
---
## Findings
- **F1:** The 20-day reversal that confirmed the idea depends on where the 20-day grid starts. On the official grid (offset 0), minus the 1-day move scaled by its 60-day volatility predicts the next 20 days with t 3.59 over 890 cases. Averaged over all 20 possible starting offsets, the t is -0.88, ranging from -5.33 to +3.59. The same holds at 5, 10 and 40 days, where the mean t over offsets is -0.89, -0.97 and -0.50. So there is no daily 1-day reversal that holds across grids.
- **F2:** The idea's move per case points the wrong way. The unusual move is -0.66 % over 20 days and the total move -0.53 % (1142 cases), which is -3.0 and -2.4 times the 0.22 % round trip. The top forecast quintile's strength (+0.259 against -0.079 for the bottom quintile, t 3.93 on 1362 grid cases) rests on the same single grid as F1.
- **F3:** The book's shorts carry its loss and its longs earn only the drift. Short coin-days lose 0.185 % per day (13 447 days) while the coins rose 0.148 % on those days. Long coin-days earn 0.134 % per day (12 029 days) against the coins' 0.131 %.
- **F4:** The book's record has an anomaly to inspect before reading anything into it. DOGE's book loses 1.50 % per day against holding's +0.056 %, and flat days (position 0, 3026 coin-days) show a book return of -0.67 % per day. This looks like a book-value or accounting fault on DOGE, not a market pattern.
- **F5:** By year, on the single offset-0 grid, the 20-day reversal slope runs both ways: t -3.00 in 2019 (66 cases), +2.38 to +4.07 in 2023 to 2025 (152 to 179 cases), and between -0.51 and +1.43 in 2018 and 2020 to 2022. Because F1 shows offset 0 is not representative, this regime split is not established.
- **F6:** No other angle stands out once the number of tests (more than 15 signals and splits) is counted:

## Ideas
- No ideas: The only strong pattern, the 20-day reversal, vanishes when the grid's starting point changes (mean t -0.88 over 20 offsets), and every other angle stays within what chance gives across the many angles looked at (forecast, 1-day move by horizon, by year, coin and volume level, volatility, range, nearness to highs, weekday, the book's long and short sides).

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
