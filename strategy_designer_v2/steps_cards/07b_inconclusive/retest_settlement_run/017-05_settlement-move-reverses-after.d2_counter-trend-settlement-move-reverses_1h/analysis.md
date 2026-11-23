---
line: 7.b inconclusive
backtest: 017-05_settlement-move-reverses-after.d2_counter-trend-settlement-move-reverses_1h
idea tested: 017-05_settlement-move-reverses-after.d2_counter-trend-settlement-move-reverses
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3827 USD
---
## Findings
- **F1:** The tested move is clear over the first 2 hours after settlement and fades by 8 hours: on the settlement cases signed by the 24-hour trend, the raw return has t 4.03 at 1 hour, 5.67 at 2 hours, 3.04 at 4 hours and only 1.41 at 8 hours (the plan's horizon), then turns to t -2.69 at 16 hours (21,059 cases). The plan's 8-hour test measured the idea where most of the move has already been given back.
- **F2:** Over 2 hours the counter-trend pre-move reverses at the settlements, with a strength of 0.039 of a usual 2-hour move against 0.017 at other hours (excess +0.056 % against +0.025 %). At the 8-hour horizon the strength is 0.0078 against 0.0021, near the 0.007 the verdict gives.
- **F3:** Over 2 hours the move grows with the 24-hour trend, as the idea says, but over 8 hours it does not. By quintile of the trend's size the 2-hour excess rises from -0.003 % (t -0.19) to +0.080 % (t 3.66) and +0.139 % (t 4.33), with a slope of 0.0079. The 8-hour quintiles are flat and noisy: +0.005 %, +0.042 %, -0.013 %, +0.031 %, +0.065 %, all with |t| ≤ 1.24.
- **F4:** The 8-hour measure is swamped by the time of day, not by the settlement itself. The cases closing at 08:00 UTC lose -0.152 % (t -4.58), while those at 00:00 gain +0.090 % (t 3.03) and those at 16:00 gain +0.159 % (t 4.70). The same counter-trend cases at hours with no settlement follow a smooth daily cycle, from -0.160 % (t -5.11) at 07:00 to +0.143 % (t 4.90) at 23:00.
- **F5:** Even at 2 hours the effect is not specific to the settlement clock times, and it is missing at one of them. The 08:00 settlement shows -0.017 % (t -1.04), while the hours without settlement next to the other two are as strong or stronger: 22:00 +0.103 % (t 6.64), 15:00 +0.093 % (t 4.63), 01:00 +0.093 % (t 5.83).
- **F6:** The 2-hour reversal is broad across coins and years but not uniform. It is positive in all six coins, with t from 0.65 (XMR) to 3.44 (ZEC), and in seven of eight years. It is absent in 2022 (-0.030 %, t -1.26) and 2023 (-0.004 %, t -0.26).
- **F7:** The tested 8-hour result is on the predicted side but weak, and it splits by side and coin. The mean is +0.026 % with t 1.25 over 17,689 cases. By side, the long dip-in-uptrend cases give +0.011 % (t 0.42) and the short rally-in-downtrend cases +0.042 % (t 1.52). By coin, BTC is negative (-0.014 %) and ZEC highest (+0.077 %, t 1.32).
- **F8:** The size is far below the cost of a trade at either horizon. The 8-hour total move is +0.02 % per case and the 2-hour excess about +0.056 %, against 0.19 % for a buy and a sell. Neither horizon could make the book pay as it is; the book's Sharpe was -0.83.

## Ideas
- `017-05_settlement-move-reverses-after.d2_counter-trend-settlement-move-reverses.b1_settlement-reversal-more-coins` (from F7): The return over the 8 hours after each funding settlement time runs opposite to the return over the 2 hours before it when that pre-move runs against the coin's 24-hour trend, and the stronger the 24-hour trend, the larger the move back.
- `017-05_settlement-move-reverses-after.d2_counter-trend-settlement-move-reverses.b2_two-hour-settlement-snapback` (from F1, F2, F3, F5, F6, F8): The return over the 2 hours after each funding settlement time runs opposite to the return over the 2 hours before it when that pre-move runs against the coin's 24-hour trend, and the stronger the 24-hour trend, the larger the move back.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
