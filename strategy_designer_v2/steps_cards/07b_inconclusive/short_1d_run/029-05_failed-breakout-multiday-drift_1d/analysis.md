---
line: 7.b inconclusive
backtest: 029-05_failed-breakout-multiday-drift_1d
idea tested: 029-05_failed-breakout-multiday-drift
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3718 USD
---
## Findings
- **F1:** The tested measure ran against the idea: the short-side unusual 8-bar move was -0.36 % per case with t -0.52 over 539 cases. My own recount of failures (one per 8 days) gives the same picture: from day 2 to day 10, -0.64 % with t -0.99 over 415 failures, and in 56 % of them price closed above both the old high and the breakout's peak within the next 10 days, which is the brief's own failure case of a second, successful break higher.
- **F2:** The effect shows when depth is measured against the coin's 20-day daily volatility. In the deepest third of failures, price fell more than its drift from day 2 to day 10, by +1.94 % on the short side (t 2.01, 139 cases). In the shallowest third it rose instead (-2.96 %, t -2.37, 138 cases), and the middle third sat between them (-0.92 %, t -0.84). The rank correlation of this depth with the day-2-to-10 short move is 0.157 (p 0.0013).
- **F3:** The shares of second breaks fit the same split. Price broke out again within 10 days in 65 % of the shallowest third of volatility-scaled failures, 60 % of the middle third and 42 % of the deepest third. A deep re-entry is the true failure; a shallow one is a pause before a fresh attempt higher.
- **F4:** Raw percent depth grades the move less clearly. The shallow third gave -2.51 % (t -2.33), the middle third +0.49 % and the deep third +0.12 %, with a rank correlation of 0.128 (p 0.009). Scaling by volatility separates the outcomes much better.
- **F5:** The test could not see the grading at all. The forecast was saturated at -20 on 70 % of the failures two days after the bar (median -20), so the deeper half had 0 cases and the supporting check returned None.
- **F6:** Shallow failures that kept rising were concentrated in rising markets. They lost -8.0 % on the short side in 2020 (t -2.61, 24 cases) and -10.7 % in 2021 (t -2.58, 13 cases). Among shallow failures after a 60-day fall, the loss was -6.27 % (t -3.02, 30 cases). The market's own moves at shallow failures drowned the plan's average.
- **F7:** Deep failures did not depend on one coin. Over days 2 to 10, the deep third gained +3.2 % for XRP, +2.2 % for XMR and +1.8 % for ETH, against -2.6 % for LTC and -1.7 % for ZEC (19 to 29 cases each), so the effect is spread across coins but still noisy within each.

## Ideas
- `029-05_failed-breakout-multiday-drift.b1_volatility-scaled-failed-breakout-depth` (from F2, F3, F4, F5, F6, F7): After a close back below the old 20-day high within 3 days of a breakout above it, the coin's decline continues across the following days, and the deeper the re-entry close sits below the old high, measured in units of the coin's 20-day daily volatility, the larger the fall from day 2 to day 10 after the failure.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
