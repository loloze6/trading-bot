---
line: 7.b inconclusive
backtest: 070-01.g1.d2.d1_depth-graded-run-break-fade_1d
idea tested: 070-01.g1.d2.d1_depth-graded-run-break-fade
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3365 USD
---
## Findings
- **F1:** The test missed the bar only because its supporting check could not be computed, not because the effect was weak. The forecast sits at its cap of -20 on 84 % of the 1,048 event bars in folds B and C, so the median of |forecast| is -20 itself. The "strictly above the median" deeper half is therefore empty and the check returned None. Meanwhile the main measure confirms: +0.59 % per case, t 3.54, over 922 days.
- **F2:** Measured on the run's own percent loss rather than on the saturated forecast, the grading the idea predicts is clearly present. The deeper half of runs (per coin) is followed by a +1.99 % short-direction excess next day (t 4.15, 522 cases). The shallower half gets +0.08 % (t 0.32, 526 cases). The difference is +1.91 % with Welch t 5.77, and Spearman between depth and excess is 0.16 (p 1e-7).
- **F3:** The depth quintiles rise toward the deep end: +0.53 %, -0.09 %, +0.54 %, +1.55 % (t 2.88) and +2.64 % (t 3.46), about 210 cases each. Run length grades nothing: 2-day runs give +1.08 %, 3-day +0.80 %, 4-day +0.51 %, 5+ days +2.21 %.
- **F4:** Depth measured in the coin's own 30-day daily swing grades more cleanly still, rising through every quintile:
- **F5:** The effect is present wherever the coin's 60-day return is not rising, and absent where it is rising, as the brief's reasoning expects:
- **F6:** The effect holds across coins and years in folds B and C.

## Ideas
- `070-01.g1.d2.d1.b1_depth-graded-run-break-fade-wider` (from F1, F2, F6): An up day that ends a run of down days is followed by a fall over the next day, and that fall is larger the more the price dropped over the run of down days it ends.
- `070-01.g1.d2.d1.b2_swing-scaled-run-break-fade` (from F1, F2, F3, F4, F5): An up day that ends a run of down days is followed by a fall over the next day, and that fall is larger the more the price dropped over the run of down days it ends, measured against the coin's usual daily swing over the last 30 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
