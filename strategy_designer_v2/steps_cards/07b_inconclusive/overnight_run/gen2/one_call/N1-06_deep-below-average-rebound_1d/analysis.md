---
line: 7.b inconclusive
backtest: N1-06_deep-below-average-rebound_1d
idea tested: N1-06_deep-below-average-rebound
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3449 USD
---
## Findings
- **F1:** Across the 201 non-overlapping deep cases (forecast ≥ 5), the mean excess 10-bar return is only +0.0099 with a hit rate of 52% and t = 0.88. These cases fall on just 97 distinct dates, and once they are clustered by date the t drops to 0.23, so the pooled effect is small and largely one shared market move counted several times.
- **F2:** The market's own move drowns the coin-level signal. Among the non-BTC deep cases, the coin's 10-bar return correlates 0.66 with BTC's return over the same bars, BTC itself averages +0.012 there, and the alt-minus-BTC excess is +0.015 with t = 1.49 (n = 162).
- **F3:** Depth below the SMA200 does not drive the rebound. Within the deep cases the deepest raw-distance tercile earns +0.001 (hit 45%, n = 67), against +0.012 for the shallowest (hit 60%). The forecast bucket 5–10 is also negative at −0.005 (n = 99), even though the overall slope is positive.
- **F4:** The rebound sits in deep cases that also fell sharply over the prior 10 bars. Deep cases that fell 15% or more earn +0.049 excess (hit 59%, t = 1.96, n = 56, 29 dates, date-clustered t = 1.11). The other 145 deep cases earn −0.005 (t = −0.44). The tercile that fell most earns +0.045 (t = 1.89, n = 61).
- **F5:** The crash rebound is strongest when realised volatility is also high. Deep, crashed and wild cases earn +0.091 excess (hit 58%, t = 2.13, n = 31, only 14 dates, clustered t = 1.38). Deep, crashed and calm cases earn +0.005 (n = 7).
- **F6:** The deep crash rebound is unstable across periods, which is why the plain test stays unclear. It is +0.120 in 2018 (n = 19, 6 dates) but −0.007 in 2022 (n = 22, 12 dates). All deep cases in 2019 earn −0.026 (t = −2.03, n = 26), while those in 2020 earn +0.101 (n = 8).
- **F7:** The crash rebound is not specific to one coin. Deep crash cases are positive in 5 of 6 coins: LTC +0.054 (n = 11), XRP +0.157 (n = 7), ZEC +0.028 (n = 14), ETH +0.039, XMR +0.040. BTC is the exception at −0.008 (n = 6).

## Ideas
- `N1-06_deep-below-average-rebound.b1_crash-below-average-rebound` (from F1, F3, F4, F7): When a coin's daily close is far below its 200-day average and the coin has also just fallen sharply over the last two weeks, its price rises over the next ten days more than its usual drift.
- `N1-06_deep-below-average-rebound.b2_high-volatility-capitulation-rebound` (from F4, F5, F6): When a coin is far below its 200-day average after a sharp two-week fall and its recent daily swings are unusually large, its price rises over the next ten days more than its usual drift.
- `N1-06_deep-below-average-rebound.b3_altcoin-rebound-versus-bitcoin` (from F1, F2, F4, F7): When an altcoin is far below its 200-day average after a sharp two-week fall, its price rises over the next ten days more than Bitcoin's over the same ten days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
