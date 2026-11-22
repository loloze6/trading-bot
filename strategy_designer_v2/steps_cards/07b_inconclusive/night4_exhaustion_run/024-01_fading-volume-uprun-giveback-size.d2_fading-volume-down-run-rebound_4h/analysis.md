---
line: 7.b inconclusive
backtest: 024-01_fading-volume-uprun-giveback-size.d2_fading-volume-down-run-rebound_4h
idea tested: 024-01_fading-volume-uprun-giveback-size.d2_fading-volume-down-run-rebound
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3319 USD
---
## Findings
- **F1:** The test's zero result (mean +0.0003 %, t 0.002, 4,537 cases) is an average of two opposite halves: by forecast quintile, the lowest fifth of cases loses 0.66 % against drift over 18 bars (t −2.84, 915 cases) and the highest fifth gains 0.66 % (t 2.00, 915 cases), the mean rising steadily from quintile 0 to 4 (−0.66, −0.37, −0.11, +0.45, +0.66 %).
- **F2:** The effect shows only on the largest losses. On the raw streak loss in usual moves (not standardised), the top fifth (median 4.0 usual moves) gains 1.32 % over 18 bars (t 4.43, 917 cases), while the bottom fifth (median 0.53) loses 0.72 % (t −3.09, 922 cases). The middle three fifths are near zero or negative (−0.06 %, −0.37 %, −0.20 %).
- **F3:** Fading volume adds nothing measurable. Among streaks rebuilt from prices in the top loss fifth (median 4.17 usual moves), those with fading volume gain 1.41 % (t 2.88, 423 cases, strength 0.16) and those with rising volume gain 1.02 % (t 2.91, 634 cases, strength 0.11); the difference, fading minus rising, is 0.39 % (Welch t 0.65).
- **F4:** Over the next 18 bars the rebound is clearest. Over all cases, the 6-bar mean is +0.06 % (t 0.92), the 18-bar mean is −0.005 % (t −0.04) and the 36-bar mean is −0.13 % (t −0.70). In the top forecast fifth, the 18-bar mean of +0.66 % (t 2.00) exceeds the 36-bar mean of +0.66 % (t 1.31) in reliability.
- **F5:** The large-loss rebound is mixed across years, with bear years against it. For fading-volume streaks in the top loss fifth:
- **F6:** The rebound leans on the coin's own recent trend. Cases in the top tercile of the prior 30-day return gain 0.45 % (t 1.81, 1,396 cases); those in the bottom tercile lose 0.40 % (t −1.83, 1,384 cases).

## Ideas
- `024-01_fading-volume-uprun-giveback-size.d2_fading-volume-down-run-rebound.b1_largest-fading-streak-losses-rebound` (from F1, F2, F5): When a coin has just fallen in an unbroken streak of four-hour periods, and the volume across the streak has been declining, it rises over the next three days, only when the streak's loss is among the largest the coin has made relative to its typical four-hour move over the past 30 days; the larger that loss, the larger the rise.
- `024-01_fading-volume-uprun-giveback-size.d2_fading-volume-down-run-rebound.b2_deep-down-streak-rebound` (from F2, F3, F4): When a coin has just fallen in an unbroken streak of four-hour periods, it rises over the next three days, and the larger the streak's loss relative to the coin's typical four-hour move over the past 30 days, the larger the rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
