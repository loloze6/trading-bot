---
line: 7.b inconclusive
backtest: 029-01_failed-breakout-depth-decline.d1_thin-volume-failed-breakout-falls_1d
idea tested: 029-01_failed-breakout-depth-decline.d1_thin-volume-failed-breakout-falls
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3270 USD
---
## Findings
- **F1:** The tested result points the way the idea predicts but is too small for this data: over the backtest's 221 cases the short-direction unusual 5-day move is +0.69 % (t 1.06, strength 0.083), and my rebuild of the same cases gives +0.85 % (t 1.33, 220 cases). Reaching t 2 at this effect size needs about 3.6 times as many cases.
- **F2:** The graded check could not run, because the forecast is pinned at its limit. 209 of the 220 cases sit at exactly -20, which left 0 cases in the larger half and all 221 in the smaller. The raw thinness value itself does grade the move: Spearman rho 0.138 (p 0.041, 220 cases), and the upper half minus the lower half is +1.75 % (t 1.38, 110 vs 110).
- **F3:** The effect sits in the thinner failures. By tercile of raw thinness, the thinnest-volume failed breakouts move +1.76 % (t 1.60, 74 cases), the middle +1.84 % (t 1.73, 73 cases) and the least thin -1.07 % (t -0.95, 73 cases).
- **F4:** Across all failed breakouts, the volume condition separates the two sides. Thin-volume failures move +0.40 % in the short direction (200 cases) and heavy-volume failures -1.07 % (t -1.69, 305 cases), a thin-minus-heavy difference of +1.47 % (t 1.61). Without the volume condition, all failures together move -0.49 % (t -1.05, 505 cases).
- **F5:** The market's own moves drown the effect in strong-trend years, and it is uneven across coins.
- **F6:** The move builds over days rather than on the next day, as the brief says. The short-direction unusual move is -0.07 % over 1 day (t -0.22), +0.85 % over 5 days and +1.59 % over 10 days (t 1.47, 210 cases).

## Ideas
- `029-01_failed-breakout-depth-decline.d1_thin-volume-failed-breakout-falls.b1_thin-failed-breakout-more-coins` (from F1, F2, F3, F4, F5): When a coin's daily close moves above its prior 20-day high and then, within the next 3 days, closes back below that old high, the coin falls over the next 5 days, only while the breakout day's volume was below its 20-day average, and the lower that volume against its average, the larger the fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
