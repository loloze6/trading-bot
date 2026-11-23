---
line: 7.b inconclusive
backtest: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d1_nearness-power-reversal-long-side_1d
idea tested: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d1_nearness-power-reversal-long-side
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3575 USD
---
## Findings
- **F1:** The main measure is on the side the idea predicts but short of the bar: the mean excess 5-day return on positive-forecast grid bars is +0.37 % with t 1.72 over 2457 cases, and the positive-forecast cases beat the flat cases (excess −0.40 %, t −1.74, 2275 cases) by a Welch t of 2.45.
- **F2:** The effect is weak and spread thinly rather than concentrated in one part of the data. 12 of 15 coins have a positive mean excess, but none has a t above 1.24 (LTC +0.77 %, t 1.24; XRP +0.88 %, t 1.00). Only 50 % of the 24 windows have a positive mean.
- **F3:** The effect changes sign across years rather than holding in one regime. It is positive in 2020 (+1.35 %, t 1.92), 2021 (+1.76 %, t 1.91) and 2024 (+0.91 %, t 2.17), and negative in 2018 (−1.84 %, t −1.63) and 2022 (−1.32 %, t −2.07). The market's own moves drown it out.
- **F4:** The grading holds only loosely, so the strongest forecasts do not isolate a clearer effect. The lowest quarter of positive forecasts earns −0.11 % (t −0.26), q2 +0.67 %, q3 +0.17 % and the top quarter +0.76 % (t 1.72). The larger-minus-smaller-half check is +0.19 %.
- **F5:** A longer horizon does not make the result clearer once it is measured on its own non-overlapping grid:
- **F6:** Measured as the workflow sizes an idea (new rises of the forecast only), the move is mostly the coin's drift:

## Ideas
- `022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d1_nearness-power-reversal-long-side.b1_nearness-reversal-all-coins` (from F1, F2, F4): For a coin's nearness to its 90-day high, the higher that signal's predictive power for the coin's 5-day returns over the past 365 days, the lower the same signal's predictive power over the following 90 days. The turn shows on the rising side: the more strongly this reversal points up, the higher the coin's return over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
