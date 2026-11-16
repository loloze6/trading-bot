---
line: 7.g patterns
backtest: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.d1_near-high-drift-extension-fades.b2_monthly-run-drift-then-fade_1d
idea tested: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.d1_near-high-drift-extension-fades.b2_monthly-run-drift-then-fade
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.5123 USD
---
## Findings
- **F1:** On Saturdays, a coin's day return rises with its 5-day return up to Friday's close. The slope is 0.0645 (t=8.92, n=2382 coin-Saturdays). By quintile of that 5-day return, the mean Saturday return climbs steadily: −0.0031 (t=−1.47), 0.0007, 0.0047 (t=4.30), 0.0093 (t=4.93), 0.0111 (t=4.39).
- **F2:** Saturdays are the strongest day for both the coins and the book.
- **F3:** After a coin's largest 1-day falls (lowest quintile of the prior day's return), the next day's mean return is +0.0060 (t=6.09, n=3448). In the other four quintiles it stays between −0.0011 and +0.0007, all |t|<1.2.
- **F4:** The book's worst 5% of days come after a run-up. On those days the coin's prior 5-day return averaged +0.0583; the coin then fell 0.0465 and the book lost 0.0303.
- **F5:** Above the 200-day average, the 10-day excess return rises with the 30-day return only up to about the 8th decile (mean 0.0634, t=1.96, 30-day return ≈0.30). It then drops to −0.0079 and 0.0083 in the top two deciles (30-day return ≈0.44 and 0.66).
- **F6:** Below the 200-day average, the top quintile of 30-day returns is followed by a 10-day excess return of −0.0228 (t=−2.10, n=130). The overall slope is negative (t=−1.69, n=629), which is weak given how many angles were examined.

## Ideas
- `002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.d1_near-high-drift-extension-fades.b2_monthly-run-drift-then-fade.g1_weekend-continuation-of-weekly-run` (from F1, F2): Going into the weekend, the larger a coin's 5-day return at Friday's close, the larger its rise over the next 1 day (Saturday).
- `002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.d1_near-high-drift-extension-fades.b2_monthly-run-drift-then-fade.g2_next-day-rebound-after-falls` (from F3): The larger a coin's 1-day fall, the larger its rise over the next 1 day.
- `002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.d1_near-high-drift-extension-fades.b2_monthly-run-drift-then-fade.g3_extreme-monthly-run-fades` (from F5, F4): While a coin's close is above its 200-day average, the larger its 30-day return beyond its usual size, the smaller its rise over the next 10 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
