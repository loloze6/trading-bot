---
line: 7.d not profitable
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g1_two-week-momentum-continuation.g3_moderate-falls-keep-falling_1d
idea tested: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g1_two-week-momentum-continuation.g3_moderate-falls-keep-falling
step 5: mismatch
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3782 USD
---
## Findings
- **F1:** The book earns 0.42 bp a day against 11.8 bp for holding the coins (Sharpe 0.22 against 0.55), so the yearly return is too small for the Calmar of 0.07; it is short on 55% of bars (9,676 of 17,524), long on only 6.4% (1,124), and flat on 38%, which gives a market part of −0.70 bp a day that eats most of its 1.5 bp of timing gain.
- **F2:** After 14-day rises, where the book is always flat, the excess 7-day return rises with the size of the rise, from +0.26% in the smallest fifth (n=171, t=0.29) to +3.76% in the largest fifth of rises scaled by volatility (n=171, t=2.55); this is the largest graded effect in the data, and the book takes none of it.
- **F3:** After 14-day falls the excess 7-day return is negative in five of the six fall-size sextiles, between −1.2% and −1.9% for the middle grades (t −1.3 to −1.9, about 145 cases each), so the short side's direction is right but its edge is about 1.5% a week.
- **F4:** The deepest falls do not rebound: the largest fall sextile has an excess of −0.60% (n=145, t=−0.53), and grid points with a positive forecast average only +0.34% (n=140); the long leg adds little.
- **F5:** Positions are small: the mean absolute allocation on active bars is 0.155 (median 0.144), so even the correct short edge turns into only 0.37 bp a day on short bars.
- **F6:** Falls keep falling about equally whatever the 60-day trend: −1.42% when the 60-day return is negative (n=369, t=−2.15) and −1.77% when it is positive (n=212, t=−2.00). By year the fall effect turns positive only in 2021, 2023 and 2024 (+1.6%, +0.4%, +0.5%), the years with the strongest rising markets.

## Ideas
- `013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g1_two-week-momentum-continuation.g3_moderate-falls-keep-falling.d1_two-week-momentum-both-sides` (from F1, F2, F3, F5): The larger a coin's 14-day rise, the higher its return over the next 7 days, and the larger its 14-day fall, the lower its return over the next 7 days, with the strongest follow-through after the largest rises.
- `013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g1_two-week-momentum-continuation.g3_moderate-falls-keep-falling.d2_falls-fall-rises-rise` (from F1, F2, F4, F6): The larger a coin's 14-day fall, up to the deepest falls, the lower its return over the next 7 days, while coins with the deepest 14-day falls rebound, except that coins with large 14-day rises keep rising over the next 7 days, more so the larger the rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
