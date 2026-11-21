---
line: 7.b inconclusive
backtest: 021-04_thin-cloud-downward-breakdown.d1_cloud-breakdown-after-deep-fall_1d
idea tested: 021-04_thin-cloud-downward-breakdown.d1_cloud-breakdown-after-deep-fall
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3459 USD
---
## Findings
- **F1:** The tested short after a downward cloud break with a falling 26-day return shows almost no effect over its 26-day horizon: the unusual move in the short direction is +0.68 % per case (t 0.32, 128 cases, 55 % hit), which matches step 5's +0.70 % (t 0.30, 112 cases), and the total move after the coins' upward drift is -3.45 %, so the short loses before its 0.19 % cost.
- **F2:** The depth of the prior 26-day fall does not grade the outcome: the correlation of the 26-day unusual move with the prior 26-day return is -0.0007, its terciles give +1.1 %, -2.6 % and -0.7 % (t 0.21, -0.53, -0.19), and by forecast size the middle third is +8.5 % (t 2.95, 36 cases) while the low and high thirds are -1.1 % and -3.8 %, which is not graded; step 5's slope is -0.0029.
- **F3:** The small positive mean comes from one bear year: in 2018 the 26-day unusual move is +21.9 % (t 4.44, 15 cases, 80 % hit) and +35.9 % over 52 days (t 6.6, 12 cases); without 2018 it is -2.1 % (t -0.95, 113 cases), and 2021 to 2023 are each about -7.6 % to -10.3 %.
- **F4:** The effect is mixed across coins at 26 days: ZEC +9.8 % (t 1.24, 18), XRP +4.0 % (t 0.68, 25), BTC +2.1 %, LTC -0.5 %, ETH -1.8 % and XMR -6.2 % (t -1.53, 28, 29 % hit).
- **F5:** The effect is larger at a longer horizon than the plan's: the unusual move is +0.2 % at 5 days (t 0.21, 156 cases), +1.6 % at 10 days (t 1.36), +0.7 % at 26 days (t 0.32) and +4.7 % at 52 days (t 1.59, 100 cases, 59 % hit).
- **F6:** Over 52 days the fall is graded by how fast the 26-day high-low midpoint (the kijun) was already falling over the past 10 days: the steepest third gives +18.0 % (t 3.15, 16 cases, 81 % hit), the middle third +0.7 % (t 0.10, 15) and the rising third -2.4 % (t -0.33, 15); at 26 days the same split is not clear (+2.4 %, -7.7 %, +4.1 %).
- **F7:** Cloud thickness and cloud slope could be measured on only 7 to 15 cases inside the windows' history, too few to read; the thin-cloud third gives +7.1 % (t 1.13, 7 cases) against +0.4 % for the thick third.

## Ideas
- `021-04_thin-cloud-downward-breakdown.d1_cloud-breakdown-after-deep-fall.b1_breakdown-under-sliding-kijun` (from F1, F2, F3, F5, F6): After a daily close that crosses down from above a coin's Ichimoku cloud to below it, while its 26-day return is already a fall, the coin falls over the next 52 days, only while the midpoint of its 26-day highest high and lowest low has been falling over the past 10 days, and the steeper that 10-day decline of the midpoint at the cross, the larger the fall that follows.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
