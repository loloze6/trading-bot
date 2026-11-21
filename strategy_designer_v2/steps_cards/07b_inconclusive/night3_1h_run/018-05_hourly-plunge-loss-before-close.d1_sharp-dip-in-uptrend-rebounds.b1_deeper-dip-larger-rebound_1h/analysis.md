---
line: 7.b inconclusive
backtest: 018-05_hourly-plunge-loss-before-close.d1_sharp-dip-in-uptrend-rebounds.b1_deeper-dip-larger-rebound_1h
idea tested: 018-05_hourly-plunge-loss-before-close.d1_sharp-dip-in-uptrend-rebounds.b1_deeper-dip-larger-rebound
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3580 USD
---
## Findings
- **F1:** The idea grades as it predicts when the fall is measured in its own unit, but not in the test's forecast. The fall is the raw 24-hour return in multiples of the 30-day mean absolute daily return. By that raw multiple, the unusual 72-hour move falls steadily across the quintiles, deepest to shallowest: +1.55 % (t 3.58, 488 cases), +0.63 %, +0.47 %, +0.25 %, −0.13 %. The deeper half beats the shallower half by +1.38 % (Welch t 3.74). Rank correlation of the raw multiple with the move is −0.077 (p 0.0001), and a more negative multiple means a deeper fall. By the test's forecast, the quintiles show no order: +0.87 %, +0.47 %, +0.68 %, +0.01 %, +0.74 %, with rank correlation −0.004. So the supporting check failed (−0.23 %) because of how the forecast was built, not because the effect is ungraded: it standardises over 500 hours, cubes with a pivot, and is read at forecast rises of 2 points, which scrambles the ranking of depth.
- **F2:** The pooled main measure is on the idea's side: +0.55 % unusual over 72 hours, t 2.98, 2440 cases. Its strength is 0.064, about the 0.05 of real ideas. The total move is +0.96 %, 5.0 times the 0.19 % cost of a trade, and the unusual move is 2.9 times it. The deepest raw quintile's +1.55 % is about 8 times the cost.
- **F3:** The deeper-fall advantage holds on almost every coin and in most years. The deeper half beats the shallower half on 6 of 6 coins: BTC +0.85 % vs −0.01 %, ETH +1.59 % vs −0.55 %, XRP +2.43 % vs −0.67 %, LTC +1.11 % vs +0.35 %, ZEC +1.45 % vs +0.13 %, and XMR, the weakest, +0.14 % vs −0.14 %. By year it beats the shallower half in 7 of 8 years; 2019 is the exception (+0.71 % vs +0.99 %).
- **F4:** The effect is mixed by period, and drowned in bear years whose 30-day rises are brief. The 2018 cases lose −2.93 % (t −4.32, 180 cases) and the 2022 cases lose −1.08 % (t −2.14). 2020, 2021 and 2025 gain +1.12 %, +2.33 % and +1.22 %.
- **F5:** The rebound grows with the strength of the 30-day rise as well as with the depth of the fall. By 30-day-return quintile, the unusual move rises from −0.53 % in the weakest (mean 30-day return +1.3 %) to +1.67 % (t 3.14) and +0.98 % in the two strongest. Rank correlation is 0.060 (p 0.009). Deep falls inside the stronger-than-median rises earn +1.84 % (t 4.17, 548 cases). Shallow falls inside the weaker rises earn −0.48 %.

## Ideas
- `018-05_hourly-plunge-loss-before-close.d1_sharp-dip-in-uptrend-rebounds.b1_deeper-dip-larger-rebound.b1_sharp-dip-rebound-more-coins` (from F1, F2, F3): When a coin's 24-hour return, read at an hourly close, falls by several times its 30-day average absolute daily return while its 30-day return is positive, the coin rises over the next 3 days more than its normal drift, and the deeper the 24-hour fall in multiples of its 30-day average absolute daily return, the larger the rise.
- `018-05_hourly-plunge-loss-before-close.d1_sharp-dip-in-uptrend-rebounds.b1_deeper-dip-larger-rebound.b2_deep-dip-in-strong-rise` (from F1, F4, F5): When a coin's 24-hour return, read at an hourly close, falls by several times its 30-day average absolute daily return while its 30-day return is positive, the coin rises over the next 3 days more than its normal drift. The deeper the 24-hour fall in multiples of its 30-day average absolute daily return, and the larger its 30-day return, the larger the rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
