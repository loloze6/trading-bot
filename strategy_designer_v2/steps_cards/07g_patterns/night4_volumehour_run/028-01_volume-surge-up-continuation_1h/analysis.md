---
line: 7.g patterns
backtest: 028-01_volume-surge-up-continuation_1h
idea tested: 028-01_volume-surge-up-continuation
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3614 USD
---
## Findings
- **F1:** The next-hour return is unusually high from the closes of the bars opening at 20:00 and 21:00 UTC. Pooled over both coins the excess mean was +0.045 % (t 4.0) and +0.040 % (t 3.7), about 5,835 cases each. It holds in each coin on its own: for the bar opening at 21:00 the excess return scaled by the 30-day usual hourly move has t 3.6 in BTC and 3.4 in ETH, 2,200 cases each. These are the only two hours out of 24 at |t| > 3.4.
- **F2:** That two-hour rise depends on the previous 24 hours. Measured from the close of the bar opening at 19:00 UTC, the excess return over the next two hours was +0.133 % (t 2.6, 880 cases) after the bottom quintile of the 24-hour move scaled by the usual move, and +0.076 % (t 2.0) after the second quintile. It was −0.004 % (t −0.1) in the middle quintile, −0.067 % (t −2.1) in the fourth and −0.029 % (t −0.8) in the top. So the larger the prior fall, the larger the evening rise.
- **F3:** The evening two-hour rise is positive in both coins overall: BTC +0.036 % (t 1.85) and ETH +0.051 % (t 2.09), 2,918 cases each. By year it is positive in 7 of 8 years for BTC and 6 of 8 for ETH, but significant only in 2020 (t 3.0 and 2.6). Its mean of about +0.04 to +0.09 % is below the 0.11 % cost of a trade unless it is concentrated by the prior 24-hour fall.
- **F4:** Over 24-hour non-overlapping cases there is a graded reversal. The excess next-24-hour return falls from +0.32 % (t 1.99, 865 cases) after the bottom quintile of the scaled 24-hour move to −0.21 % (t −1.6) and −0.16 % (t −1.3) after the top two quintiles. The bottom quintile is positive in both coins (BTC +0.31 %, t 1.6; ETH +0.33 %, t 1.3). Given how many angles were examined, this is suggestive only.
- **F5:** The tested situation does not stand out. Signed 6-hour continuation after hours beyond 2.5 usual moves was +0.19 % (t 0.6) in BTC and +0.30 % (t 0.9) in ETH when volume was more than 3 times its 30-day mean, and −0.43 % (t −1.2) in ETH at 1.5 to 3 times. Up-hours of 1.5 to 2.5 usual moves on more than 3 times volume gave +0.59 % (t 2.0, 99 cases), a lone cell among 25 that is indistinguishable from chance.
- **F6:** The book's losses come from the years the coins fell. Its mean daily return was −0.28 % (t −4.0) in 2018 and −0.33 % (t −3.3) in 2022, against −0.10 % to +0.16 % (|t| < 1.6) in the other six years. It was long on 68 % of bars at a mean allocation of 0.49, so this long-only book mostly carried the market's drift rather than a timing gain.
- **F7:** The next-hour return is low from the closes of the bars opening at 00:00 to 02:00 UTC. The excess was −0.022 % (t −2.0), −0.023 % (t −2.2) and −0.032 % (t −3.3), with the 02:00 bar negative in both BTC (t −2.8) and ETH (t −2.1). The book's gross gain per bar was negative in those hours (−1.28, −0.60 and −1.24 bp).

## Ideas
- `028-01_volume-surge-up-continuation.g1_evening-rebound-after-daily-fall` (from F1, F2, F3): In the two hours after 20:00 UTC, a coin rises, and the further it has fallen over its past 24 hours (measured against its usual 24-hour move), the larger that rise.
- `028-01_volume-surge-up-continuation.g2_daily-move-reverses-next-day` (from F4, F5): Over the next 24 hours a coin moves against its past 24-hour return, and the larger that return in usual 24-hour moves, the larger the move back.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
