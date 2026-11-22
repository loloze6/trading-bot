---
line: 7.b inconclusive
backtest: 023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days_1d
idea tested: 023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3096 USD
---
## Findings
- **F1:** The test's result points the way the idea predicts but falls short of the bar. On 1,476 independent 5-day cases the correlation is +0.034 with t 1.29. The mean move in the forecast's direction is +0.52 % (strength 0.045, t 1.66), close to the 0.05 strength real ideas usually show. A true effect of that size needs far more cases than six coins provide to reach t 2.
- **F2:** The effect is spread thinly across coins rather than carried by one. Five of six coins have a positive correlation: BTC +0.036, ETH +0.077, LTC +0.016, XRP +0.036, ZEC +0.063. XMR alone is negative at −0.051. No coin reaches t 2 (largest t 1.28, ETH, on 275 cases), so each coin's sample is too small on its own.
- **F3:** The effect changes sign over time, which adds noise without overturning the direction.
- **F4:** The effect is mostly on the long side. After 30-day rises the 5-day move in the forecast's direction is +0.86 % (strength 0.077, t 1.82, 769 cases). After 30-day falls it is +0.16 % (t 0.39, 707 cases).
- **F5:** The effect is not clearly graded by forecast size, which weakens the correlation. The mean directional move by quartile of |forecast| is +0.67 %, +0.78 %, −0.54 % and +1.18 % (t 1.04, 1.26, −1.09, 1.61; 369 cases each).
- **F6:** The plan's 5-day horizon is roughly where the effect peaks, so a different horizon would not give a clearer answer.
- **F7:** The move per case is large enough to pay for trading. The total move of +0.73 % per case is 3.8 times the 0.19 % cost of a trade. The question left open is whether the effect is real, not whether it could pay.

## Ideas
- `023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins` (from F1, F2, F6, F7): In a coin whose 30-day net move has been large relative to its 30-day high-low range, the larger its 30-day return, the further the coin moves in that same direction over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
