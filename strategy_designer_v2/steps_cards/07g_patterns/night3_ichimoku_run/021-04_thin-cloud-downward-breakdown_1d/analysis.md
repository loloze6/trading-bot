---
line: 7.g patterns
backtest: 021-04_thin-cloud-downward-breakdown_1d
idea tested: 021-04_thin-cloud-downward-breakdown
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3699 USD
---
## Findings
- **F1:** The coin's own 14-day return predicts its next 7 days in the same direction: over 2141 non-overlapping 7-day cases on 6 coins, a case signed by the 14-day return beats the coin's normal drift by 1.08 % (strength 0.080, t 3.80). The most-risen fifth beats it by 2.09 %. The rank slope has t 3.88, with t 1.98 in windows w1–w12 and t 3.31 in w13–w24. Its sign is positive on 6 of 6 coins, with per-coin slope t from 0.15 (LTC) to 2.45 (ZEC). I compared about 25 features and horizons, and this is the one that stands out most.
- **F2:** This continuation is about 5.7 times this backtest's 0.19 % round trip from the unusual move alone (1.08 % per case). That fits the earlier finding F11 that ideas large enough to pay cover the cost by about 4 times.
- **F3:** The continuation is uneven across years: the 14-day slope t is 3.00 in 2020 and 1.71 in each of 2019, 2022 and 2025, but −0.29 in 2018, 0.00 in 2021 and −0.59 in 2023.
- **F4:** It fades by 14 days: the 14-day return against the next 14 days has slope t −0.01 (1001 cases, signed strength −0.008).
- **F5:** A single large day keeps going for a week. A one-day return measured against the past 14 days' volatility is followed by a 7-day unusual move in its direction of 0.73 % per case (strength 0.057, t 2.64, 1998 cases). The slope t is 1.81 in w1–w12 and 2.55 in w13–w24, and the sign is positive on 5 of 6 coins.
- **F6:** Saturdays rise more than the coin's average day: by 0.32 % (t 3.93, 2467 coin-days), positive on 6 of 6 coins (BTC only +0.04 %) and in 6 of 8 years. Thursdays fall below it by 0.30 % (t −2.74). Over 7 weekdays these are among many comparisons, and neither is a graded situation.
- **F7:** The tested short book lost mostly the coins' rise, not to timing. Its mean daily return was +0.053 % in 2018 and +0.017 % in 2022 (the two years the coins fell, −0.34 % and −0.18 % a day), but negative in every bull year (−0.224 % in 2023). Per case, the normal drift against the short was −4.39 % against an unusual move of −0.19 %.
- **F8:** The tested book's trades lost on every coin. Its 699 trades, held about 23.9 days, had a mean net result of −2.2 % (BTC) to −17.3 % (XRP) and only 28 to 41 % of them winners. The forecast's size at entry barely relates to the result (correlation 0.079), so cloud thinness did not grade the outcome.

## Ideas
- `021-04_thin-cloud-downward-breakdown.g1_two-week-momentum-one-week-follow-through` (from F1, F2, F3, F4): The larger a coin's 14-day return, in either direction, the larger its move in the same direction over the next 7 days, beyond its normal drift.
- `021-04_thin-cloud-downward-breakdown.g2_large-day-shock-continues-weekly` (from F5, F2): The larger a coin's one-day return relative to its daily volatility over the past 14 days, in either direction, the larger its move in the same direction over the next 7 days, beyond its normal drift.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
