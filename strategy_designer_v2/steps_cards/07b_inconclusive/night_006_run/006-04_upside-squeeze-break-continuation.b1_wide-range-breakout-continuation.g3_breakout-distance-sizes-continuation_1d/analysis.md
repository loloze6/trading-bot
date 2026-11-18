---
line: 7.b inconclusive
backtest: 006-04_upside-squeeze-break-continuation.b1_wide-range-breakout-continuation.g3_breakout-distance-sizes-continuation_1d
idea tested: 006-04_upside-squeeze-break-continuation.b1_wide-range-breakout-continuation.g3_breakout-distance-sizes-continuation
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.2979 USD
---
## Findings
- **F1:** The test's slope t of +1.79 on 108 breakout cases rests on a few very large outcomes. Trimming the top and bottom 5 % of excess returns turns it to −1.45 (96 cases), dropping the 3 largest excess returns gives −1.47, and the rank correlation of forecast with excess return is −0.13 (p 0.18).
- **F2:** The slope is not shared across coins. ZEC alone carries it with t +4.07 on 21 cases; without ZEC it is −0.47 on 87 cases, LTC is −2.77, and ETH and XMR are negative.
- **F3:** The slope also flips between years: −1.58 in 2021, −1.16 in 2023, −1.10 in 2024 and +3.02 in 2025.
- **F4:** Breakouts as a group do rise more than usual, but without grading by distance. The mean excess 10-day return after any close above the prior 20-day high is +0.064 (t 2.78, 108 cases, 59 % positive, median +0.040), against −0.004 on the 1,583 cases without a breakout.
- **F5:** The forecast terciles show no grading. Mean excess returns are +0.079, +0.014 and +0.101 from lowest to highest, and the top 8 forecasts have a mean of +0.244 but a median of −0.012 with half positive, so the largest forecasts are a lottery.
- **F6:** The 10-day horizon is not a peak where a graded effect shows. On the forecast the slope t is +0.65 at 5 days and −0.44 at 20 days, and the mean excess is negative at 20 days (−0.033, 49 cases).
- **F7:** Among breakouts, the coin's own prior 10-day return grades the next 10-day excess return better than the distance does: slope t +3.14, rank correlation +0.15, 98 cases. Over all grid cases the same slope is t +3.39 (1,547 cases), but with a rank correlation of only +0.06.

## Ideas
- `006-04_upside-squeeze-break-continuation.b1_wide-range-breakout-continuation.g3_breakout-distance-sizes-continuation.b1_breakout-distance-more-coins` (from F1, F2, F3): The further a coin's close sits above the highest high of its prior 20 days, as a share of that high, the further its price rises over the next 10 days.
- `006-04_upside-squeeze-break-continuation.b1_wide-range-breakout-continuation.g3_breakout-distance-sizes-continuation.b2_breakout-momentum-sizes-continuation` (from F4, F5, F7): While a coin's close sits above the highest high of its prior 20 days, the larger its own 10-day return, the further its price rises over the next 10 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
