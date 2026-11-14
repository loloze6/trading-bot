---
line: 7.d not profitable
backtest: 002-01_sma-golden-cross-upward-drift_1d
idea tested: 002-01_sma-golden-cross-upward-drift
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3202 USD
---
## Findings
- **F1:** The book falls short of holding on both failed measures: its daily Sharpe is 0.376 against holding's 0.570, its mean daily return is 0.00074 against 0.00121, and its deepest fall is -93.1% against holding's -79.97%, which leaves a Calmar of 0.001.
- **F2:** The size of the forecast does not grade what follows: the mean excess 10-bar return across forecast buckets (0-5, 5-10, 10-15, 15-20) is -0.85%, +0.23%, +1.05% and +0.004% (n = 212, 183, 174, 263), the step-5 slope has t = 0.37 over 832 active blocks, and the raw-spread quartiles show no rising pattern either (+0.14%, +1.30%, -0.53%, -0.70%).
- **F3:** On the book's invested days, the coin's own 20-bar return sorts the gain: in the lowest r20 quartile the position earns a mean of -0.00139 per day and carries -24% of the total gain, while in the highest quartile it earns +0.00495 per day and carries 86% of it (next-day coin return t = 2.77, n = 1132).
- **F4:** The same sort holds on non-overlapping 10-bar blocks while the forecast is positive: blocks whose 20-bar return is in the lowest quartile have a mean excess 10-bar return of -2.94% (t = -2.73, 174 blocks), and those in the highest quartile have +3.39% (t = 1.83, 174 blocks).
- **F5:** The losing state is a spread that is still widening while price has already turned down over 20 bars: on invested days in that state the next-day coin return averages -0.245% (n = 885) and the state carries -33% of the book's gain, while the r20-positive states earn +0.40% and +0.32% per day (t = 2.38 and 2.49).
- **F6:** The book's deepest falls sit in that state: across windows w12, w13, w16 and w18 (book -23%, -55%, -35% and -60%), invested days with a falling 20-bar return and a widening spread average -1.45% per day (t = -2.13, n = 168), and 12.5% of those days drop more than 8%.
- **F7:** Distance from the recent high sorts the gain in the same way: on invested days, when the close is within the top quartile of closeness to its 60-bar high, the next-day return averages +0.48% (t = 3.17) and carries 72% of the gain, while the quartile farthest below the high averages -0.10% and has 6.5% of its days below -8%.
- **F8:** The result rests on one window: w11 alone returns +405% for the book against +281% for holding, while most other windows lose or stay near flat even when holding gains (w16 -35% against +36%; w23 +0.4% against +32%).

## Ideas
- `002-01_sma-golden-cross-upward-drift.d1_golden-cross-with-live-momentum` (from F2, F3, F4, F5, F6, F8): While the 50-day SMA is above the 200-day SMA, the coin keeps drifting upward, and the drift is larger the stronger the coin's own return over the last several weeks, only while that recent return is positive.
- `002-01_sma-golden-cross-upward-drift.d2_uptrend-near-recent-highs` (from F1, F5, F6, F7): While the 50-day SMA is above the 200-day SMA, the coin keeps rising, and the rise is larger the closer its close sits to its recent high, only while price trades near that high rather than deep below it.
- `002-01_sma-golden-cross-upward-drift.d3_recent-momentum-carries-forward` (from F2, F3, F4): (new idea) In a coin's own bars, the forward drift over the next days is graded by the coin's recent return: the stronger the gain over the last several weeks, the further price continues upward.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
