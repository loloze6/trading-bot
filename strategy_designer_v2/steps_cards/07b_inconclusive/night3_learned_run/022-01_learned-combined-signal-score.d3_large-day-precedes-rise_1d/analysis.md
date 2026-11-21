---
line: 7.b inconclusive
backtest: 022-01_learned-combined-signal-score.d3_large-day-precedes-rise_1d
idea tested: 022-01_learned-combined-signal-score.d3_large-day-precedes-rise
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3226 USD
---
## Findings
- **F1:** The effect is on the predicted side but short of the bar. Over 5 days the top third of forecasts beats the bottom third by 0.77 % (Welch t 1.64, 1139 cases each, 3419 grid cases). The same grading is clearer on shorter horizons: over 1 day the gap is 0.36 % (t 3.93, 17380 cases) and over 2 days it is 0.52 % (t 2.88, 8650 cases). Over 10 and 20 days the gap is larger, 1.28 % and 1.83 %, but less certain (t 1.38 and 1.00, 1691 and 827 cases).
- **F2:** The effect varies across coins and is partly carried by ZEC. Over 5 days the gap is 3.24 % (t 2.43) on ZEC, 1.21 % on ETH, 0.70 % on BTC and 0.60 % on XRP. It is negative on LTC (-0.83 %) and XMR (-0.12 %). Without ZEC the pooled gap falls to 0.67 % (t 1.38, 2729 cases).
- **F3:** The effect varies over time. The gap is negative in 2018 to 2020 (-1.28 %, -0.89 %, -0.12 %) and positive in every year from 2021 to 2025 (+0.96 % to +2.22 %, t up to 1.97 in 2024). No single year clears t 2, so the effect is present in later periods but the data per year is thin.
- **F4:** The two sides of the idea differ.
- **F5:** The size of the move is large enough against cost only in the strongest cases.
- **F6:** The grading holds on both sides separately at 5 days. Within up days, the slope of the 5-day excess return on the size of the move is +0.0022 per forecast point (t 2.51, 1557 cases). Within down days it is +0.0020 (t 2.55, 1718 cases). The test's one-sided thirds split diluted this, because the bottom third was mostly near-still days whose returns are noisy.

## Ideas
- `022-01_learned-combined-signal-score.d3_large-day-precedes-rise.b1_large-day-more-coins` (from F1, F2, F3, F6): The larger a coin's absolute return over its last day, the higher its return over the next 5 days.
- `022-01_learned-combined-signal-score.d3_large-day-precedes-rise.b2_large-up-day-continues` (from F4, F5, F6): The larger a coin's rise over its last day, the higher its return over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
