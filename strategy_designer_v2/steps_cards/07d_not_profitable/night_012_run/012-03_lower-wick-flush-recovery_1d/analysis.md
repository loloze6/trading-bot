---
line: 7.d not profitable
backtest: 012-03_lower-wick-flush-recovery_1d
idea tested: 012-03_lower-wick-flush-recovery
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3162 USD
---
## Findings
- **F1:** The forecast sizes the position against the effect: on the 246 flush bars, those closing nearest their low (bottom quarter of close-in-range, mean 0.06) rose 2.96 % the next day (t 3.04, n 62) yet got a mean allocation of only 0.0099, while those closing nearest their high (top quarter, mean 0.48) fell 0.22 % the next day (t -0.30, n 62) with the largest allocation, 0.485.
- **F2:** Across the flush bars, a higher close-in-range comes with a lower next-day return (Spearman -0.197) and no different 3-day return (Spearman -0.005), which matches the verdict's 3-bar slope t of 0.77.
- **F3:** The book holds the position only on the flush bar itself (mean allocation 0.24 on the bar, 0.015 on the next), so it collects only the 1-day move. It earned 0.011 in summed next-day gains against about 0.120 in summed entry and exit fees.
- **F4:** The book's daily mean is -6.8e-6 against the coins' 0.00119. It is invested on only 2.4 % of days, and 70 % of those 416 days are losses.
- **F5:** The book's result rests on one window. Window w3 alone sums to -0.246 in daily book returns, against -0.074 for the next worst (w1), and the Sharpe stays at -0.21 with one window left out.
- **F6:** The rebound grows with the depth of the coin's prior fall. Flush bars in the lowest quarter of 20-day return (mean -32 %) rose 4.30 % the next day (t 2.92, n 49) and 3.69 % over 3 days (t 2.22, n 49). The other quarters rose between -0.28 % and 0.48 % the next day, all with |t| below 0.6.

## Ideas
- `012-03_lower-wick-flush-recovery.d1_close-at-low-flush-rebound` (from F1, F2, F3): Among daily bars that fall sharply on a volume burst, the closer the close sits to the bar's low, as a share of the bar's high-to-low range, the larger the price rise over the next 1 day.
- `012-03_lower-wick-flush-recovery.d2_flush-rebound-after-deep-falls` (from F5, F6): Among bars that fall sharply on a volume burst, the longer the lower wick below the close, as a share of the bar's high-to-low range, the larger the price rise over the next 3 days, only while the coin's 20-day return is negative, and the more so the deeper that 20-day fall.
- `012-03_lower-wick-flush-recovery.d3_capitulation-depth-predicts-rebound` (from F4, F6): Among daily bars that fall sharply on a volume burst, the more the coin has fallen over the prior 20 days, the larger the price rise over the next 1 to 3 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
