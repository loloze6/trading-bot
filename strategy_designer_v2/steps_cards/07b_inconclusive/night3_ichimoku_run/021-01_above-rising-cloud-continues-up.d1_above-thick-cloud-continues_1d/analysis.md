---
line: 7.b inconclusive
backtest: 021-01_above-rising-cloud-continues-up.d1_above-thick-cloud-continues_1d
idea tested: 021-01_above-rising-cloud-continues-up.d1_above-thick-cloud-continues
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3537 USD
---
## Findings
- **F1:** The test's result lies on the opposite side from the idea, and the level is weak. The thickness forecast's slope on the 26-day excess return is -0.0083 (t -1.26, 149 independent in-regime cases). Bars above a rising cloud beat the coin's normal 26-day drift by +4.8 % (t 1.30). Bars outside the regime trail it by -1.7 % (in minus out, Welch t 1.66).
- **F2:** Thickness does not grade the move. On 26 days, the forecast quartiles go from thinnest to thickest cloud (mean width 2.5 %, 4.7 %, 6.0 %, 8.0 % of the price). Their excess returns are +16.2 %, -1.4 %, +3.0 % and +1.0 %. The thinnest quartile's spread is 0.74, against about 0.29 for the others. So the negative slope comes from a few very large moves above thin clouds (t of that quartile about 1.35 on 38 cases), not from a steady gradient.
- **F3:** The effect is mixed across coins and years. The forecast's t per coin at 26 days is +0.91 (BTC), +1.28 (LTC), -0.82 (ETH), -0.34 (XMR), -0.51 (XRP) and -1.71 (ZEC). ZEC alone has an excess return of +21.3 % on 17 cases. The in-regime excess return per year changes sign: -11.9 %, +9.3 %, -7.1 %, +8.1 %, -15.8 %, -2.3 %, +9.4 %, +25.2 % from 2018 to 2025, with 5 to 34 cases a year.
- **F4:** The only horizon where thickness grades clearly is the shortest, and there it works against the idea. The forecast's t on the excess return is -2.27 over 5 days (852 cases), -1.10 over 10 days (421), -1.26 over 26 days (149) and +1.01 over 52 days (85). Above a rising cloud, the thinner the cloud, the larger the next days' rise.
- **F5:** The supporting check could not be run on this data (0 cases), so the test could not have confirmed the idea even with a positive slope. The windows are about 122 daily bars long (2,921 bars over 24 windows). The 52-day span, displaced 26 days, plus the 26-day slope need about 104 bars. So the cloud slope could be recomputed on none of the 26-day grid cases, and the cloud position on only 38 of 149.
- **F6:** Size is not what limits this idea. The unusual move is +3.25 % per case over 26 days (strength 0.093, about twice the usual 0.05 of F10). The total move is +7.13 %, against a round-trip cost of 0.19 % (16.8 and 36.9 times the cost). Yet the book's Sharpe of 0.51 trails holding the coins by 0.046, because the gain is mostly the coins' own drift (+3.88 % of the +7.13 %).

## Ideas
- `021-01_above-rising-cloud-continues-up.d1_above-thick-cloud-continues.b1_thin-cloud-short-rise` (from F4, F2, F1): When a coin closes above its Ichimoku cloud and the cloud is rising, its return over the next 5 days is larger the thinner the cloud (the gap between its two spans as a share of the price).

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
