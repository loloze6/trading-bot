---
line: 7.b inconclusive
backtest: 021-02_below-falling-cloud-continues-down.d1_below-gently-falling-calm-cloud.b1_below-cloud-short-more-coins_1d
idea tested: 021-02_below-falling-cloud-continues-down.d1_below-gently-falling-calm-cloud.b1_below-cloud-short-more-coins
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4709 USD
---
## Findings
- **F1:** The plan's main measure has the wrong sign for a short, so the "inactive" verdict hides a result on the side the idea predicts. The plan's formula, -forecast/10 x (forward return minus drift), counts a rise as a gain. With the sign corrected (forecast/10 x excess return), the short's gain is +0.95 % per case, t 1.55, over 353 non-overlapping cases. The coins ended 1.84 % below their drift (t -1.17). The supporting check, -5.9 % for |forecast| above the median minus below, also points the idea's way.
- **F2:** The cloud-slope grading holds clearly and as the idea states: the slower the 26-day fall, the more the coin falls afterwards. The rank correlation of the standardised fall's steepness with the 26-day excess return is +0.23 (p 0.00002). The gentlest fifth of falls ends 12.2 % below drift (t -3.9, 71 cases) and the second fifth 7.1 % below (t -2.2, 70 cases). The three steepest fifths end 2.4 % to 4.0 % above drift.
- **F3:** The slow-fall effect is not confined to one group of coins or one period. The slowest third of falls ends 9.1 % below drift on the six default coins (t -2.8, 53 cases) and 10.9 % below on the other thirteen (t -2.9, 65 cases). It ends 12.9 % below drift after 2021 (t -4.8, 80 cases) and 4.2 % below before (t -0.8, 38 cases).
- **F4:** The volatility part of the forecast runs against the idea, and this cancels the slope part in the tested forecast.
- **F5:** The market's own moves dominate the result.
- **F6:** Cost is no obstacle for the slow-fall cases.

## Ideas
- `021-02_below-falling-cloud-continues-down.d1_below-gently-falling-calm-cloud.b1_below-cloud-short-more-coins.b1_below-gently-falling-cloud` (from F1, F2, F3, F6): When a coin closes below its Ichimoku cloud and the cloud is falling, its return over the next 26 days is negative, and more negative the slower the cloud has fallen over the past 26 days.
- `021-02_below-falling-cloud-continues-down.d1_below-gently-falling-calm-cloud.b1_below-cloud-short-more-coins.b2_gentle-cloud-wild-coin` (from F2, F4, F5, F6): When a coin closes below its Ichimoku cloud and the cloud is falling, its return over the next 26 days is negative, and more negative the slower the cloud has fallen over the past 26 days and the wilder the coin's daily moves have been over the past 30 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
