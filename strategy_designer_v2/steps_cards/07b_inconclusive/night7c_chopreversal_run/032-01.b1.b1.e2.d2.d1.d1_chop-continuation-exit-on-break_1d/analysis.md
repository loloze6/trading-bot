---
line: 7.b inconclusive
backtest: 032-01.b1.b1.e2.d2.d1.d1_chop-continuation-exit-on-break_1d
idea tested: 032-01.b1.b1.e2.d2.d1.d1_chop-continuation-exit-on-break
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3714 USD
---
## Findings
- **F1:** The tested next-day effect points the way the idea predicts but is diluted. On folds B and C, step 5's measure recomputes to a t of 1.82 over 1217 days. Read without the forecast weight on a 1-day grid, the chop-and-agreement bars give +0.46 % per case (t 3.00 over 899 days), with both sides positive: long +0.37 % (t 2.85), short +0.41 % (t 3.14).
- **F2:** The standardised forecast loses the grading the idea states. Next-day signed excess by |forecast| tercile is flat at 0.35 %, 0.43 % and 0.38 %. By the raw scaled 7-day move (|7-day return / (30-day daily sd × √7)|) it grows: 0.32 %, 0.52 % and 0.55 %.
- **F3:** The test measured the effect at a shorter horizon than where it shows. On non-overlapping grids, chop-and-agreement cases give +1.06 % over 3 days (t 2.62, 307 days), +2.37 % over 5 days (t 3.13, 184 days) and +3.76 % over 7 days (t 3.02, 120 days). The same 7-day measure is +0.17 % (t 0.12) when choppy without agreement and −1.68 % (t −1.03) when the 30-day efficiency is high.
- **F4:** Over 7 days the follow-through grows with the scaled 7-day move. By |scaled move| tercile it is +1.93 % (t 1.26), +3.85 % (t 2.09) and +5.51 % (t 2.78), with a case-level correlation of 0.11. At 14 days the lowest tercile turns negative (−2.53 %) while the upper two stay at +5.2 % and +5.9 %.
- **F5:** The 7-day effect is spread rather than confined to one part of the data, but it varies in strength.
- **F6:** Exiting when the regime breaks cuts the move rather than protecting it.
- **F7:** Per case, the tested 1-day move (+0.14 %) is 0.7 times the 0.19 % cost of a trade, while the 7-day move in the same situation (+3.76 % in folds B and C) is about 20 times that cost.

## Ideas
- `032-01.b1.b1.e2.d2.d1.d1.b1_chop-continuation-more-coins` (from F1, F5): When a coin's past 30 days have gone back and forth with little net progress compared with the sum of its daily moves, its 7-day move counted in 30-day daily swings is followed by a move the same way, day by day, only on the days the 30 days are still choppy and the 7-day move still points the same way as the 30-day net move. The larger the scaled 7-day move, the larger the following daily moves, and the follow-through stops on the first day either the chop or the agreement ends.
- `032-01.b1.b1.e2.d2.d1.d1.b2_choppy-month-weekly-continuation` (from F2, F3, F4, F6, F7): When a coin's past 30 days have gone back and forth with little net progress compared with the sum of its daily moves, and its 7-day move points the same way as its 30-day net move, its 7-day move counted in 30-day daily swings is followed by a move the same way over the next 7 days. The larger the scaled 7-day move, the larger the following 7-day move.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
