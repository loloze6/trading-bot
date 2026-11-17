---
line: 7.b inconclusive
backtest: 013-06_breakout-volume-drives-continuation_1d
idea tested: 013-06_breakout-volume-drives-continuation
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 1
cost: 0.1912 USD
---
## Findings
- **F1:** The tested measure lies on the side the idea predicts but falls short of the bar: the high-volume breakouts beat the low-volume ones by +0.195 in 30-day excess return (Welch t 1.66, 30 vs 30 kept cases, out of 445 active breakout bars), and the Spearman correlation between forecast and the 30-day outcome is +0.15.
- **F2:** The gap comes from a few very large winners in the strongest-volume cases: the top forecast quartile (median volume ratio 5.9, forecast capped at 20) has a mean 30-day excess of +0.256 but a median of only +0.017; the overall outcome spread is 0.46 (max +2.31); dropping the top 5% of outcomes cuts the difference to +0.028 (t 0.43); and the rank test gives p 0.18.
- **F3:** The ordering is graded across forecast quartiles at 30 days, with mean excess returns of -0.014, -0.004, +0.116 and +0.256 from lowest to highest relative volume.
- **F4:** The sign holds in most coins and recent years but not in all of them:
- **F5:** The effect grows with the horizon up to 30 days (difference +0.057 at 10 days with t 0.83, +0.102 at 20 days with t 1.06, +0.195 at 30 days with t 1.66), so the plan's 30-day horizon is where it shows best. Only 60 non-overlapping cases on six coins leave the test too few for a skewed outcome like this one.

## Ideas
- `013-06_breakout-volume-drives-continuation.b1_breakout-volume-more-coins` (from F1, F2, F3, F4, F5): When a coin closes above its prior 52-week high, the higher its volume on the breakout day relative to its own 90-day average, the larger its return over the next 30 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
