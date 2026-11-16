---
line: 7.d not profitable
backtest: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e2_short-drift-after-strong-highs_1d
idea tested: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e2_short-drift-after-strong-highs
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3422 USD
---
## Findings
- **F1:** The book's mean daily return is 0.000479, against 0.00118 for holding the coins. The book is in a position on only 33.8 % of bars, at a mean allocation of 0.53 when in. Its gain before fees is 0.000546 per bar, against fees of 0.000067 per bar, so fees are not what keeps the mean daily return below 0.0005.
- **F2:** Nearly all the gain comes from closes at the very top of the 20-day range. In the top forecast quintile (forecast 17.1) the next-day return is 0.00506 and the gain 0.00529, from 1043 bars. Quintiles 2 to 3 (forecast 7.9 to 11.6) earn only 0.00034 to 0.00070 at allocations of 0.41 to 0.63, and the next-day return there (0.0013 and 0.0006) is below the coin's all-window mean of 0.00119.
- **F3:** The deepest fall is -25.4 %, running from w4 to w10 over 782 days. In those windows the active bars earned 0.00088 against 0.00217 elsewhere, and the next-day return was 0.00076 against 0.00303, while allocation was higher (0.73 against 0.54). Middle-tercile forecasts in those windows lost money: next-day return -0.00051, gain -0.00015, from 494 bars.
- **F4:** Active bars that move further toward the high over 5 days are followed by larger rises. The 5-day return quintiles from -4.6 % to +24 % carry next-day returns rising from 0.00063 to 0.00450 and gains from 0.00052 to 0.00355, about 1000 bars each.
- **F5:** Relative to the coin's own volatility, the follow-through is strongest in calm markets. In the lowest 20-day volatility quintile (2.05 % daily) the next-day return is 0.0019, about 0.093 of a day's volatility, and the gain is 0.00325. In the highest quintile (8.5 % daily) it is 0.0041, about 0.048 of a day's volatility, and the gain is only 0.0011.
- **F6:** How long the coin has been above its 200-day average matters. Bars about 24 days into the trending regime show a next-day return of -0.00003 and a gain of -0.0006 (1040 bars). Bars about 86 days in show 0.0051 and 0.0040 (1018 bars).

## Ideas
- `002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e2_short-drift-after-strong-highs.d1_push-to-the-high` (from F1, F2, F4): While a coin's close is above its 200-day average, the stronger its rise toward its 20-day high, the larger its rise over the next 5 days. The effect concentrates on closes pressed against the 20-day high after a large 5-day gain, with the rise growing with that 5-day gain.
- `002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e2_short-drift-after-strong-highs.d2_calm-breakouts-follow-through` (from F5, F3): While a coin's close is above its 200-day average, the stronger its rise toward its 20-day high, the larger its rise over the next 5 days. Measured against the coin's own 20-day volatility, the rise is larger the calmer the coin's past 20 days have been.
- `002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e2_short-drift-after-strong-highs.d3_established-uptrend-near-highs` (from F3, F6): While a coin's close is above its 200-day average, the stronger its rise toward its 20-day high, the larger its rise over the next 5 days. The rise is larger the longer the close has stayed above its 200-day average, counted in days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
