---
line: 7.g patterns
backtest: 021-03_thin-cloud-upward-breakout_1d
idea tested: 021-03_thin-cloud-upward-breakout
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4355 USD
---
## Findings
- **F1:** After a coin's large down day, measured against its own 20-day volatility, the next day is unusually strong, and only in volatile periods. The lowest tenth of the day's z-move is followed by +0.51 % above the coin's mean daily return (t 3.49, 1442 days), and the second tenth by +0.26 % (t 2.04). Below zero, the rank correlation between the size of the fall and the next day is negative in all 6 coins (rho -0.03 to -0.10, p < 0.05 in ETH, XMR, XRP and ZEC). Above zero there is no such relation (rho -0.05 to +0.03). In the coin's most volatile third, the lowest fifth is followed by +1.19 % (t 5.40, 900 days), about 6 times the 0.19 % cost of a round trip. In its calmest third the same days are followed by -0.13 % (t -1.08). This is the angle that stands out among the roughly 25 I looked at, but the coins share these days: averaged per day, the lowest fifth gives +0.25 % with a t of only 1.62 (965 days). It is also strongest in 2020 and 2021 (+1.2 %, t 3.4 and 3.7) and slightly negative in 2024 and 2025.
- **F2:** The rebound fades within days. Over 3 days, on non-overlapping cases, the lowest tenth gives +0.55 % (t 1.44, 448 cases), and the 8th and 9th tenths give -0.74 % and -0.76 % (t -2.26 and -2.52).
- **F3:** At the upward cloud crosses the cloud's thinness grades nothing. The raw width relative to price has a rank correlation of 0.017 (p 0.84) with the unusual 26-day return over 152 cases. The thickest third returns -1.1 % against +6.9 % and +8.9 % for the others.
- **F4:** Crosses that come after a large 26-day run-up tend to do worse, though this does not stand out from chance. The top third of prior 26-day return (mean +28 %) is followed by -2.4 % unusual return, against +9.6 % and +10.9 % for the other thirds (rho -0.18, p 0.063, 108 cases).
- **F5:** The book's held position earns its timing within the 26-day hold and not after it. On days 1 to 19 after a cross it gains 0.16 % to 0.25 % per day, against 0.106 % from the market's own rise. On days 20 to 26 it gains 0.118 % against 0.105 %. Beyond 26 days it gains 0.017 % against 0.028 %.
- **F6:** Over 26 days, nearness to the 26-day high grades the coin's unusual return. On 429 grid cases the rank correlation is 0.133 (p 0.006), with +5.0 % and +2.7 % in the two nearest fifths against -0.2 % in the farthest. This agrees with the nearness-to-highs ideas already known.
- **F7:** The weekday effects do not survive clustering by day. Saturday's next day looks strong when every coin-day is counted (+0.43 %, t 5.24). Averaged per day it is +0.23 % with t 1.43, and its sign changes across years (2018 t -2.01, 2020 t +2.87).

## Ideas
- `021-03_thin-cloud-upward-breakout.g1_volatile-market-down-day-rebound` (from F1, F2): After a daily close that falls by a large amount relative to the coin's own 20-day volatility, while that 20-day volatility is high, the coin rises over the next day. The larger the fall measured in its 20-day volatility, and the higher that volatility, the larger the next day's rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
