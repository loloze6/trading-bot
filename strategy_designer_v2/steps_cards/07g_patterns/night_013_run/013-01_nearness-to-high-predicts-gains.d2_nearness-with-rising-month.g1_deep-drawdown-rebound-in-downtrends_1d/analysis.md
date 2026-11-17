---
line: 7.g patterns
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends_1d
idea tested: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3220 USD
---
## Findings
- **F1:** Across all bars on the non-overlapping 7-day grid, a coin's 14-day return predicts its 7-day forward excess return with slope 0.0515 (t 3.77, n 2155 independent cases). Its 30-day return does the same more weakly: slope 0.0248 (t 2.88, n 1723), and a per-coin rank version still gives t 2.51.
- **F2:** The 30-day momentum is uneven, not steady. It is strong in 2025 (t 4.24) and in ZEC (t 2.80), reversed in 2018 (t -3.88), and between -1.3 and +1.1 in the other years and coins. The 60-day return carries nothing (slope -0.003, t -0.54, n 1147), so the effect sits in the last two to four weeks.
- **F3:** The tested depth relation is not monotone when the 30-day return is negative. Only the deepest fifth below the 60-day high is followed by a positive excess (+0.0208, t 1.74, n 166). The next fifth is the worst (-0.0281, t -2.65), and the fifth closest to the high is -0.0076 (t -1.10). This matches the step-5 slope of t -0.37 and the book's mean daily return of 8.4e-05.
- **F4:** A coin's volume relative to its 20-day average (log) predicts its 7-day forward excess return with slope 0.0125 (t 2.64, n 2011). The lowest-volume fifth averages -0.0124 (t -2.32), but the effect is carried mostly by ZEC (t 2.21) and XRP (t 1.75); in BTC, ETH, LTC and XMR the t lies between -0.1 and 1.0.
- **F5:** Saturdays are the strongest day. The average-of-coins Saturday return is +0.00454 (t 3.04, n 414 days), against -0.0018 to +0.0033 on other days. Saturday beats the other days in all six coins (t from 0.34 to 2.67) and in seven of eight years (2023 is the exception, t -1.24).
- **F6:** Closes at a new 60-day high are followed by a 7-day excess of +0.0198 (n 158), against -0.0014 for the other bars. The Welch t is 1.44, so the brief's breakout continuation is in the right direction but not distinct from chance.

## Ideas
- `013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g1_two-week-momentum-continuation` (from F1, F2, F3, F6): The higher a coin's 14-day return, the higher its return over the next 7 days.
- `013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g2_volume-surge-precedes-gains` (from F4): The higher a coin's traded volume over the past day relative to its average over the past 20 days, the higher its return over the next 7 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
