---
line: 7.b inconclusive
backtest: 012-04_flush-depth-retracement-size_1d
idea tested: 012-04_flush-depth-retracement-size
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3625 USD
---
## Findings
- **F1:** The test's forecast barely grades the flush bars: 78% of kept flush bars sit at the cap of 20, and the middle and top forecast terciles both average exactly 20.0. Their mean excess 3-day returns run lo −0.0041, mid +0.0117, hi −0.0011, so the slope (t −0.65 recomputed, −0.75 in the verdict) has almost no spread to work on.
- **F2:** The flush bars show no rebound distinct from other sharp falls. Their mean excess 3-day return is +0.0022 (t 0.28, n 75), against +0.0012 for the 351 other sharp falls (Welch t 0.11). At 1 day the flush bars do worse: −0.0099 against +0.0092 (Welch t −2.53).
- **F3:** At longer horizons the tested slope turns against the idea: t −2.22 over 5 days and t −2.40 over 10 days (n 75 and 73). Deeper capped flushes keep falling rather than retracing.
- **F4:** The long-lower-wick condition works against the rebound. Among all 354 declustered sharp falls, the wick-over-range slope on the excess return is t −3.34 at 1 day and −1.96 at 3 days. The highest wick quartile averages −0.0112 over 3 days and the lowest +0.0131. Volume-burst falls without the wick average +0.0100 (n 119); those with it average −0.0026 (n 41).
- **F5:** Among all sharp falls, the volume ratio to its prior 20-day mean predicts the rebound in grade. Its slope is t 3.99 over 1 day, 3.24 over 2 days and 2.53 over 3 days (n 351–354), and it fades by 5 days (t −0.52).
- **F6:** Among all sharp falls, the raw open-to-low drop in percent predicts the rebound strongly: t 5.74 at 1 day, 4.90 at 2 days, 4.41 at 3 days, and 1.12 at 5 days. Scaled by 20-day volatility, the same drop shows nothing (t −0.13 at 3 days), so part of this grading may come from high-volatility periods.
- **F7:** Flush outcomes swing by year rather than holding steadily. Mean excess 3-day return is +0.060 in 2020, −0.040 in 2021, −0.063 in 2022 and about +0.02 in 2023–2025, on 5–14 cases per year.

## Ideas
- `012-04_flush-depth-retracement-size.b1_volume-burst-sharp-fall-rebound` (from F5, F4, F2): Among bars that fall sharply, the larger the bar's volume relative to its mean over the prior 20 days, the larger the price rise over the next 3 days.
- `012-04_flush-depth-retracement-size.b2_sharp-fall-depth-retracement` (from F6, F4, F1): Among bars that fall sharply, the larger the bar's drop from its open to its low, the larger the price rise over the next 3 days, as price drifts back toward where it traded before the fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
