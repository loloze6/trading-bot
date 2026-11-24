---
line: 7.g patterns
backtest: 031-01.g1.g1.g1.g2_thursday-run-carries-two-days_1d
idea tested: 031-01.g1.g1.g1.g2_thursday-run-carries-two-days
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4401 USD
---
## Findings
- **F1:** The tested graded momentum (14-day return in usual moves, clipped, times the drift-removed 2-day return) shows only on bars that start on Thursday (mean 0.0084, t 2.98, 361 days) and on Friday (0.0061, t 2.80, 359 days); every other weekday is flat (Mon t −0.05, Tue t 0.35, Wed t 1.41, Sat t −0.14, Sun t −0.49).
- **F2:** The effect sits almost entirely on the rising side. On Thursday bars after a positive 14-day return, the drift-removed 2-day move in the return's direction is +0.84 % (t 2.62, 283 days; graded t 3.64), against +0.08 % after a negative one (t 0.23; graded t −0.14). On Friday bars the rising side gives +0.82 % (t 3.08, 280 days) and the falling side +0.38 % (t 1.30).
- **F3:** The book earns on its longs and loses on its shorts. Long trades average +1.68 % net (1643 trades) and short trades −1.34 % (1662). Per coin-day on Thursday bars, long positions gain +0.42 % (1092) and short positions −0.20 % (1105); on Friday bars, longs gain +0.59 % (1079) and shorts −0.05 % (1099).
- **F4:** The Thursday-and-Friday momentum is positive in all six coins (t from 1.30 for XMR to 3.70 for ZEC) and in 6 of 8 years. It is flat in 2022 (t 0.09) and 2023 (t −0.16), which fits the book's failing Calmar (0.46) and its 8 losing windows out of 24.
- **F5:** After a coin's largest 1-day rises (top quintile, mean 1.39 usual daily moves), the drift-removed 5-day return is +1.60 % (t 2.42, 598 cases). That quintile beats the year's average 5-day return in all 8 years. The graded version over all days is weaker (t 1.62, 544 days).
- **F6:** The rising-side move after a Thursday close (+0.84 % over 2 days, F2) is about 4.4 times the 0.19 % cost of a trade. The idea as tested moves +0.50 %, or 2.6 times the cost.

## Ideas
- `031-01.g1.g1.g1.g2.g1_thursday-rising-run-carries` (from F1, F2, F3, F6): The higher a coin's positive 14-day return, measured in its usual daily moves at Thursday's close (UTC), the more it rises over the following Friday and Saturday together.
- `031-01.g1.g1.g1.g2.g2_friday-run-carries-weekend` (from F1, F2, F4): The higher a coin's 14-day return, measured in its usual daily moves at Friday's close (UTC), the more it rises over the following Saturday and Sunday together.
- `031-01.g1.g1.g1.g2.g3_big-up-day-continues` (from F5): The larger a coin's 1-day rise, measured in its usual daily moves, the more it rises over the next 5 days beyond its normal drift.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
