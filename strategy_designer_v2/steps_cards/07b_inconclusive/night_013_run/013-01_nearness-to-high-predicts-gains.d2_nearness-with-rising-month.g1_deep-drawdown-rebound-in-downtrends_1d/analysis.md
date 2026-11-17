---
line: 7.b inconclusive
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends_1d
idea tested: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3466 USD
---
## Findings
- **F1:** The test's main measure is on neither side: on the 1226 regime grid cases the slope of the 7-day excess return on the forecast is -0.00028 (t -0.37), and it stays near zero at 1, 3 and 7 days (t -0.03, -0.33, -0.37). The top third by forecast has a mean excess of -0.0013 and fails the supporting check.
- **F2:** The forecast is not the idea's depth. It is standardised against its own past 60 values, so it correlates only 0.35 with the plain percent distance below the 60-day high. On that plain distance, the regime slope at 7 days is positive (0.060, t 2.41, 829 cases with data), and so is the 1-day slope (t 3.20).
- **F3:** The plain-depth effect is weak and rests on a few extreme cases, so it is not clear either:
- **F4:** Depth cannot be told apart from the 30-day fall itself:
- **F5:** The effect depends on the period and the coin:

## Ideas
- No ideas: The tested forecast shows no relation (t -0.37). The plain-depth effect it missed is driven by outliers and by 2018, is not graded across depth, and cannot be separated from the 30-day fall, so no part of the data shows the idea clearly enough to amend it to.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
