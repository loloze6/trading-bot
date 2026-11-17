---
line: 7.d not profitable
backtest: 010-05_rsi-above-share-reversal_1d
idea tested: 010-05_rsi-above-share-reversal
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.2890 USD
---
## Findings
- **F1:** The book loses on its shorts, not on fees. Short bar-days earned a mean -0.001703 a day over 2826 days, while the coin rose +0.002623 the next day on those same days. Long bar-days earned -0.000345 over 2800 days. Short trades averaged -9.78% net (646 trades) against +0.21% net for long trades (601 trades). Fees cost only 0.0000338 of the book a day.
- **F2:** The losses sit where the coin had risen over the past 30 days. There the book was short on 1775 bar-days and lost -0.002498 a day while the coin gained +0.003101 a day. Where the 30-day return was negative, shorts gained +0.000490 over 388 bar-days.
- **F3:** Sorted by 90-day trend, the book was most short in the rising tercile (mean position -0.73) and lost -0.001914 a day there. In the falling tercile it was net long (mean position +0.47) and earned +0.000961 a day. The coin's next-day return was +0.001707 in the rising tercile and +0.002393 in the falling one.
- **F4:** On the non-overlapping 14-day grid, the RSI-above-50 share does not predict reversal overall: slope +0.005, t 0.15, n 192. Its sign splits by trend. Where the 30-day return was positive the slope was +0.079 (t 1.33, n 109), meaning continuation. Where the 30-day return was non-positive it was -0.102 (t -1.42, n 83), meaning reversal. In the rising 90-day tercile the slope was +0.256 (t 2.43, n 18).
- **F5:** The share quartiles are not monotone against the next 14 days' demeaned return: +0.040, -0.057, -0.001, +0.021 from the lowest share to the highest. The most persistent above-50 stretches (mean share 0.96) were followed by gains, not falls.
- **F6:** Zeroing the shorts taken after a positive 30-day return lifts the daily book from mean -0.001202 (Sharpe -0.96) to -0.000193 (Sharpe -0.22). The book is still below zero, so removing the shorts in rises closes most of the gap but does not by itself make it pay.

## Ideas
- `010-05_rsi-above-share-reversal.d1_rsi-share-reversal-in-downtrends` (from F2, F3, F4, F6): The larger the share of the past 30 days that a coin's 14-day RSI has spent above 50, the lower the coin's return over the next 14 days, only while the coin's 90-day return is negative.
- `010-05_rsi-above-share-reversal.d2_rsi-dominance-continues-in-uptrends` (from F1, F2, F4, F5): In a coin whose 30-day return is positive, the larger the share of the past 30 days that its 14-day RSI has spent above 50, the higher the coin's return over the next 14 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
