---
line: 7.d not profitable
backtest: 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.g1_high-volatility-fall-reversal_1d
idea tested: 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.g1_high-volatility-fall-reversal
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 3.6183 USD
---
## Findings
- **F1:** Almost all of the book's edge sits in its deepest-fall bars. In the top forecast quintile (forecast 14.5–20, allocation 0.91) each active bar gains 0.0090, with next-day return 0.0120 and t 5.30. The middle three quintiles gain only 0.0005–0.0020 per bar.
- **F2:** Fees eat most of the shallow-fall positions. The lowest forecast quintile pays a fee of 0.00008 per bar against a gain of 0.00008. The second and third quintiles pay 0.00021 and 0.00030 against gains of 0.00050 and 0.00063. The 3366 trades average −0.11% before fees and −0.21% after. The book's mean daily return is 0.00045, against 0.00118 for holding the coins.
- **F3:** The reversal grows much faster than the fall's size. In the high-volatility regime, falls beyond 2 standard deviations are followed by 0.0201 next day (n 124), falls of 1–1.5 by 0.0106 (n 416), and falls of 0–1 by only 0.0034–0.0038.
- **F4:** The high-volatility regime is what makes falls reverse. The same falls beyond 2 standard deviations in the calm regime are followed by only 0.0013 (n 287), and falls of 1.5–2 by 0.0009 (n 278).
- **F5:** Among falls beyond 1 standard deviation, the reversal depends on the four days before the fall. After the steepest prior 4-day declines the next day returns 0.0168 (t 5.06, n 459). After a flat prior 4 days it returns −0.0038 (t −1.78, n 458).
- **F6:** The coin's 5-day return grades the next day across all active bars. The bottom 5-day-return quintile (−56% to −10%) gives a next-day return of 0.0110 (t 4.00). The flat quintile (−4% to 0%) gives −0.0005 (t −0.36), even though allocation there is a similar 0.39.
- **F7:** The book's losses come from big positions on mid-sized falls that keep going. The worst 5% of active bars carry allocation 0.78 against 0.39 overall, and a day's fall of −1.30 standard deviations against −0.55. All of them sit in the high-volatility regime, and the book's deepest fall is −22.6% (Calmar 0.70).

## Ideas
- `011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.g1_high-volatility-fall-reversal.d1_deep-capitulation-fall-reversal` (from F1, F2, F3, F4, F5, F7): In a coin whose daily volatility over the past 20 days is high, a down day is followed by a rise over the next 1 day, and that rise grows more than in proportion to the fall measured in the coin's 20-day daily standard deviations, so shallow falls are followed by almost no rise. The rise is largest when the fall extends the coin's decline over the prior 4 days, and it grows with the depth of that 4-day decline.
- `011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.g1_high-volatility-fall-reversal.d2_volatile-five-day-fall-rebound` (from F4, F5, F6): In a coin whose daily volatility over the past 20 days is high, the coin rises over the next 1 day, and the rise is larger the deeper the coin's 5-day fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
