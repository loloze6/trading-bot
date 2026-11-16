---
line: 7.b inconclusive
backtest: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.g1_one-day-move-reversal.g1_high-volatility-fall-rebound_1d
idea tested: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.g1_one-day-move-reversal.g1_high-volatility-fall-rebound
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 1
cost: 3.7694 USD
---
## Findings
- **F1:** Step 5's main measure is clearly on the predicted side: the next-day return minus the coin's mean, regressed on the forecast over 3447 regime bars, has a slope of 0.0011 with t 5.89. The result is inconclusive only because the supporting check failed: the slope where the volatility percentile is at least 0.9 is 0.00043 smaller than where it is between 0.8 and 0.9 (636 vs 242 bars).
- **F2:** Across the full volatility range, the rebound does grow with volatility. On all bars, with the percentile recomputed from prices, the slope of the next-day return on the vol-scaled fall rises steadily: 0.0006 (t 0.51) at a percentile of 0.2 or below, 0.0025 (t 1.68) at 0.2–0.4, 0.0031 (t 1.97) at 0.4–0.6, 0.0142 (t 6.26) at 0.6–0.8 and 0.0203 (t 2.91) at 0.8–0.9. Only the thin top bin dips, to 0.0163 (t 1.64, n 42). The gradient lives across the whole range, not inside the top fifth the check compared.
- **F3:** The effect is broad over coins and periods, though uneven. The regime slope is positive for all six coins (t from 1.66 for LTC to 2.72 for ETH) and in all eight years, but near zero in 2019 (t 0.11), 2021 (t 0.42) and 2025 (t 0.51).
- **F4:** Inside the regime, the gain sits in the largest falls. The top forecast quintile (mean forecast 16.3) is followed by a next-day excess return of +1.70% (t 4.25, n 204). The middle three quintiles are near zero (−0.03% to +0.16%, t at most 0.35).
- **F5:** The same rebound shows without any regime. Over all bars, the most-negative decile of the vol-scaled one-day return (mean −1.82 usual moves) is followed by a next-day excess of +0.54% (t 3.35, n 1119). Outside the regime, the fall slope is still positive (t 2.19, n 9101).

## Ideas
- `002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.g1_one-day-move-reversal.g1_high-volatility-fall-rebound.b1_vol-graded-fall-rebound` (from F1, F2, F3, F5): The larger a coin's one-day fall relative to its usual daily move over the past 20 days, the larger its rise over the next day, and the higher the coin's 20-day volatility ranks against its own past 100 days, the stronger that rebound.
- `002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.g1_one-day-move-reversal.g1_high-volatility-fall-rebound.b2_extreme-fall-rebound-turbulent` (from F1, F4): When a coin's 20-day volatility is high compared with its own past levels, the larger its one-day fall relative to its usual daily move over the past 20 days, the larger its rise over the next day, growing fastest among its largest falls.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
