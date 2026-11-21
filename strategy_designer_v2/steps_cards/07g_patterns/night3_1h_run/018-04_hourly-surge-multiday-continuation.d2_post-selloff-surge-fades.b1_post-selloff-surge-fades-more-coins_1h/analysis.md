---
line: 7.g patterns
backtest: 018-04_hourly-surge-multiday-continuation.d2_post-selloff-surge-fades.b1_post-selloff-surge-fades-more-coins_1h
idea tested: 018-04_hourly-surge-multiday-continuation.d2_post-selloff-surge-fades.b1_post-selloff-surge-fades-more-coins
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4685 USD
---
## Findings
- **F1:** The calmer the last 24 hours compared with the coin's past 30 days, the weaker the next 5 days. The ratio used is the 24-hour standard deviation of hourly returns over the 720-hour one, split into quintiles within each coin. After the calmest fifth, the drift-removed 120-hour return has a strength of -0.111 (t -4.26, 1,327 non-overlapping cases), or -1.31 %. After the most agitated fifth it is +0.055 (t 1.81, 1,326 cases), or +0.77 %. The quintiles in between rise almost steadily (-0.048, +0.002, +0.049).
- **F2:** The calm-before-weakness pattern holds across coins, windows and the recent years.
- **F3:** The weakness after calm is strongest when the calm 24 hours also ended lower. In the calmest fifth, a falling 24-hour return gives a strength of -0.186 (t -4.70, 635 cases), against -0.042 (t -1.23, 686 cases) when it rose. In the second-calmest fifth it is -0.084 (t -2.35) after a fall.
- **F4:** The pattern is large next to the cost of a trade. The calm fifth's -1.31 % unusual move over 5 days is about 6 times the 0.22 % round trip. After removing the coin's +0.85 % normal 5-day rise, a short there would still capture about 0.46 % in total, about 2 times the cost. At 2 days the calm fifth is -0.50 % (t -3.95); at 10 days, -1.64 % (t -2.38).
- **F5:** The tested situation shows no fade over 5 days. The verdict's mean is -0.18 % per case (t -0.47, 1,186 cases). In the grid sample, the 5-day strength after a falling prior 7 days is -0.001 to -0.088 by surge quintile, with no level-wise shortfall growing with the surge. Its top surge quintile after a prior fall is -0.037 (t -0.96).
- **F6:** Pooled 30-day momentum looks predictive, but the effect comes from differences between windows, not within them.
- **F7:** Over one day, two patterns stand out, but both are small next to a trade's cost (F10 of the prior findings).

## Ideas
- `018-04_hourly-surge-multiday-continuation.d2_post-selloff-surge-fades.b1_post-selloff-surge-fades-more-coins.g1_quiet-day-precedes-weakness` (from F1, F2, F4): The quieter a coin's last 24 hours have been compared with its own past 30 days, the further its price falls below its usual 5-day return over the next 5 days.
- `018-04_hourly-surge-multiday-continuation.d2_post-selloff-surge-fades.b1_post-selloff-surge-fades-more-coins.g2_quiet-decline-keeps-sliding` (from F1, F3, F4): After a 24-hour fall that came with unusually low volatility compared with the coin's past 30 days, the price keeps falling relative to its usual 5-day return over the next 5 days; the lower that volatility, the larger the further fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
