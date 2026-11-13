---
line: 7.g patterns
backtest: N2-06_rebound-in-high-volatility_1d
idea tested: N2-06_rebound-in-high-volatility
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.3540 USD
---
## Findings
- **F1:** Across the six coins, a wide-range down day is followed by a next-day excess return of +0.89%, with t=6.07 over 1616 cases and 62.6% up days; a wide-range down day here means the top fifth of each coin's high-low range relative to its 60-day average. A wide-range up day is followed by −0.34%, with t=−2.04 over 1287 cases and 43.7% up days.
- **F2:** Where the bar closes within its range sorts what follows a drop. Drop days (z<−1.5) that close in the bottom fifth of their range are followed by +1.22%, with t=4.44 over 454 cases and 66.5% up. Drop days that close in the upper half are followed by −0.93%, with t=−1.23 over 45 cases and 44% up.
- **F3:** Among bars that close in the bottom tenth of their range, the next day returns +1.27% (t=3.73, n=312, 64.7% up) when the bar's range is in its widest third, and −0.14% (t=−0.53, n=312) when the range is in its narrowest third.
- **F4:** Drops (z<−1.5) on volume above 1.89 times the 20-day mean are followed by +1.25% (t=2.88, n=271), against +0.10% (t=0.33, n=271) on volume below 1.25 times the mean.
- **F5:** The volatility regime changes the size of the rebound but not its frequency, which is the step 5 result (z=0.10). Bars closing near their low are followed by +0.86% in high-volatility bars (t=3.00, n=419) against +0.10% in quiet bars (t=0.48, n=516), while the up shares are about the same (56.6% vs 57.0%). The most extreme drops (z<−3) are followed by +3.7% in high volatility (t=2.32, n=48) against −0.09% in quiet bars (n=31).
- **F6:** The rebound lasts beyond one bar: non-overlapping 3-day returns after drops with z<−2 average +1.50%, with t=3.81 over 355 cases.
- **F7:** The rebound after drops has faded in recent years. Drops with z<−1.5 are followed by −0.05% in 2024 (t=−0.11, n=129) and +0.17% in 2025 (t=0.32, n=109). Earlier years were stronger, for example +1.91% in 2020 (t=2.34) and +0.83% in 2023 (t=4.22).
- **F8:** The bar after a Friday bar returns +0.24% in excess (t=2.66, n=2070), with t=1.78 in 2018–2021 and t=2.10 in 2022–2025. The bar after a Monday bar returns −0.26% (t=−2.57, n=2076), with t=−1.91 and t=−1.72 in the same two halves.

## Ideas
- `N2-06_rebound-in-high-volatility.g1_wide-range-low-close-capitulation-rebound` (from F1, F2, F3, F4): A coin that falls on a day whose high-low range is much wider than its recent average range, and closes near that day's low, tends to close higher the next day, and more so when the day's volume is well above its recent average.
- `N2-06_rebound-in-high-volatility.g2_wide-range-up-day-fade` (from F1): A coin that rises on a day whose high-low range is much wider than its recent average tends to close lower the next day.
- `N2-06_rebound-in-high-volatility.g3_rebound-size-scales-with-volatility` (from F5): After a large one-day drop, the next-day rebound in a coin is larger in size when its recent volatility is high in its own history, even though rebounds are no more frequent.
- `N2-06_rebound-in-high-volatility.g4_multi-day-post-drop-drift` (from F6, F2): After a large one-day drop, a coin keeps drifting up over the following three days, not only the next one.
- `N2-06_rebound-in-high-volatility.g5_post-friday-upward-drift` (from F8): In a coin's daily bars, the bar that follows a Friday bar tends to close above its open-day level more than other days do.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
