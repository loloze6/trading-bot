---
line: 7.d not profitable
backtest: 029-03_close-below-breakout-bar-low.a1_failed-breakout-all-coins_1d
idea tested: 029-03_close-below-breakout-bar-low.a1_failed-breakout-all-coins
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4106 USD
---
## Findings
- **F1:** The book barely earns. Its mean daily return is 0.000027 against 0.0015 for holding the coins, and it is in a position on only 2.0 % of coin-days. Its 205 trades lose 2.39 % each on average (median −1.35 %, 33 % winners, t −1.86), so the losses are far larger than the 0.22 % cost of a trade.
- **F2:** Recomputed from prices on every failure bar (one per 5-day grid cell), closes under the breakout day's low within 3 days give 294 cases. Their mean short-signed unusual 5-day move is −0.92 % (t −1.32) and the total is −1.74 %, so the coin rises after them. Step 5's +1.33 % on 113 cases comes only from the bars where its bet rule fired.
- **F3:** The broader failure, a close back below the old 20-day high, gives 715 to 1384 cases with fail windows of 3, 5 and 10 days. It is followed by a coin that rises more than its drift: unusual −1.41 % (t −2.17), −1.22 % (t −2.29) and −1.06 % (t −2.72). A short on a failed breakout loses in the pooled data.
- **F4:** The coin's own 20-day return at the failure splits the result.
- **F5:** The losses gather in the strong-rally years.
- **F6:** Depth under the breakout low does not grade the move.
- **F7:** The situation is rare: 0.3 % to 1.3 % of bars per coin, and AVAX and ONDO never traded. Widening the fail window to 10 days or using the old high triples to quintuples the cases (827 to 1384), but only in the situations of F3, which follow with a rise.

## Ideas
- `029-03_close-below-breakout-bar-low.a1_failed-breakout-all-coins.d1_failed-breakout-without-rally` (from F2, F4, F5, F6): When a failed breakout above the prior 20-day high ends with a daily close below the low of the breakout day, the coin falls over the next 5 days, only while its 20-day return before that close is small; the smaller that 20-day return, the larger the fall.
- `029-03_close-below-breakout-bar-low.a1_failed-breakout-all-coins.d2_rally-failure-resumes-upward` (from F3, F4, F5, F7): When a coin whose 20-day return is large closes back below a 20-day high it broke within the last 10 days, it rises over the next 5 days, and the larger that 20-day return, the larger the rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
