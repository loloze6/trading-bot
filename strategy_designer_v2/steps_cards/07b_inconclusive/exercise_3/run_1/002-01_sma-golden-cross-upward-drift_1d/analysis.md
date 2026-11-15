---
line: 7.b inconclusive
backtest: 002-01_sma-golden-cross-upward-drift_1d
idea tested: 002-01_sma-golden-cross-upward-drift
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3331 USD
---
## Findings
- **F1:** The effect is too small to separate from noise at any horizon: the forecast slope's t is 0.20, 0.37, 0.55 and −0.06 at 5, 10, 20 and 40 bars (3349, 1657, 811 and 388 non-overlapping cases), while the 10-bar excess return has a standard deviation of 0.14–0.22 against a mean shift of under 0.011.
- **F2:** The gap between up-state (forecast > 0) and flat bars widens with the horizon but stays below significance: on minus off is 0.0011 at 10 bars (Welch t 0.14), 0.0179 at 20 bars (0.0089 − (−0.0090), t 0.93) and 0.0379 at 40 bars (0.0194 − (−0.0185), t 0.84), so the plan's 10-bar horizon sits where the gap is smallest.
- **F3:** The response to the forecast is not graded. Forecast bins 0–5, 5–10, 10–15 and 15–20 give 10-bar excess means of −0.0085 (n 212), +0.0023 (n 183), +0.0105 (n 174) and +0.0000 (n 263). By raw spread, the widest sextile (n 277) gives −0.0069, while the bin just below zero gives +0.0078 (n 276) and the two middle positive bins give +0.0028 and +0.0046. Moderate spreads drift up and the most stretched spreads fall back.
- **F4:** Fresh crosses go against the brief on both sides. In the first 20 bars after an up-cross, the 10-bar excess return is −0.018 (n 107, t ≈ −1.4). In the first 20 bars after a down-cross it is +0.019 (n 96, t ≈ 1.4), and +0.024 between 20 and 60 bars after (n 100, t ≈ 1.8). Strong rebounds below the 200-day line offset the up-state gain.
- **F5:** The effect splits by coin and by year. On minus off at 10 bars is +0.014 for ETH (t 0.80) and −0.016 for LTC (t −0.90), and it is negative in 6 of 8 years: 2020 gives 0.0088 vs 0.0610 (t −2.56) and 2023 gives −0.0087 vs 0.0185 (t −1.94). The pooled slope therefore averages opposite signs.

## Ideas
- `002-01_sma-golden-cross-upward-drift.b1_golden-cross-multi-week-drift` (from F2, F1): While the 50-day SMA of the close is above the 200-day SMA, the coin's return over the following several weeks is higher than its usual return, by more the wider the spread between the two averages.
- `002-01_sma-golden-cross-upward-drift.b2_stretched-spread-pullback` (from F3, F1): While the 50-day SMA is above the 200-day SMA, the coin's following return falls as the spread between the two averages stretches beyond its usual width, so the widest spreads are followed by a pullback.
- `002-01_sma-golden-cross-upward-drift.b3_death-cross-rebound` (from F4, F5): After the 50-day SMA crosses below the 200-day SMA, the coin rises over the following weeks by more than its usual return, the more so the more recently the cross happened.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
