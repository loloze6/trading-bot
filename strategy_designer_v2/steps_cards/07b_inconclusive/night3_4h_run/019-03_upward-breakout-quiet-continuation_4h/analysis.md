---
line: 7.b inconclusive
backtest: 019-03_upward-breakout-quiet-continuation_4h
idea tested: 019-03_upward-breakout-quiet-continuation
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3586 USD
---
## Findings
- **F1:** The tested effect is on the predicted side but small and noisy: over 18 bars (3 days) the mean excess return is +0.21 % (t 1.29, 3069 cases), 0.023 of the coin's usual move, about half the ~0.05 strength of real ideas (findings F10). It is about 1.1 times the 0.19 % cost of a trade. It is no clearer at 6, 12 or 36 bars (t 0.37, 0.56, 1.14).
- **F2:** The supporting check could not be run, because the forecast is saturated. Its median, 25th and 75th percentiles are all 20, so the median split put all 3073 cases in the lower half and none in the upper. The test's grading was never measured.
- **F3:** The narrowness of the two-day stretch, the core of the idea's grading, does not order the outcome. The narrowness quintiles give +0.60, +0.35, −0.11, +0.46 and −0.20 %, none with |t| above 1.35, and the Spearman correlation of narrowness with the 18-bar excess return is −0.017.
- **F4:** The size of the break does order the outcome, measured as the close's distance above the two-day high in units of the 30-day average 4h range. The top quintile (median 1.35 ranges) earns +1.46 % excess over 3 days (t 3.24, 569 cases), about 7.7 times the cost of a trade. The other four quintiles sit between −0.37 % and +0.03 %. The raw break in percent shows the same pattern, with its top quintile at +1.00 % (t 2.09).
- **F5:** The coin's prior 7-day return splits the cases cleanly and in grades. Its quintiles give −0.75 % (t −2.37), −0.27 %, +0.41 %, +0.61 % and +1.12 % (t 2.17) over 18 bars, and −0.74 % up to +1.89 % (t 2.53) over 36 bars. Breakouts after a falling week lose (−0.51 %, t −2.07, 903 cases), while those after a rising week gain (+0.57 %, t 2.68, 1949 cases).
- **F6:** The two conditions together carry the effect. Large breaks (top tercile) after a rising week earn +1.44 % over 3 days (t 3.12, 696 cases), while every tercile after a falling week is negative (−0.25 to −0.85 %).
- **F7:** Market noise and calmer conditions also matter. By year the result swings from −0.84 % (2019, t −2.25) and −0.77 % (2022) to +1.56 % (2020, t 3.87), and LTC is negative (−0.51 %). After a rising week, cases with below-median 30-day volatility earn +1.02 % (t 3.65, 1196 cases), against −0.16 % in high volatility.

## Ideas
- `019-03_upward-breakout-quiet-continuation.b1_upward-breakout-on-more-coins` (from F1, F2, F7): When a four-hour bar closes above the highest high of a coin's preceding two-day narrow stretch, the coin rises over the next three days, and the narrower that stretch was compared with the coin's 30-day average four-hour range, the larger the rise.
- `019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week` (from F3, F4, F5, F6): When a four-hour bar closes above the highest high of a coin's preceding two days, only while the coin's 7-day return is positive, the coin rises over the next three days, and the farther that close sits above the two-day high, measured in the coin's 30-day average four-hour range, the larger the rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
