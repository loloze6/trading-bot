---
line: 7.d not profitable
backtest: 002-03_price-cross-above-long-sma_1d
idea tested: 002-03_price-cross-above-long-sma
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3646 USD
---
## Findings
- **F1:** The book loses on the days it holds a coin above a flat or falling 200-day SMA. Held days with the SMA's 20-day slope between -5% and 0 averaged -0.000144 (n=1460, t -0.13), and slope at or below -5% averaged 0.000556 (n=172, t 0.27). With a rising SMA the held days averaged 0.001715 (n=3655, t 2.04) for slope 0 to 5% and 0.004502 (n=2300, t 2.69) for 5 to 15%.
- **F2:** On non-overlapping 20-bar blocks, active bars with a non-positive SMA slope had a 20-bar excess return of -0.033 (n=64, t -1.46). Active bars with a positive slope had +0.034, +0.019 and +0.014 across the three slope bands (n=139, 100, 27). On daily bars, keeping only the positive-slope days raised the Sharpe from 0.394 to 0.509, level with holding at 0.509.
- **F3:** Held days after a non-positive 60-day return lost -0.000623 a day (n=1473, t -2.35). Held days after a positive 60-day return gained 0.001948, 0.003423 and 0.010923 across rising bands of that return (n=1698, 1499, 397).
- **F4:** The book's worst 5% of held days came at large positions far above the average: mean allocation 1.76 against 0.93 over all held days, and mean distance 89% against 31%. In the 20-bar blocks the furthest-above distance quintile returned -0.020 excess (t -0.62), while the 29 to 54% quintile returned +0.038 (t 1.24).
- **F5:** Fresh crosses do not pay. Blocks within 20 days of the forecast turning on returned -0.021 excess (n=162, t -1.21), and the lowest forecast bin (0 to 5) returned -0.029 (n=111, t -1.63).
- **F6:** The falls sit in a few windows. The book lost -0.33, -0.39 and -0.48 in w12, w13 and w18 against the coins' -0.15, -0.31 and -0.24, while w24 (4.37) and w11 (2.06) carry the gain. XMR's book Sharpe was -0.02 against 0.48 for holding it, with a deepest fall of -0.96.

## Ideas
- `002-03_price-cross-above-long-sma.d1_cross-with-rising-average` (from F1, F2, F6): While a coin's close is above its long moving average, it keeps drifting upward further the further it sits above, only while the long moving average itself is rising, and the drift grows with the steepness of that rise.
- `002-03_price-cross-above-long-sma.d2_cross-confirmed-by-momentum` (from F3, F5): While a coin's close is above its long moving average, it keeps drifting upward further the further it sits above, only while the coin's own return over the past few months is positive, and the drift grows with that return.
- `002-03_price-cross-above-long-sma.d3_extended-distance-fades-drift` (from F4, F6): While a coin's close is above its long moving average, it keeps drifting upward further the further it sits above, except when the close is stretched very far above, where the upward drift weakens as the stretch grows.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
