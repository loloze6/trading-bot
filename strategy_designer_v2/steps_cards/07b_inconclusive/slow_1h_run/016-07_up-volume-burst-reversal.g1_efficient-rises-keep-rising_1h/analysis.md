---
line: 7.b inconclusive
backtest: 016-07_up-volume-burst-reversal.g1_efficient-rises-keep-rising_1h
idea tested: 016-07_up-volume-burst-reversal.g1_efficient-rises-keep-rising
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3358 USD
---
## Findings
- **F1:** The test's forecast standardises the efficiency ratio against its own past 72 hourly values, and this standardisation is what loses the effect. Among 2139 non-overlapping 3-day rises, the 72-hour excess return regressed on the raw ratio has slope t 2.49, on the standardised ratio only t 0.60, and the two correlate at just 0.31.
- **F2:** Measured in the idea's own terms (the raw share of hourly movement in the rise's direction), the effect is on the predicted side and graded. Mean excess 72-hour return across raw-ratio quintiles of rises runs -0.0033, -0.0037, +0.0030, +0.0069, +0.0092 (about 443 cases each), with slope t 2.71 on 2217 cases.
- **F3:** The test's main measure is on the predicted side but short of the bar. The forecast slope is +0.000365 with t 1.19 on 2254 cases. The forecast-weighted mean excess is +0.0038. The lowest forecast quintile alone is negative (-0.0032), and the other four are flat between +0.0001 and +0.0058.
- **F4:** The effect grows with the horizon. The forecast's slope t is -0.41 at 24 hours, 1.19 at 72 hours and 1.23 at 120 hours. The raw ratio's slope t is 0.67, 2.71 and 3.03 at the same horizons. A 5-day horizon shows it more clearly than the plan's 3 days.
- **F5:** The effect is spread thinly rather than concentrated. The raw-ratio slope is positive in all 6 coins (t from 0.01 for ETH to 2.39 for LTC) and in all 8 years (t from 0.00 in 2022 to 2.24 in 2024). The forecast slope is positive in 5 of 6 coins and 7 of 8 years, with none reaching t 2. Each subset of 350 to 390 cases is too small to show it alone.
- **F6:** The share adds only partly beyond the rise's size. With both in one regression, the raw ratio has t 1.61 and the 3-day return t 0.66. Inside size terciles, the raw-ratio slope t is 0.79, 2.39 and 0.36. The rise's size alone gives t 1.97 at 72 hours and 3.65 at 120 hours.
- **F7:** The book lost money: Sharpe -0.72, mean daily return -0.00046, Calmar -0.22, with 3.15 trades per day. The hourly rebalancing on a standardised forecast is costly next to a gain that is small and builds over several days.

## Ideas
- `016-07_up-volume-burst-reversal.g1_efficient-rises-keep-rising.b1_efficient-rises-more-coins` (from F3, F5): When a coin has risen over the past 2 to 3 days, the more of its hourly movement over that period went in the direction of the rise (net move relative to the sum of absolute hourly moves), the more it rises over the next 3 days.
- `016-07_up-volume-burst-reversal.g1_efficient-rises-keep-rising.b2_smooth-rises-keep-rising` (from F1, F2, F4): When a coin has risen over the past 3 days, the larger the share of its hourly movement over those 3 days that went in the direction of the rise (net 3-day move over the sum of absolute hourly moves), the more it rises over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
