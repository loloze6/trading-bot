---
line: 7.b inconclusive
backtest: 024-03_uprun-volume-fade-depth-giveback.b1_up-run-fade-more-coins_4h
idea tested: 024-03_uprun-volume-fade-depth-giveback.b1_up-run-fade-more-coins
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4240 USD
---
## Findings
- **F1:** The main measure is on the predicted side but small and unclear: +0.10 % per case over 18 bars (strength 0.011 of a usual 9.29 % move, t 1.18, 12,138 cases). It is no clearer at other horizons: -0.05 % at 6 bars (t -0.60), +0.12 % at 12 bars (t 1.77), +0.04 % at 36 bars (t 0.29). The test already used all 19 coins and all four folds on 4h bars, and the hourly data behind 4h bars ends with 2025, so there is no more 4h data to add.
- **F2:** Run size is graded opposite to the idea. In the case regression the run-gain coefficient on the unflipped drift-adjusted return is +0.0026 (t 5.1). The smallest run-gain quintile gives back +0.75 % (t 4.6). The largest gains another 0.65 % instead (short-direction mean -0.65 %, t -2.73, about 2,430 cases each). So the largest runs continue rather than fade.
- **F3:** The give-back shows only when the coin's 30-day return is negative.
- **F4:** The volume-fade grading has the predicted sign but shows clearly only where runs are largest.

## Ideas
- `024-03_uprun-volume-fade-depth-giveback.b1_up-run-fade-more-coins.b1_fading-rally-in-downtrend` (from F3, F4, F1): After an unbroken streak of rising four-hour periods whose gain is large relative to the coin's typical four-hour move over the past 30 days, the coin falls over the next three days, only while the coin's own 30-day return is negative. The more the volume declined from the start of the streak to its end, the larger the fall.
- `024-03_uprun-volume-fade-depth-giveback.b1_up-run-fade-more-coins.b2_large-up-streaks-continue` (from F2): After an unbroken streak of rising four-hour periods, the coin keeps rising over the next three days. The larger the streak's gain relative to the coin's typical four-hour move over the past 30 days, the larger the further rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
