---
line: 7.b inconclusive
backtest: 028-01_volume-surge-up-continuation.d1_high-volume-hourly-drops-rebound.b1_heavy-volume-rises-keep-rising_1h
idea tested: 028-01_volume-surge-up-continuation.d1_high-volume-hourly-drops-rebound.b1_heavy-volume-rises-keep-rising
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 1
cost: 0.2051 USD
---
## Findings
- **F1:** The tested idea comes out on its predicted side but well short of the bar: recomputed over 4,485 cases, the mean unusual 24-hour move is +0.059 % with t 0.94 (step 5: +0.066 %, t 1.03, 4,448 cases), a strength of only 0.016 of the coin's usual 4.12 % daily move, and about 0.6 times the 0.11 % cost of a trade.
- **F2:** The effect is mixed across periods rather than steady. The mean unusual 24-hour move is +0.50 % (t 2.71, 580 cases) in 2020 and +0.35 % (t 1.75, 609 cases) in 2021, but −0.38 % (t −1.57, 553 cases) in 2018 and −0.28 % (t −1.93, 540 cases) in 2025, and only 54 % of the 24 windows have a positive mean, with a spread of 0.45 % between windows.
- **F3:** The brief's 2-to-6-hour continuation is absent. After the same cases the unusual move is −0.024 % at 2 hours (t −1.29), −0.050 % at 6 hours (t −1.54) and −0.070 % at 12 hours (t −1.55), and it turns positive only at 24 hours (+0.059 %, t 0.94), so the 24-hour reading sits on a small early fade.
- **F4:** The forecast's grading does not sort the outcomes. By forecast quartile the 24-hour unusual move is +0.11 % (q1), −0.055 % (q2), +0.15 % (q3) and +0.034 % (q4), and more than half the cases sit at the cap of 20 (q3 mean 19.3, all of q4), so the top-against-bottom check passes on a near-flat profile.
- **F5:** Recomputed from prices, hourly rises of at least 3 of their 30-day standard deviations show the clearest continuation on volume of 3 to 6 times the 30-day average: +0.68 % over 24 hours (t 2.80, 309 cases). The same rises on volume above 6 times average give +0.44 % (t 1.32, 170 cases), and on volume of 1.5 to 3 times average +0.16 % (t 0.45, 188 cases). At 6 hours the 3-to-6-times group gives +0.24 % (t 1.80, 407 cases).
- **F6:** The same-sized hourly drops are not followed by further falls over 24 hours. On volume above 6 times average they give −0.64 % in their own direction (t −1.40, 214 cases), which is a partial rebound, so the continuation shows only on the rising side.

## Ideas
- `028-01_volume-surge-up-continuation.d1_high-volume-hourly-drops-rebound.b1_heavy-volume-rises-keep-rising.b1_heavy-volume-rises-all-coins` (from F1, F2, F5): After an hour in which the coin rises far more than its typical hourly move over the past 30 days on volume several times its average hourly volume over the past 30 days, the price keeps rising over the next 24 hours. The heavier that hour's volume against its 30-day average and the larger its rise against its typical hourly move, the larger the further rise.
- `028-01_volume-surge-up-continuation.d1_high-volume-hourly-drops-rebound.b1_heavy-volume-rises-keep-rising.b2_sharp-rise-on-volume-continues` (from F4, F5, F6): After an hour in which the coin rises far more than its typical hourly move over the past 30 days, on volume several times its average hourly volume over the past 30 days, the price keeps rising over the next 24 hours. The larger that hour's rise against its typical 30-day hourly move, the larger the further rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
