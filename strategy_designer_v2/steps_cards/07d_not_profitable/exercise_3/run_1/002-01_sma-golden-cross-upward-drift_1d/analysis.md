---
line: 7.d not profitable
backtest: 002-01_sma-golden-cross-upward-drift_1d
idea tested: 002-01_sma-golden-cross-upward-drift
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3363 USD
---
## Findings
- **F1:** While the short SMA is above the long one, the 10-bar excess return depends on the coin's recent 20-bar return, not on the spread. When that return is negative the mean excess is -0.0171 (t -2.26, n 333), and when it is positive it is +0.0221 (t 2.07, n 361). Across the 20-bar return quartiles the excess rises steadily, from -0.029 (t -2.73) through -0.001 and +0.010 to +0.034 (t 1.83).
- **F2:** The spread size that sets the forecast does not grade what follows. Its active quartiles give 10-bar excesses of +0.001, +0.013, -0.005 and -0.007, with no |t| above 1.04, which is why the main slope's t is 0.37.
- **F3:** The book's deepest falls come while it is long in a golden-cross state but the coin is falling. On active bars inside book drawdowns deeper than 15%, 71% have a negative 20-bar return, against 49% of all active bars. Their median 20-bar return is -0.089 against +0.004, and their median distance below the 30-bar high is -0.199 against -0.102.
- **F4:** How close price sits to its recent high grades the gain the same way. In the active state, bars at the 30-bar high are followed by a 10-bar excess of +0.041 (t 2.37). Bars in the deepest quartile below it (median -0.28) are followed by -0.022 (t -2.03).
- **F5:** Scaling the position by a positive 20-bar return lifts the proxy coin-averaged book on all its fall measures but not its mean. Calmar rises from 0.39 to 0.57, the deepest fall shrinks from -0.41 to -0.21, and Sharpe rises from 0.71 to 0.81 (holding 0.64). The mean daily gain drops from 0.000501 to 0.000347.
- **F6:** In the active state the daily book earns 0.001234 when the 20-bar return is up and 0.000443 when it is down. The coin itself earns 0.00335 against 0.00049 in those two states.
- **F7:** The 20-bar return carries no such effect while the short SMA is below the long one. There, its lowest quartile is followed by an excess of +0.010 (t 0.97) and its highest by -0.003 (t -0.29), so the effect belongs to the golden-cross regime.
- **F8:** The mean daily gain is starved by small positions. The lowest forecast bucket (0-5) holds a mean allocation of 0.13 and earns -0.000011 a day while the coin earns 0.000909. The 8453 flat days earn about zero while the coin earns 0.0013.

## Ideas
- `002-01_sma-golden-cross-upward-drift.d1_golden-cross-with-rising-momentum` (from F1, F3, F4, F5, F6, F7): While the short moving average of the close is above the long one, price keeps drifting upward, but only while the coin's own recent return is positive. The drift is larger the stronger that recent rise and the closer price stands to its recent high, and it turns into a decline when the coin has been falling inside the golden-cross state.
- `002-01_sma-golden-cross-upward-drift.d2_nearness-to-recent-high` (from F2, F4, F8): (new idea) In one coin, the closer the close stands to its recent high, the larger its rise over the following days; the further below that high it stands, the more it keeps falling.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
