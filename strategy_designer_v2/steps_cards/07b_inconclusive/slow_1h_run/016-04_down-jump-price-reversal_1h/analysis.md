---
line: 7.b inconclusive
backtest: 016-04_down-jump-price-reversal_1h
idea tested: 016-04_down-jump-price-reversal
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3106 USD
---
## Findings
- **F1:** The tested forecast barely ranks the falls by how they were made, because the raw share of the 3-day fall carried by the 3 biggest hourly losses is mostly a measure of how small the fall is: its Spearman correlation with the 72-hour return is 0.84, and the top share quintile (mean share 25.4) holds falls averaging only -0.9 %, against -11.2 % in the bottom quintile.
- **F2:** The test's negative slope (t -1.92 on 2,762 fallen cases) comes from the size of the fall, not from its shape: tiny falls underperform and large falls rebound. In the top share quintile the excess 72-hour return is -1.05 %, and in the small-fall tercile it is -0.22 % to -1.18 % across share terciles, against +0.10 % to +0.87 % in the big-fall tercile.
- **F3:** Once fall size is controlled, the way the fall was built adds nothing. In a regression on fall size, the share of hourly losses carried by the top 3 has t -0.58 at 72 hours and t 1.57 at 24 hours, and the absolute top-3 loss has t 0.20 at 72 hours. Inside the big-fall tercile, the lowest loss-share tercile rebounds most (+1.46 % excess over 72 hours, against +0.04 % and +0.15 %).
- **F4:** The share effect is mixed across coins and years rather than hidden in one part of the data. Controlled for fall size, its 72-hour slope has t from -1.56 (ETH) to +1.60 (BTC) across the six coins. Across years, t runs from -2.23 (2025) to +1.35 (2020), and the signs alternate.
- **F5:** The size of the 3-day fall carries a clear graded reversal that is strongest over the next day. On the fallen grid cases, excess return regressed on the 72-hour return has t -8.11 at 24 hours (slope -0.144, n 2,669). The same regression gives t -3.53 at 72 hours and t -2.54 at 168 hours. With the top-3 loss in the model, the 24-hour fall-size coefficient keeps t -7.12.

## Ideas
- `016-04_down-jump-price-reversal.b1_fall-size-next-day-rebound` (from F2, F3, F5): When a coin has fallen over the past 3 days, the larger its 3-day fall, the more it rises over the next 1 day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
