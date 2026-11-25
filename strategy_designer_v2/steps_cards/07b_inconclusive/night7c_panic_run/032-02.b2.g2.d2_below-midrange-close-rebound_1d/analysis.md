---
line: 7.b inconclusive
backtest: 032-02.b2.g2.d2_below-midrange-close-rebound_1d
idea tested: 032-02.b2.g2.d2_below-midrange-close-rebound
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 1
cost: 0.2222 USD
---
## Findings
- **F1:** The test's result lies on the side the idea predicts but just short of the bar: a forecast-weighted excess next-day return of +0.39 % with t 1.97 over 1,369 days. In folds B and C it is +0.60 % with t 1.76 over 1,712 bars and 626 days, positive for all 6 coins (BTC t 2.02, XMR t 2.91, the others t 0.80 to 1.11) and in 9 of 12 windows, so the effect is consistent but too small for six coins to show at t ≥ 2.
- **F2:** The effect is present only when ranges are wide. When the 30-day mean range is wider than the 90-day one, the next-day excess return rises with how low the close sits in the day's range (slope 0.024, t 4.51, 1,660 bars), with closes in the lowest fifth of the range at +1.57 % (t 3.97, 264 bars). When ranges are narrow the slope is −0.0004 (t −0.11, 2,781 bars).
- **F3:** When ranges are wide, closes in the upper half of the day's range are followed by a below-normal next day: −0.47 % (t −1.55), −0.76 % (t −2.28) and −1.49 % (t −2.86), from the top of the range down to the middle. The plan's long-only regime leaves out this half of the gradient.
- **F4:** The test's forecast does not grade the move. By forecast quartile the weighted excess is +0.45 %, +0.83 %, +0.17 % and +0.85 % (t 0.93, 2.00, 0.36, 1.64), while the raw close location does grade it (F2). The 60-bar standardisation of the location blurs the gradient the idea describes.
- **F5:** The plan's 1-day horizon is where the effect lives. On non-overlapping grids of wide-range, lower-half closes the excess is +0.82 % at 1 day (t 3.80, 780 cases), +0.74 % at 2 days (t 1.77, 379), −0.29 % at 3 days (t −0.38, 232) and −1.52 % at 5 days (t −1.76, 154).
- **F6:** A falling month adds little. Cases after a negative 30-day return earn +0.94 % (t 1.36, 493 bars) against +0.47 % (t 1.25, 1,219 bars) after a rising one, so the effect does not depend on the decline the brief describes.

## Ideas
- `032-02.b2.g2.d2.b1_below-midrange-rebound-all-coins` (from F1, F2, F5): When a coin's daily high-low ranges over the past 30 days are wide compared with the past 90 days, the further its close sits below the middle of the day's high-low range, the larger its rise over the next 1 day.
- `032-02.b2.g2.d2.b2_close-location-in-wide-ranges` (from F2, F3, F5): When a coin's daily high-low ranges over the past 30 days are wide compared with the past 90 days, the further its close sits below the top of the day's high-low range, the larger its return over the next 1 day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
