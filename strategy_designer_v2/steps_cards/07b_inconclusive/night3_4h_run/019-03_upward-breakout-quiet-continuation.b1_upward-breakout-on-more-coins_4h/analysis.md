---
line: 7.b inconclusive
backtest: 019-03_upward-breakout-quiet-continuation.b1_upward-breakout-on-more-coins_4h
idea tested: 019-03_upward-breakout-quiet-continuation.b1_upward-breakout-on-more-coins
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.4127 USD
---
## Findings
- **F1:** The forecast is saturated, so the test could not check the idea's grading. 89 % of the 6,689 cases sit at the cap of 20, and the 25th to 75th percentiles are all 20. The median split therefore put all 6,664 cases in the lower half and none in the upper half.
- **F2:** The main result is on the predicted side but small and unclear. Over 18 bars the unusual move is +0.17 % (t 1.32 on 6,664 cases), and it is no clearer at other horizons: +0.08 % (t 0.86) at 6 bars, +0.06 % (t 0.64) at 12 and +0.27 % (t 1.41) at 36. Fewer than half the cases are up (hit rate 0.46 at 18 bars). No more data is available, because the test already used all 19 coins and all four folds.
- **F3:** The stretch's narrowness, the idea's stated grade, does not grade the move. By narrowness quintile, from widest to narrowest, the 18-bar unusual move is +0.45 %, −0.04 %, +0.36 %, −0.26 % and −0.01 %, every t between −1.0 and 1.4, with about 1,240 cases each.
- **F4:** The size of the breakout does grade the move, and only its largest fifth carries it. The 18-bar unusual move is −0.26 %, −0.10 %, +0.15 % and −0.19 % in the four lower breakout quintiles, and +0.98 % (t 2.21, 1,301 cases) in the top one, where the median close is 3.3 % above the stretch's high.
- **F5:** The result is drowned by the coin's own 30-day trend and swings by year. At the same 30-day return, breakout cases move like the average bar: −0.37 % against −0.34 % in the lowest quintile, +0.82 % against +0.78 % in the fourth, and +0.78 % against +0.66 % in the top. By year the cases run from +1.99 % (t 5.08) in 2020 to −1.02 % (t −3.72) in 2022 and −0.98 % (t −3.78) in 2025.
- **F6:** The breakout adds something of its own only when the coin is rising over 30 days and the breakout is large.
- **F7:** The coin's own 30-day return predicts its next days on every bar, breakout or not.

## Ideas
- `019-03_upward-breakout-quiet-continuation.b1_upward-breakout-on-more-coins.b1_large-breakouts-in-rising-coins` (from F1, F3, F4, F5, F6): When a four-hour bar closes above the highest high of a coin's preceding two-day stretch, the coin rises over the next three days, only while its 30-day return is positive, and the further that close clears the stretch's high, the larger the rise.
- `019-03_upward-breakout-quiet-continuation.b1_upward-breakout-on-more-coins.b2_thirty-day-trend-continues` (from F5, F7): The higher a coin's 30-day return, the more it rises over the next three days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
