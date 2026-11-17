---
line: 7.b inconclusive
backtest: 010-02_rsi-below-share-continuation_1d
idea tested: 010-02_rsi-below-share-continuation
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 1
cost: 0.1521 USD
---
## Findings
- **F1:** The main measure is on the side the idea predicts but short of the bar: mean forecast/10 × excess 14-day return 0.0156, t 1.59, on 384 independent grid cases. It is about the same in both coins that ran: BTC 0.0149 (t 1.24, n 192) and ETH 0.0163 (t 1.05, n 192).
- **F2:** The effect is weak and mixed across periods. Five of eight years are positive, the best 2025 at 0.034 (t 1.99, n 48). 2020, 2023 and 2024 are slightly negative (−0.008, −0.010, −0.009), so no single year carries it and none is clear.
- **F3:** It is not one-sided. Long cases give 0.0197 (t 1.33, n 187) and short cases 0.0117 (t 0.90, n 197).
- **F4:** It is not graded the way the idea says. Excess 14-day return by quintile of the raw share below falls from +0.015 and +0.021 (lowest two quintiles) to −0.009 and −0.043 (middle and fourth). It then turns back to +0.019 in the highest quintile (share +0.46, n 67). Likewise the largest |forecast| quartile earns 0.016 (t 0.63), no more than the second quartile's 0.025 (t 1.91).
- **F5:** The same sign holds at every horizon tried. The 3-day result is 0.0042 (t 2.31, n 1907), 7-day 0.0084 (t 1.81, n 815), 21-day 0.0286 (t 1.92, n 240) and 28-day 0.0235 (t 1.22, n 192). Spearman between share and excess return is negative at all of them (−0.02 to −0.10). So the result is a small, consistent continuation effect that is too small for 384 cases to show, not a sign flip.
- **F6:** Only two coins ran (BNB is not in the data), while four more coins with all four folds are available (LTC, XMR, XRP, ZEC). Adding them would roughly triple the independent cases from the 384 the test used.

## Ideas
- `010-02_rsi-below-share-continuation.b1_rsi-below-share-continuation-broader` (from F1, F5, F6): The larger the share of the past 30 days that a coin's 14-day RSI has spent below its midpoint of 50, the lower the coin's return over the next 14 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
