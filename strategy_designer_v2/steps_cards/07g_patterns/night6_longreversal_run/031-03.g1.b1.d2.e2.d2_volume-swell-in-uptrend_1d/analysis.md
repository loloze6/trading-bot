---
line: 7.g patterns
backtest: 031-03.g1.b1.d2.e2.d2_volume-swell-in-uptrend_1d
idea tested: 031-03.g1.b1.d2.e2.d2_volume-swell-in-uptrend
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.4663 USD
---
## Findings
- **F1:** Across all bars of the 1d grid, every regime included, the 14-day volume swell (14-day mean volume over 30-day mean, minus 1) predicts the next 14 days' excess return. The lowest per-coin quintile averages −5.02 % (day-clustered t −3.05, 306 cases) and the highest averages +5.07 % (t 1.92, 306 cases). Their difference has a Welch t of 6.20, and the day-clustered regression of excess return on the swell's per-coin rank has a t of 3.12.
- **F2:** The swell effect does not need the close to be above its 50-day mean. Among grid bars below that mean, the lowest swell quintile averages −6.30 % over 14 days (t −2.56, 126 cases) and the highest averages +2.16 %, a high-minus-low Welch t of 3.91. The trending-only test the plan ran gave a slope t of only 1.65.
- **F3:** The weak side of the swell carries as much as the strong side. With fading volume (lowest quintile), the 14-day excess return is negative whether the coin's own 14-day return was up (−5.12 %, t −2.82, 138 cases) or down (−4.93 %, t −2.34, 168 cases). With swelling volume (highest quintile), it is +6.11 % after an up 14 days (t 1.81) and +3.16 % after a down 14 days (t 1.03).
- **F4:** The swell keeps its predictive power once momentum, volatility and trend are controlled for. With the 30-day return, the 30-day volatility and the distance to the 50-day mean in the same clustered regression, the swell's t is 2.94 and none of the three controls reaches |t| 1.5.
- **F5:** The effect peaks at the 14-day horizon. The clustered t of the swell rank is 2.27 at 7 days, 3.12 at 14 days and 1.31 at 28 days.
- **F6:** The effect is broad across coins but uneven across years.
- **F7:** The book's gain is carried by long holds. Trades of 15 to 30 days average +19.5 % before fees (1146 trades) and trades of 30 to 60 days average +37.7 % (326 trades). The 1790 trades of 14 days or less average +2.8 %, with a median of only +0.31 %.
- **F8:** The other angles showed nothing that stands out over that many looks:

## Ideas
- `031-03.g1.b1.d2.e2.d2.g1_volume-swell-any-trend` (from F1, F2, F4, F5, F6): The more a coin's mean daily volume over the last 14 days sits above its mean daily volume over the last 30 days, the more its price rises over the next 14 days, whether its close is above or below its 50-day mean.
- `031-03.g1.b1.d2.e2.d2.g2_fading-volume-precedes-falls` (from F1, F2, F3, F4): The more a coin's mean daily volume over the last 14 days sits below its mean daily volume over the last 30 days, the more its price falls over the next 14 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
