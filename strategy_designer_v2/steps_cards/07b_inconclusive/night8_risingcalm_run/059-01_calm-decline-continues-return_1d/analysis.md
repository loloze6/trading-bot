---
line: 7.b inconclusive
backtest: 059-01_calm-decline-continues-return_1d
idea tested: 059-01_calm-decline-continues-return
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 1
cost: 0.2225 USD
---
## Findings
- **F1:** On folds B and C, the plan's main measure has the predicted sign but is weak. The slope of the 5-day excess return on the forecast is +0.00116, with t 1.33 over 428 non-overlapping calm grid bars where the forecast is below 0. This matches the verdict's slope of +0.000496 with t 0.97 over 907 bars on all folds. The supporting size is also on the idea's side: the unusual move is +0.79 % per case with t 2.02 over 560 days. The result points the idea's way but falls short of the bar.
- **F2:** The decline is followed by a fall that is mostly a level effect, not a graded one. Calm 5-day grid bars with a negative forecast average an excess return of -1.47 %. By forecast quintile, from the deepest decline (forecast -18.5) to the shallowest (-1.6), the excess returns are -2.94 %, -0.26 %, -1.84 %, -2.05 % and -0.22 %. Only the shallowest quintile is clearly flat, so the slope is diluted.
- **F3:** The grading shows more clearly at a shorter horizon. Over 3 days the slope on the forecast has t 2.72 over 708 bars, and the slope on the raw swing-scaled decline has t 2.36 over 557 bars. Over 1, 10 and 20 days the t values are 0.32, 1.08 and -0.36.
- **F4:** The effect is concentrated in falling calm markets, those whose 60-day return is below -10 %. There the 5-day slope has t 2.14 over 158 bars and the mean excess is -2.82 % with t -3.35. In choppy markets the slope has t -0.55 over 45 bars, and in rising markets t 0.16 over 40 bars.
- **F5:** The effect is uneven over time and across coins. The slope is positive in 2018 (t 1.20), 2019 (t 0.95) and 2020 (t 0.43), but negative in 2021 (t -1.72). Coin slopes range from t -0.96 for BTC to t 1.83 for ETH, with 63 to 77 bars per coin. These small groups add noise to a pooled slope that is already weak.
- **F6:** The test ran on 6 of the 19 coins available. Thirteen more coins have daily bars in folds A and D, and partly in B and C, so the same idea can be measured on more cases without narrowing it.

## Ideas
- `059-01.b1_calm-decline-all-coins` (from F1, F5, F6): In a calm market, the further a coin's 14-day return has fallen below zero, measured in units of its own 30-day daily swing, the larger its fall over the next 5 days.
- `059-01.b2_falling-calm-decline-continues` (from F4, F2): In a falling, calm market, the further a coin's 14-day return has fallen below zero, measured in units of its own 30-day daily swing, the larger its fall over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
