---
line: 7.b inconclusive
backtest: 010-05_rsi-above-share-reversal_1d
idea tested: 010-05_rsi-above-share-reversal
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.2755 USD
---
## Findings
- **F1:** The test's slope is on the opposite side to the idea, and too weak to call. The 14-day slope of coin-demeaned return on the forecast was -0.00101 with t -1.43 on 384 cases. Bars where the forecast was short, meaning RSI was mostly above 50, then gained +0.0132 against the coin's average (n 187). Bars where it was long gained -0.0156 (n 186). That is mild continuation, not the reversal the idea predicts.
- **F2:** The effect is not graded the way the idea needs.
- **F3:** The sign holds at other horizons but never clears the bar except marginally at 3 days. The slope t was -2.10 at 3 days (1,907 cases), -1.66 at 7 days (815), -1.43 at 14 days (384) and -1.54 at 30 days (179). The plan's horizon is not hiding a reversal.
- **F4:** The effect is not steady across periods, coins or sides.
- **F5:** Splitting by recent volatility gives scattered, not clean, pockets.
- **F6:** The book lost money purely through timing. The daily timing gain was -0.00098 for both BTC and ETH, with an average position near zero (-0.013 and -0.015). BNB did not run, so only two of the brief's three coins were tested.

## Ideas
- No ideas: The result runs weakly against the predicted reversal (t -1.43), is not graded by the share, and flips sign across years and volatility regimes (F1–F5). No part of the data shows the reversal clearly enough to narrow the idea to it, and more data on the same idea would only sharpen an effect on the wrong side.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
