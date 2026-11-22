---
line: 7.d not profitable
backtest: 026-03_weekend-reversal-exceeds-weekday.b1_midweek-moves-continue-into-weekend_1h
idea tested: 026-03_weekend-reversal-exceeds-weekday.b1_midweek-moves-continue-into-weekend
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3597 USD
---
## Findings
- **F1:** The book's whole edge per case is too thin for its cost: the 2379 Thursday-23:00 cases move +0.30 % in total over 48 hours against a 0.19 % round-trip cost, the 4130 recorded trades average −0.09 % gross and −0.19 % net, and the book is flat five days a week, so its mean daily return is only 0.011 % against 0.05 % required.
- **F2:** The continuation lives almost only after midweek rises: long cases move +0.96 % total (+0.69 % unusual, 1132 cases), while short cases move −0.36 % total (−0.09 % unusual, 1247 cases), so the short half of the book pays the cost for nothing.
- **F3:** The effect after rises is graded by size. Rises in the largest |48h move| quintile continue +2.12 % over 48 hours (t 4.02, 249 cases) and those in the fourth quintile +1.15 % (t 3.23, 234 cases). The matching falls show no continuation: −0.09 % (t −0.19) in the top quintile and −0.87 % (t −2.42, a rebound) in the fourth.
- **F4:** The continuation shows when the midweek move goes the same way as the coin's 14-day return: +0.61 % over 48 hours (t 3.33, 1303 cases). Against the 14-day trend it partly reverses: −0.33 % (t −1.65, 809 cases).
- **F5:** Among the largest 48-hour moves, only those read on Thursday's close carry the following 48-hour move: +1.08 %, t 2.97, 470 cases. Every other weekday's |t| is 1.45 or less.
- **F6:** Across all weekdays the two largest move quintiles split by direction. Rises continue +0.56 % over the next 48 hours (t 4.23, 3452 cases). Falls are followed by a rise, −0.36 % in the fall's direction (t −2.67, 3127 cases).
- **F7:** The book misses most of the coin's rise: holding the coins earns 0.33 % on Fridays and 0.45 % on Saturdays per day, while the book earns 0.03 % and 0.11 %. Combined with the yearly sign flips (2019: −0.84 % per case, t −2.57; 2023: −0.32 %), this leaves the Sharpe 0.29 below holding and the Calmar at 0.08.

## Ideas
- `026-03_weekend-reversal-exceeds-weekday.b1_midweek-moves-continue-into-weekend.d1_midweek-rises-carry-into-weekend` (from F1, F2, F3, F7): A coin's 48-hour return over Wednesday and Thursday is followed by a move in the same direction over the next two days, Friday and Saturday, and the larger the Wednesday-Thursday move, the larger the move that follows, only while that midweek move is a rise.
- `026-03_weekend-reversal-exceeds-weekday.b1_midweek-moves-continue-into-weekend.d2_trend-aligned-midweek-move-continues` (from F1, F4, F5): A coin's 48-hour return over Wednesday and Thursday is followed by a move in the same direction over the next two days, Friday and Saturday, and the larger the Wednesday-Thursday move, the larger the move that follows, only while that move goes the same way as the coin's 14-day return.
- `026-03_weekend-reversal-exceeds-weekday.b1_midweek-moves-continue-into-weekend.d3_sharp-two-day-falls-rebound` (from F2, F3, F6): After a fall in a coin's 48-hour return, the coin rises over the next two days, and the larger the fall, the larger the rebound.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
