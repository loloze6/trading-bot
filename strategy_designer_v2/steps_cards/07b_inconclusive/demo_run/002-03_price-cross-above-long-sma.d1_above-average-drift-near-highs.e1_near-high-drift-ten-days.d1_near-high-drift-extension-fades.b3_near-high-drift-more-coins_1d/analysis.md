---
line: 7.b inconclusive
backtest: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.d1_near-high-drift-extension-fades.b3_near-high-drift-more-coins_1d
idea tested: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.d1_near-high-drift-extension-fades.b3_near-high-drift-more-coins
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3686 USD
---
## Findings
- **F1:** The tested forecast had the predicted sign but missed the bar: slope +0.00145, t 1.31 on 1547 trending grid cases at 10 days. The reason is that its two parts pull against each other. The 20-day range position alone gives t +3.07 (slope 0.00153). The extension penalty `ext30` gives slope −0.00181, t −2.61, and because `ext30` is negated, that means larger 30-day runs were followed by larger rises, not smaller ones.
- **F2:** The 30-day run continues rather than fades inside the trending regime. The raw 30-day return has slope t +2.29. Mean excess 10-day return rises across its quintiles from −0.031 (lowest) to −0.012, +0.019, +0.032 and +0.022 (highest, mean run +173%). So the "except when extended" clause predicts the wrong way.
- **F3:** The range effect sits mostly in the top fifth of the 20-day range (closes near the 20-day high). Those bars have a mean excess 10-day return of +0.0515 against −0.0051 for the rest, Welch t 3.30, 310 vs 1237 cases. The lower four quintiles are flat (−0.008, −0.009, +0.003, −0.006).
- **F4:** The range effect is skewed but holds up under robustness checks:
- **F5:** The range effect is broad across periods and coins:
- **F6:** The effect belongs to the 10-day horizon and not longer. The range slope t is 3.24 at 5 days and 3.07 at 10 days, but 0.19 at 20 days (757 cases).

## Ideas
- `002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.d1_near-high-drift-extension-fades.b3_near-high-drift-more-coins.b1_near-high-drift-without-fade` (from F1, F2, F3, F4, F5, F6): While a coin's close is above its 200-day average, the higher its close sits in its 20-day close range, the larger its rise over the next 10 days, most of all as its close nears its 20-day high.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
