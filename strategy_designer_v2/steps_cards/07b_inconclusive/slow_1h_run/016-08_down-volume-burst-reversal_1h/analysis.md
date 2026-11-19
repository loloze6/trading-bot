---
line: 7.b inconclusive
backtest: 016-08_down-volume-burst-reversal_1h
idea tested: 016-08_down-volume-burst-reversal
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.2884 USD
---
## Findings
- **F1:** The tested measure is on the side the idea predicts but too small for this data. The top-half minus bottom-half excess 72-hour return is +0.0033 with Welch t 1.05 on 2,762 grid cases (1,381 per half). At this effect size, reaching t = 2 would take about 10,000 cases, roughly 3.6 times what the six default coins provide.
- **F2:** The effect is weak and graded only loosely. The rank correlation of forecast with excess 72-hour return is rho 0.028 (p 0.14, n 2,762). Across forecast quintiles the mean excess return is not monotone: -0.0075, +0.0017, -0.0049, +0.0004, +0.0027.
- **F3:** The effect is mixed across coins. ETH shows it clearly (+0.0158, t 2.16, n 461) and XMR leans the same way (+0.0091, t 1.28). BTC (-0.0010, t -0.17), LTC (-0.0027, t -0.34) and XRP (-0.0052, t -0.66) go the other way.
- **F4:** The effect is mixed across periods. It is positive in 2019 (+0.0169, t 2.18) and 2021 (+0.0202, t 1.61) but reversed in 2025 (-0.0155, t -2.07). Across the 24 windows only 62.5 % have a positive difference, with a mean of +0.0017 (t 0.63).
- **F5:** The effect appears only at the plan's 3-day horizon. At 24 hours the difference is +0.0003 (t 0.27, n 8,482), and at 7 days it is -0.0003 (t -0.04, n 1,216). The raw top-3 share gives the same picture as the forecast: +0.0032, t 1.01 at 72 hours.
- **F6:** It leans larger after the deepest falls, though no part of the data shows it clearly. In the deepest tercile of 72-hour returns the difference is +0.0071 (t 1.08), against +0.0023 (t 0.43) in the middle tercile and +0.0013 (t 0.28) in the shallowest. After rises the volume share predicts nothing (-0.0021, t -0.65, n 2,865).
- **F7:** The book loses while holding the coins gains: the book's mean daily return is -0.00074 against +0.00119 for holding. Per hourly bar, the timing part of the gain is negative (-0.000012) and the market part is positive (+0.000015), at a mean position of 0.24.

## Ideas
- `016-08_down-volume-burst-reversal.b1_volume-burst-reversal-more-coins` (from F1, F2): When a coin has fallen over the past 3 days, the larger the share of that period's volume traded in its few busiest hours, the more of the fall the coin wins back over the next 3 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
