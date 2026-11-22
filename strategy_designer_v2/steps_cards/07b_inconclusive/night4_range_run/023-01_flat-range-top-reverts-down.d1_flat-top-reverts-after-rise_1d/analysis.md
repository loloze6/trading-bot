---
line: 7.b inconclusive
backtest: 023-01_flat-range-top-reverts-down.d1_flat-top-reverts-after-rise_1d
idea tested: 023-01_flat-range-top-reverts-down.d1_flat-top-reverts-after-rise
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3371 USD
---
## Findings
- **F1:** The tested measure came out on the wrong side of the idea. Step 5's mean unusual 5-day move in the short direction is -0.77 % with t -1.85 over 895 cases, and the stronger half does no better than the weaker (difference -0.04 %). The size reading gives -0.21 % per case (-0.020 of a usual 10.60 % move) against a cost of 0.19 % per trade, so prices tended to rise after a flat-range top, not fall.
- **F2:** On the non-overlapping 5-day grid, while the 90-day return is positive (1,313 cases), the unusual 5-day move rises with the flatness-weighted range position (slope +0.021, t 1.96; Spearman +0.065). By range-position quintile it climbs from -2.50 % in the lowest fifth to +1.81 % in the highest. The top fifth minus the bottom fifth is +2.86 % (Welch t 2.57, 263 cases each). That is continuation, the reverse of the reversion the idea predicts.
- **F3:** The same reading is reversion-free outside the rising-coin condition too. With the 90-day return negative (1,242 cases), the 5-day slope is +0.012 (t 1.36), and the 5-day reversion measure on large standardised positions is -0.44 % (t -1.38). There is no part of the data where a high flat-range close is followed by a fall.
- **F4:** Within the rising-coin condition, the continuation sits in months of middling flatness (slope +0.080, t 4.28, 437 cases). It is absent in the flattest third of months (slope -0.005, t -0.43, 438 cases), which is exactly where the brief says reversion should show.
- **F5:** The continuation is not steady over time. In rising coins the 5-day slope is positive with t 2.40 in 2020 and t 2.36 in 2021, but negative in 2023, 2024 and 2025 (t -0.63, -1.06, -0.22). It is positive for 5 of 6 coins, but no single coin reaches t 2 (ETH t 1.50, ZEC t 1.36, LTC t -0.38).
- **F6:** Step 5's cases rose more than the drift in 5 of 6 coins (ZEC +3.06 %, ETH +1.55 %, LTC +1.06 %, BTC +0.90 %, XRP -0.60 %) and in 5 of 8 years. So the wrong-side result is broad rather than driven by one coin, and the book lost accordingly (Sharpe -1.08).

## Ideas
- `023-01_flat-range-top-reverts-down.d1_flat-top-reverts-after-rise.b1_range-top-continues-in-risers` (from F2, F4, F5, F6): In a coin whose 90-day return is positive, the higher its close sits in its 30-day closing range, the more it rises over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
