---
line: 7.g patterns
backtest: 032-02.b1.e1.e1.e2_compressed-ranges-precede-rises_1d
idea tested: 032-02.b1.e1.e1.e2_compressed-ranges-precede-rises
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4113 USD
---
## Findings
- **F1:** Where the close sits in its own 60-day closing range predicts the coin's next days in the direction of that position, which is the opposite of the brief's fade. The date-clustered t of the slope of the vol-scaled excess return on range position is 2.09 to 2.82 at a 5-day horizon across all five grid offsets (846 cases, 152 dates). At a 10-day horizon it is 1.55 to 2.46 across all five offsets (414 cases, 74 dates).
- **F2:** On the 10-day grid, the mean excess 10-day return rises with range position by quintile. The bottom quintile (mean position -0.97) gives -0.87 %, the middle -3.34 %, the fourth +3.04 % and the top quintile (mean position +0.90) gives +5.14 % (83 cases each). The slope is positive on all six coins (t 1.14 to 2.48).
- **F3:** The range-position effect sits in compressed coins. The slope is 0.75 (t 2.27, 207 cases) where the 60-day range in mean absolute daily moves is at or below its median, and 0.17 (t 0.99, 207 cases) where it is wider.
- **F4:** Breakouts from compressed ranges keep going rather than fail. On days closing above a tight range's top (lowest third of range width), the move against the break averages -4.88 % over 5 days and -11.2 % over 10 days (155 break days, overlapping, not clustered).
- **F5:** The tested compression measure carries no information. Its 20-day slope has t 0.11 (827 cases, 147 dates), and its quintiles' excess 20-day returns (-2.98 %, -2.19 %, +5.91 %, -1.46 %, +0.78 %) are not monotone. The book's mean daily return on days in a position, 6.96e-05, is below the 0.0005 floor.
- **F6:** Friday and Saturday daily returns are the highest of the week: +0.54 % (t 1.75, 207 dates) and +0.58 % (t 2.26, 206 dates) when coins are averaged per date. Friday and Saturday exceed the other days in every year from 2018 to 2021 and on all six coins. Many angles were looked at, so this is borderline, and it cannot be graded.
- **F7:** The 20-day return in units of 60-day volatility also predicts the next days' excess return the same way. Its t is 2.39 at 5 days and 2.23 at 10 days on grid 0, and 1.69 to 2.31 across the 5-day offsets. This is consistent with the continuation in F1.

## Ideas
- `032-02.b1.e1.e1.e2.g1_compressed-range-position-continues` (from F1, F2, F3, F7): The higher a coin's daily close sits within its 60-day range of closes, measured from the bottom edge to beyond the top edge, the larger its rise over the next 10 days, and the lower it sits, the larger its fall. The effect is strongest when that 60-day range is narrow against the coin's average absolute daily move.
- `032-02.b1.e1.e1.e2.g2_tight-range-breakouts-keep-going` (from F4, F3, F1): The further a coin's daily close goes past the edge of a narrow 60-day range of closes, measured in its average absolute daily moves, the larger its further move in the same direction over the next 10 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
