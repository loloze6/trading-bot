---
line: 7.b inconclusive
backtest: 006-04_upside-squeeze-break-continuation.b1_wide-range-breakout-continuation_1d
idea tested: 006-04_upside-squeeze-break-continuation.b1_wide-range-breakout-continuation
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3171 USD
---
## Findings
- **F1:** Step 5's main measure is on the predicted side but close to zero. Across 404 non-overlapping breakout cases, the slope t of the 10-day excess return on the width forecast is 0.39. The top third beats the bottom third by only 0.0093 (Welch t 0.36), against a case-level standard deviation of 0.215 in the 10-day excess return.
- **F2:** The width effect changes sign across periods rather than sitting in one part of the data. The yearly slope t is −3.12 in 2021 (n 65), +1.72 in 2019 (n 44), +1.71 in 2024 (n 54) and +1.89 in 2025 (n 44), and it lies between −1.2 and −0.2 in 2018, 2020, 2022 and 2023.
- **F3:** The effect is not monotonic in forecast size. Mean 10-day excess return by forecast quintile, lowest to highest, is 0.008, 0.015, 0.058, 0.003 and 0.031. The middle quintile is best and the fourth is worst.
- **F4:** The sign depends on the horizon. The slope t is −1.49 at 3 days, −1.31 at 5 days, +0.39 at the plan's 10 days and +1.28 at 20 days (n 369). The raw width ratio behaves the same way (t −1.22, −1.23, +0.75, +1.45), so any positive width effect shows only at longer horizons.
- **F5:** No coin carries the effect. Per-coin slope t at 10 days ranges from −0.84 (LTC, n 70) to +0.79 (BTC, n 75), on 49 to 75 cases per coin.
- **F6:** Breakouts as a whole are followed by gains beyond holding, whatever the width. The mean 10-day excess return is +0.023 (t 2.14, n 404).
- **F7:** That gain is concentrated where the last 5 days' volume is above its 60-day level. In that half the mean excess return is +0.050 at 10 days (t 2.55, n 157) and +0.091 at 20 days (t 2.75, n 138). In the low-volume half it is +0.017 (t 1.10) and −0.002 (t −0.13). Width has no slope inside either half (t 0.12 and −0.04 at 10 days).

## Ideas
- `006-04_upside-squeeze-break-continuation.b1_wide-range-breakout-continuation.b1_wide-range-breakout-more-coins` (from F1, F5): When a coin closes above the high of its prior 20 days, the wider its 20-day range was against its 100-day range, the further price rises over the next 10 days.
- `006-04_upside-squeeze-break-continuation.b1_wide-range-breakout-continuation.b2_volume-backed-breakout-continuation` (from F6, F7): When a coin closes above the high of its prior 20 days, the higher its last 5 days' volume against its 60-day average volume, the further price rises over the next 20 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
