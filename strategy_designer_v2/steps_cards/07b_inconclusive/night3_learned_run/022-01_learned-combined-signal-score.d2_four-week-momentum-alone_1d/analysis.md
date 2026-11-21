---
line: 7.b inconclusive
backtest: 022-01_learned-combined-signal-score.d2_four-week-momentum-alone_1d
idea tested: 022-01_learned-combined-signal-score.d2_four-week-momentum-alone
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 1
cost: 0.1931 USD
---
## Findings
- **F1:** The tested result points the way the idea predicts but falls just short of the bar. The mean of forecast/10 × the excess 5-day return is +0.0045, with t 1.95 over 3,419 non-overlapping cases. The size, +0.51 % unusual move per case (strength 0.043), is 2.6 times the 0.19 % cost of a round trip.
- **F2:** The effect is mixed across coins and periods.
- **F3:** The relation is not linear across the forecast.
- **F4:** Where the coin's 20-day volatility stands within its own range shapes the effect. In the lowest tercile the measure is +0.0068 (t 1.97) and in the middle tercile +0.0095 (t 2.53). In the highest tercile it is -0.0034 (t -0.69), where the coin's own large moves drown it.
- **F5:** The plan's 5-day horizon is not where the measure is strongest.

## Ideas
- `022-01_learned-combined-signal-score.d2_four-week-momentum-alone.b1_four-week-momentum-more-coins` (from F1, F2): The higher a coin's 28-day return, the higher its return over the next 5 days.
- `022-01_learned-combined-signal-score.d2_four-week-momentum-alone.b2_four-week-momentum-ten-days` (from F1, F5): The higher a coin's 28-day return, the higher its return over the next 10 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
