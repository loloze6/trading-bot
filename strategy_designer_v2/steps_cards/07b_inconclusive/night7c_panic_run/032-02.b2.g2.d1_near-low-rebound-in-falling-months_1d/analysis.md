---
line: 7.b inconclusive
backtest: 032-02.b2.g2.d1_near-low-rebound-in-falling-months_1d
idea tested: 032-02.b2.g2.d1_near-low-rebound-in-falling-months
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3455 USD
---
## Findings
- **F1:** Inside the regime the effect is graded and on the predicted side, but only across the close's place in the day's range: next-day excess return by close-location quintile runs −0.79 % (t −1.54), −1.05 % (t −1.91), +0.14 %, +0.29 %, +1.09 % (t 1.51), about 308 cases each. The near-low tercile minus the near-high tercile is +1.72 % (Welch t 4.17, 511 vs 515 cases), against +0.54 % (t 3.61) outside the regime.
- **F2:** The main measure (t 1.30) clips the forecast at 0, so it can only use the near-low half of this gradient. The near-high half carries half of the spread. The bottom forecast tercile earns −0.94 % the next day (t −2.11, 513 cases) and the top tercile +0.95 % (t 1.74, 517 cases), so neither half alone clears t 2.
- **F3:** The effect is drowned by the regime's own noise rather than absent. The next-day excess return has a standard deviation of 6.93 % inside the regime against 5.24 % outside. A mean of about +0.4 % to +1 % per case therefore needs far more cases than the 1,188 independent days the test had.
- **F4:** The effect is on the predicted side in every part shown, so it is weak and broad, not confined to one coin or year:
- **F5:** The 30-day fall adds to the close's place only where the close is near the low, and the effect is a one-day move:

## Ideas
- `032-02.b2.g2.d1.b1_near-low-rebound-more-coins` (from F1, F3, F4): When a coin's daily high-low ranges over the past 30 days are wide compared with the past 90 days and its 30-day return is negative, the lower its close sits within the day's high-low range, the larger its rise over the next 1 day, and the more so the deeper its 30-day fall.
- `032-02.b2.g2.d1.b2_near-high-close-fades` (from F1, F2, F5): When a coin's daily high-low ranges over the past 30 days are wide compared with the past 90 days and its 30-day return is negative, the higher its close sits within the day's high-low range, the larger its fall over the next 1 day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
