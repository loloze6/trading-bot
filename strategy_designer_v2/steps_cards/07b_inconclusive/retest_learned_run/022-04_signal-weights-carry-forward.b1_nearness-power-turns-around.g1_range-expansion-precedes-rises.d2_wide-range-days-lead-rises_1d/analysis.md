---
line: 7.b inconclusive
backtest: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d2_wide-range-days-lead-rises_1d
idea tested: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d2_wide-range-days-lead-rises
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3536 USD
---
## Findings
- **F1:** The test's result is zero, not merely short of the bar. The OLS slope of the excess 5-day return on the forecast has t 0.02 over 1370 wide-day grid cases. Across the five forecast quintiles the mean excess return stays flat (+0.58 %, +0.60 %, +1.06 %, +0.54 %, +0.81 %), even though the range ratio climbs from 1.06 to 2.53. So inside wide days, how much wider brings no larger move.
- **F2:** What the data does show is a step between wide and narrow days. Wide-day cases average +0.72 % above drift over 5 days (t 2.29, 1370 cases). Narrow-day cases (forecast 0) average −0.48 % (t −2.04, 2049 cases). The idea and its long-only forecast threw the narrow side away.
- **F3:** Pooling both sides, the graded relation is strongest at 3 days. The slope of the excess return on the range ratio over all grid cases has t 2.15 at 3 days (2592 cases) and t 1.67 at 5 days (2555 cases). Among wide days only, the 3-day slope has t 1.31 and the 5-day slope t −0.36. The test measured the idea at a horizon, and on a side, where the grading is weakest.
- **F4:** The effect is unstable across periods and coins, which also blurs the result. The all-case log-ratio slope at 5 days runs from t −2.57 in 2018 to t +3.36 in 2024 and +2.30 in 2025. Only XRP is individually clear (t 2.78); LTC is negative (t −1.38) and BTC and XMR are near zero.
- **F5:** Where the day closes inside its range adds little. Wide days closing near their high average +1.18 % (t 2.03, 401 cases), against +0.44 % (t 0.83) for wide days closing near their low. But the graded wide-times-close-location term has t of only 0.58 at 5 days and 1.11 at 3 days.

## Ideas
- `022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d2_wide-range-days-lead-rises.b1_range-versus-norm-both-sides` (from F2, F3, F1): The further a coin's daily high-low range exceeds its average range over the past 30 days, the higher that coin's return over the next 3 days above its usual drift, and the further the range falls short of that average, the lower that return.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
