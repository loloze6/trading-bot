---
line: 7.b inconclusive
backtest: 002-01_sma-golden-cross-upward-drift_1d
idea tested: 002-01_sma-golden-cross-upward-drift
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3223 USD
---
## Findings
- **F1:** The forecast's slope on excess forward returns is flat at every horizon tried: t is 0.20, 0.37, 0.55 and -0.06 at 5, 10, 20 and 40 days (n = 3349, 1657, 811, 388), and the raw 50/200 spread gives t between -0.76 and 0.02. The plan's 10-day horizon is not hiding an effect that shows at another horizon.
- **F2:** While the 50-day SMA is above the 200-day SMA, the next 10-day excess return splits by the coin's own 20-day return, so the two sides cancel in the pooled slope. In the top tercile of 20-day return it is +0.032 (t 2.22, n 242). In the bottom tercile it is -0.021 (t -2.15, n 225). Below the 200-day average, no tercile reaches |t| 1.2.
- **F3:** The forecast does not grade the move. Excess 10-day return across forecast quartiles runs -0.0094, +0.0049, +0.0060, +0.0006 (n 208 each). The spread within each quartile is 0.15 to 0.22, about 20 times the gaps between quartiles. On-bars against off-bars differ by only +0.0011 (Welch t 0.14, 832 vs 825 blocks).
- **F4:** The effect is mixed across periods. The yearly 10-day slope is significantly negative in 2020 (t -2.22) and 2022 (t -2.42), and lies between -1.13 and 0.14 in every other year. Being above the 200-day average beat being below it in only 2018, 2022 and 2025.
- **F5:** The weeks right after a cross move against it. Days 11-30 after an up-cross give a 10-day excess return of -0.037 (t -2.60, n 89, hit rate 40%). Days 11-30 after a down-cross give +0.042 (t 2.53, n 73, hit rate 62%). The same pattern holds at 20 days (-0.068, t -2.67).
- **F6:** The effect is mixed across coins. Above-minus-below 10-day excess return is positive for BTC, ETH and ZEC (+0.006, +0.014, +0.013) and negative for LTC, XMR and XRP (-0.016, -0.002, -0.009).
- **F7:** The book's small gain is mostly the market's own rise, not timing. The book's mean daily return is 0.000400, of which 0.000348 is the market part (mean position 0.28), leaving 0.000052 for timing.

## Ideas
- `002-01_sma-golden-cross-upward-drift.b1_golden-cross-with-momentum` (from F2, F3, F1): While a coin's 50-day SMA is above its 200-day SMA, its return over the next 10 days is larger the larger its own 20-day return, so the uptrend persists only where price is still climbing and reverses where it has stalled.
- `002-01_sma-golden-cross-upward-drift.b2_early-post-cross-reversal` (from F5, F4): In the two to four weeks after a coin's 50-day SMA crosses its 200-day SMA, the coin's return over the next 10 days runs against the direction of the cross: below its average after an up-cross and above its average after a down-cross.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
