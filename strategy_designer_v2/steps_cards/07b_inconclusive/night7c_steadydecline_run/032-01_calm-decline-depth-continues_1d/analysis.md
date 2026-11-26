---
line: 7.b inconclusive
backtest: 032-01_calm-decline-depth-continues_1d
idea tested: 032-01_calm-decline-depth-continues
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.5256 USD
---
## Findings
- **F1:** The test's result is zero, not merely short of the bar: the slope of the 5-day excess return on the forecast is 0.0004 with a day-clustered t of 0.35 over 173 cases on 141 days, and the short-direction mean excess is −0.05 % with t −0.07. The idea's size is 0.019 of a usual 5-day move (unusual move +0.29 %, t 0.41 over 178 days), and its total move of −0.32 % per case is against the book, set against a trade cost of 0.19 %.
- **F2:** In the visible folds B and C, the calm regime covers only 7.0 % of the bars, leaving 40 non-overlapping 5-day cells after a calm fall. Their mean excess is −0.83 % (t −0.44), and the slope on the 28-day fall is 0.032 (day-clustered t 0.15 over 33 days).
- **F3:** Depth does not grade the outcome. Across the calm-fall quartiles from deepest to shallowest, the 5-day excess is +0.07 %, −3.59 %, +0.84 % and −0.44 %, which shows no order with the size of the fall.
- **F4:** The calm-fall cases split in opposite directions by coin and by window, so the mean is a mix rather than a weak common effect. By coin the 5-day excess is ETH +8.9 % (5 cases) against LTC −6.6 % (10 cases); by window it is w13 +8.2 % and w12 +2.1 % against w16 −15.5 % and w15 −5.0 %.
- **F5:** Other horizons do not rescue it. The calm-fall slope on the 28-day fall has a day-clustered t of 1.26 at 3 days (56 days) and 1.54 at 10 days (16 days). With the calm regime dropped, the slope across all falls has t −0.08, −0.21 and 0.71 at 3, 5 and 10 days, and the 5-day mean excess after all falls is −0.56 %.
- **F6:** The closest hint is a looser calm reading that measures ranges against their own 90-day level, and it still falls short:
- **F7:** The one strong number points the other way and rests on very little evidence. In loud falls (range ratio above 1), the 10-day slope on the 28-day fall is −0.56 with t −5.26, meaning deeper loud falls rebound. It covers only 29 cases on 8 days, too few to build on.

## Ideas
- No ideas: The tested effect is zero (F1) and no part of the data shows it clearly: depth does not grade the outcome (F3), the coins and windows contradict each other (F4), no horizon reaches t 2 (F5), and the quiet-range hint stays below t 2 and disappears when graded (F6). An amended idea would rest on noise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
