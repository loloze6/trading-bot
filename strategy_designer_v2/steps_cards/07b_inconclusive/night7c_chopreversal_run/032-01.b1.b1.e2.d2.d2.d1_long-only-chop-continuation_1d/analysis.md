---
line: 7.b inconclusive
backtest: 032-01.b1.b1.e2.d2.d2.d1_long-only-chop-continuation_1d
idea tested: 032-01.b1.b1.e2.d2.d2.d1_long-only-chop-continuation
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.3259 USD
---
## Findings
- **F1:** The tested result points the way the idea predicts but falls short of the bar. On the visible folds B and C, the positive-forecast 7-day grid cases end +2.24 % above the coin's drift. That mean has an unclustered t of 2.20 on 250 cases, but the cases bunch on only 103 days, and once the cases of one day are taken together the t falls to 1.38. This matches step 5's +1.19 % with t 1.35 on 532 cases over 233 days: the evidence is limited by the number of distinct days, not by the sign.
- **F2:** The effect is graded as the idea says. By forecast tercile, the mean unusual 7-day move is -1.71 % (t -1.02, 83 cases), then +2.76 % (t 1.55, 83 cases), then +5.64 % (t 3.17, 84 cases). The top tercile stays at +4.89 % (day-clustered t 2.30, 50 days) after removing each coin's own mean for that year, against -1.79 % for the bottom tercile, consistent with step 5's top-minus-bottom of +2.99 %.
- **F3:** The coin's own market drowns much of the result. The active cases follow the year's market move: -6.30 % in 2018 (t -1.89, 20 days), -1.44 % in 2019, +3.45 % in 2020 and +9.55 % in 2021 (t 2.91, 28 days). In the same years all grid cases moved -3.16 %, -0.55 %, +1.93 % and +1.74 %. Measured against each coin's own mean for that year, the overall excess shrinks to +1.82 % (day-clustered t 1.17).
- **F4:** The effect does not depend on one coin, and it shows at the plan's horizon only. All six coins have a positive 7-day mean unusual move, from +0.69 % on ETH to +4.36 % on XRP, each with t between 0.26 and 1.31 on 35 to 50 cases. The same signal gives +0.31 % (t 0.81) over 3 days and -0.11 % (t -0.04) over 14 days. A longer or shorter horizon would not sharpen the test; more independent cases at 7 days would.
- **F5:** The continuation grows with 30-day volatility, as the brief's agitation reasoning implies. By volatility tercile, the excess over the coin-year mean is +2.03 % (t 0.82), then +2.93 % (t 1.63), then +5.90 % (t 1.85). Against this, inactive grid bars sit at -0.58 % (t -0.61, 212 days).

## Ideas
- `032-01.b1.b1.e2.d2.d2.d1.b1_choppy-month-continuation-more-coins` (from F1, F2, F4): When a coin's past 30 days have gone back and forth with little net progress compared with the sum of its daily moves, and both its 7-day and 30-day net moves are up, its 7-day rise counted in 30-day daily swings tends to be followed by a further rise over the next 7 days, a rise that is larger after the largest scaled 7-day rises and grows faster than in proportion to their size.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
