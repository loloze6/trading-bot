---
line: 7.b inconclusive
backtest: 016-05_up-even-volume-continuation.g1_evening-utc-hour-drift.d1_efficient-rise-keeps-rising_1h
idea tested: 016-05_up-even-volume-continuation.g1_evening-utc-hour-drift.d1_efficient-rise-keeps-rising
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3504 USD
---
## Findings
- **F1:** The tested measure is on the predicted side but small and mixed. Its mean is +0.27 % (t 1.41, 2916 cases). By coin it ranges from -0.29 % (LTC, t -0.62) to +0.84 % (XRP, t 1.31). By year it swings from -1.14 % (2019, t -2.01) to +1.20 % (2020, t 2.15). The size is an unusual move of -0.13 % per case, a strength of -0.016, against a cost of 0.19 %.
- **F2:** The continuation shows only in the largest rises measured against the coin's own volatility. The 3-day return is scaled by the past 30 days' hourly volatility, scaled up to 3 days. In the top quintile of that ratio, the excess 72-hour return is +1.51 % (t 3.42, 539 cases), a strength of 0.17. That is about 8 times the 0.19 % round trip. The three middle quintiles are near zero or negative, from -0.68 % (t -2.14) to +0.26 %. The overall OLS slope of the excess return on this ratio is t 3.61 (2691 rises), and weighting by the ratio gives a mean of +0.49 % (t 2.28).
- **F3:** Efficiency adds nothing beyond the size of the rise. Regressing the excess 72-hour return on both measures gives t 1.75 for the volatility-scaled rise and t 0.17 for the efficiency ratio. Inside the top quintile of scaled rises, the most efficient tercile earns the least: +0.41 %, against +1.85 % and +2.27 % for the other two.
- **F4:** The tested forecast blurs the signal it is built from. Standardising the efficiency ratio over a 73-hour window brings the forecast's Spearman correlation with the excess 72-hour return down to 0.009, against 0.044 for the raw efficiency ratio.
- **F5:** The strong-rise continuation is broad but not universal. In the top quintile it is positive in 5 of 6 coins: ZEC +2.68 % (t 2.15), BTC +1.30 % (t 2.14), XRP +2.87 %, LTC +1.32 %, ETH +0.68 %, while XMR is -0.04 %. It is positive in 7 of 8 years; 2022 is the exception at -1.14 %. It persists to 144 hours (+1.96 %), so it does not reverse at the 72-hour horizon.

## Ideas
- `016-05_up-even-volume-continuation.g1_evening-utc-hour-drift.d1_efficient-rise-keeps-rising.b1_efficient-rise-more-coins` (from F1): The more efficiently a coin has risen over its past 3 days (its 3-day rise large relative to the sum of its absolute hourly moves), the more it keeps rising over the next 3 days.
- `016-05_up-even-volume-continuation.g1_evening-utc-hour-drift.d1_efficient-rise-keeps-rising.b2_volatility-scaled-rise-continues` (from F2, F3, F5): The larger a coin's 3-day rise relative to its own typical 3-day move over the past 30 days, the more it keeps rising over the next 3 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
