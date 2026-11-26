---
line: 7.g patterns
backtest: 032-01.b1.b1.e2.d2.d1.d1_chop-continuation-exit-on-break_1d
idea tested: 032-01.b1.b1.e2.d2.d1.d1_chop-continuation-exit-on-break
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4126 USD
---
## Findings
- **F1:** On a non-overlapping 7-day grid, when a coin's 30-day efficiency ratio is below its median, its 7-day move scaled by 30-day daily swings is followed over the next 7 days by an excess move the same way: +2.34 % per case (t 2.19 over 130 days, 429 cases), graded t 2.13. That is a strength of 0.15 of a usual 7-day move (15.1 %), about 12 times the 0.19 % cost of a trade. The tested 1-day horizon gives only +0.14 %, 0.7 times the cost.
- **F2:** The continuation grows as the 30-day efficiency ratio falls. The slope of the next 7-day excess return on the scaled 7-day move is 0.025 (t 2.43, 286 cases) in the lowest ER third, 0.030 (t 3.47, 286) in the middle third, and 0.002 (t 0.25, 287) in the highest third.
- **F3:** Inside low-ER months, the effect is strongest when the 7-day and 30-day moves share a sign: graded mean +3.20 % (t 2.86 over 103 days, 230 cases). When they disagree it is +0.98 % (t 0.69, 89 days). In high-ER months with agreement it is +2.24 % (t 0.88).
- **F4:** In low-ER months the move grows with the size of the scaled week. The top third of |scaled 7-day move| is followed by +4.29 % (t 2.16, 67 days) and the bottom third by +1.85 % (t 1.84, 62 days). In the ER × |z| table, low- and mid-ER big-z cells give +3.9 % (t 2.12) and +4.3 % (t 2.83).
- **F5:** The low-ER 7-day continuation points the same way in every year (graded mean +4.7 %, +1.2 %, +1.5 %, +1.6 % in 2018 to 2021) and in every coin (+1.5 % to +2.7 %, LTC t 2.12, others t 1.11 to 1.72). No single year or coin is significant alone.
- **F6:** The book's trades held 8 days or more earn +9.3 % net (long, 120 trades) and +8.4 % net (short, 140), and those held 4 to 7 days earn +3.0 % and +1.5 %. Trades closed after 1 day lose −0.88 % (469 longs) and −2.31 % (469 shorts). The exit on the first day the regime breaks cuts the move the idea captures.
- **F7:** The same continuation fades over longer and shorter horizons. In low-ER months the graded mean is +0.59 % at 3 days (t 1.39, 324 days) and +3.05 % at 14 days (t 1.47, 52 days). The 7-day horizon is the clearest.
- **F8:** Not findings, given how many angles were looked at:

## Ideas
- `032-01.b1.b1.e2.d2.d1.d1.g1_choppy-month-weekly-continuation` (from F1, F2, F4, F5, F6): When a coin's past 30 days have made little net progress compared with the sum of its daily moves, its 7-day return counted in 30-day daily swings is followed by a move the same way over the next 7 days. The less net progress the 30 days made and the larger the scaled 7-day move, the larger that following 7-day move.
- `032-01.b1.b1.e2.d2.d1.d1.g2_agreeing-week-continues-weekly` (from F3, F1, F6, F7): When a coin's past 30 days have made little net progress compared with the sum of its daily moves and its 7-day return points the same way as its 30-day return, the 7-day return counted in 30-day daily swings is followed by a move the same way over the next 7 days, larger the larger the scaled 7-day move.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
