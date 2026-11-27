---
line: 7.b inconclusive
backtest: 067-01.b1.b1.b2_choppy-stretch-carry-all-coins_1d
idea tested: 067-01.b1.b1.b2_choppy-stretch-carry-all-coins
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3879 USD
---
## Findings
- **F1:** The tested measure points the predicted way but is too weak to count: over all folds the main measure is +0.0059 with a day-clustered t of 0.79 over 1641 cases on 429 days. The idea's size is a strength of 0.014 of a usual move (+0.28 %, t 0.92, 1180 days). The test already used every coin and every fold available on daily bars, so more data cannot be added.
- **F2:** On folds B and C, the 5-day grid shows the same weak positive result: score mean 0.038 with t 1.62 (390 cases, 166 days). Clipping the 2.5 % tails of the returns gives 0.014 with t 1.45, and dropping DOGE gives 0.020 with t 1.52. One coin's outliers lift the mean but are not the whole effect.
- **F3:** The effect sits in the calmer cases. Splitting each coin's cases by its 30-day swing, the calmer half scores 0.033 with t 2.00 at 5 days (154 cases, 65 days) and 0.068 with t 2.49 at 10 days. The wilder half scores 0.080 with t 1.47 and 0.072 with t 1.54, noisier and driven by large single moves.
- **F4:** Measured as 30-day swing against 90-day swing, the result separates more cleanly. Where the recent swing is at or below its longer norm, the clipped score is 0.045 with t 2.30 at 5 days (134 cases, 58 days) and 0.095 with t 2.16 on a 10-day grid (66 cases, 30 days). Where it is above, the score is 0.023 with t 0.78 and 0.044 with t 0.79.
- **F5:** The carry builds up to about 10 days and then fades. In the direction of the stretch, the return beyond drift is +1.1 % at 1 day (t 1.87), +2.4 % at 5 days (t 1.80) and +3.1 % at 10 days (t 2.23). On a non-overlapping 20-day grid the score is -0.005 (t -0.12, 100 cases).
- **F6:** The grading by stretch size is weak. By quartile of |forecast|, the 5-day directional move rises from +0.8 % and +0.4 % in the two lower quartiles to +3.3 % and +5.0 % in the two upper ones. But on clipped returns the terciles are flat: 1.1 %, 0.7 % and 1.6 %, with t between 0.6 and 1.3.
- **F7:** The effect is uneven over time and points the same way on both sides. By year, the 5-day score is 0.000 in 2018 and -0.004 in 2019, then 0.026 in 2020 and 0.104 in 2021. Long cases score 0.051 (t 1.11) and short cases 0.026 (t 1.63).

## Ideas
- `067-01.b1.b1.b2.b1_calm-choppy-stretch-carry` (from F1, F3, F4, F5): In a choppy, calm market, the further a coin's close stands from its 20-day average, measured in units of its 20-day standard deviation of daily returns, the more the coin keeps moving the same way over the next 10 days, rising after closes above the average and falling after closes below it.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
