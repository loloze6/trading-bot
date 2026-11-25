---
line: 7.g patterns
backtest: 032-01.b1.b1_large-weekly-rise-continues_1d
idea tested: 032-01.b1.b1_large-weekly-rise-continues
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.3867 USD
---
## Findings
- **F1:** A large down day is followed by a graded next-day rebound. After a day whose return is below −1 of the coin's 30-day daily swing, the next day's unusual return falls by 0.91 % per unit of that swing: the larger the fall, the larger the rebound (slope −0.0091, t −4.36, 759 cases, not day-clustered). By size of fall, the rebound is +3.78 % after falls below −3 swings (t 1.49, 48 cases, 21 days) and +1.18 % after falls of −3 to −2 swings (t 1.75, 131 cases, 67 days). The rebound is 6 to 20 times the 0.19 % cost of a trade.
- **F2:** Large up days show no mirror effect. The next day's unusual return is −0.58 % after rises of +2 to +3 swings (t −1.09) and −0.36 % after rises above +3 swings (t −0.41). The rebound is a down-day effect only.
- **F3:** The rebound after a fall below −1 swing appears everywhere I looked. It is positive in all 12 windows (w7 to w18), from +0.15 % to +2.27 % a day, with t 4.19 in w10 and t 2.41 in w18. It is positive in all 6 coins, from +0.24 % (BTC) to +1.32 % (XMR), with t 2.99 for XMR and t 2.33 for ZEC.
- **F4:** The rebound grows with the coin's volatility, ranked against the coin's own history. After a fall below −1 swing, it is +0.13 % in the lowest third of 30-day volatility (t 0.27, 227 cases), +0.69 % in the middle third (t 1.72, 295 cases) and +1.56 % in the highest third (t 1.72, 237 cases).
- **F5:** The rebound is larger when the fall comes inside a rising week. After a fall below −1 swing, it is +1.34 % when the 7-day return is positive (t 2.91, 212 cases, 118 days). It is +0.59 % when the 7-day return is negative (t 1.19, 547 cases, 176 days).
- **F6:** The rebound carries over a 3-day horizon, measured on a non-overlapping 3-day grid. After a fall below −2 swings, the next 3 days' unusual move is +2.64 % (t 1.90, 48 cases, 21 days), against −0.14 % on ordinary days (t −0.31).
- **F7:** The tested book does not capture this pattern. It was long on only 24.6 % of the days with a fall below −2 swings.
- **F8:** The weekly continuation in the tested idea is one-sided. The slope of the next 7 days' unusual move on the scaled 7-day return is 0.024 for rising weeks (t 2.57, 437 cases) and −0.004 for falling weeks (t −0.32, 422 cases).

## Ideas
- `032-01.b1.b1.g1_large-down-day-next-day-rebound` (from F1, F2, F3, F6, F7): The larger a coin's one-day fall, counted in its daily swing over the past 30 days, the larger its rise over the next day.
- `032-01.b1.b1.g2_agitated-down-day-rebound-grows` (from F1, F4): When a coin's 30-day volatility is high compared with its own past, the larger its one-day fall counted in its 30-day daily swing, the larger its rise over the next day, and the rebound grows with how high that volatility is.
- `032-01.b1.b1.g3_dip-in-rising-week-rebounds` (from F1, F5, F8): When a coin's 7-day return is positive, the larger its one-day fall counted in its 30-day daily swing, the larger its rise over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
