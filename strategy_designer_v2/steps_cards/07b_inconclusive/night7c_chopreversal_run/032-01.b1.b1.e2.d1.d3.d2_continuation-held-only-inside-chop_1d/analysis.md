---
line: 7.b inconclusive
backtest: 032-01.b1.b1.e2.d1.d3.d2_continuation-held-only-inside-chop_1d
idea tested: 032-01.b1.b1.e2.d1.d3.d2_continuation-held-only-inside-chop
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3356 USD
---
## Findings
- **F1:** The test's own result points the way the idea predicts but falls short of the bar: the slope on forecast/10 is +0.0012 (t 1.56) over 8058 active bars on 2546 days, and the supporting mean is +0.17 %, so it fails only on the strength of the evidence, not on its direction.
- **F2:** On the explored folds the next-day move follows the scaled week on average: the signed next-day excess return is +0.39 % (t 2.70; 3807 cases on 1217 days). But the next-day grading is weak: the clustered slope on forecast/10 has t 1.81, and the signed slope on the size of the raw scaled week is −0.0006 (t −0.24).
- **F3:** At one day the strongest cases add nothing. The top quartile of the raw scaled week earns +0.13 % the next day (t 0.36), against +0.51 % (t 2.89) and +0.67 % (t 2.66) for the middle quartiles. This flat, then falling, pattern is what keeps the one-day slope short of the bar.
- **F4:** Over the next 7 days the effect is graded. On a non-overlapping 7-day grid the clustered slope on forecast/10 is 0.0232 (t 2.76; 512 cases, 172 days) and the signed mean is +2.4 % (t 2.33). The top quartile of the raw scaled week gives +5.0 % (t 2.91), against +0.9 % (t 0.68) for the bottom quartile.
- **F5:** The effect is uneven across coins and years. XMR's next-day signed excess is −0.01 % (t −0.06; 691 cases), while the other five coins range from +0.30 % to +0.58 %. By year it ranges from +0.13 % in 2020 (t 0.48) to +0.73 % in 2021 (t 2.25).
- **F6:** Held one day at a time, the move per case (+0.14 %) is 0.7 times the 0.19 % cost of a trade. The 7-day signed move of +2.4 % per case is about 12 times that cost.

## Ideas
- `032-01.b1.b1.e2.d1.d3.d2.b1_chop-continuation-more-coins` (from F1, F2, F5): When a coin's past 30 days have gone back and forth with little net progress compared with the sum of its daily moves, its 7-day move counted in 30-day daily swings tends to be followed by a move the same way over the following days, only while its 30-day return points the same way and only for as long as the past 30 days are still going back and forth at each day's close. The larger that scaled 7-day move, the larger the following move.
- `032-01.b1.b1.e2.d1.d3.d2.b2_chop-continuation-over-week` (from F3, F4, F6): When a coin's past 30 days have gone back and forth with little net progress compared with the sum of its daily moves, its 7-day move counted in 30-day daily swings tends to be followed by a move the same way over the next 7 days, only while its 30-day return points the same way. The larger that scaled 7-day move, the larger the 7-day move that follows.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
