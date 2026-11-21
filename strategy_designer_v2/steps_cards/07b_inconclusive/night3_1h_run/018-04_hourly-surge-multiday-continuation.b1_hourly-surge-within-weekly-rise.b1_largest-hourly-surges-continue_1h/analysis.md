---
line: 7.b inconclusive
backtest: 018-04_hourly-surge-multiday-continuation.b1_hourly-surge-within-weekly-rise.b1_largest-hourly-surges-continue_1h
idea tested: 018-04_hourly-surge-multiday-continuation.b1_hourly-surge-within-weekly-rise.b1_largest-hourly-surges-continue
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.5131 USD
---
## Findings
- **F1:** The test's near-zero result comes from dilution by ordinary surges. Cases whose 24-hour return was at least twice its 30-day average absolute daily return had an unusual move of +1.86 % over 5 days (t 2.69, 341 cases) and +2.27 % over 10 days (t 2.14). The 2,018 cases below twice usual had −0.22 % (t −0.93). Over half of all cases (1,285 of 2,539) carried a forecast of 5 or less and averaged −0.32 % over 5 days.
- **F2:** Inside the largest surges the move is roughly graded with the surge's size, but the effect is absent below twice usual. Over 5 days the strength is 0.19 for 2 to 2.5 times usual, 0.01 for 2.5 to 3, 0.34 for 3 to 4 and 0.30 above 4. It is −0.01 to −0.08 for every bucket below 2, and the rank correlation over all cases is only 0.05 (2,261 cases).
- **F3:** The surges of twice usual or more are large enough to pay. Their unusual move of +1.86 % per case is about 10 times the 0.19 % cost of a buy and a sell, and their total move is +2.53 %. The tested idea's pooled unusual move of +0.12 % was 0.6 times that cost.
- **F4:** The 7-day condition carries the effect. Among all hourly surges of twice usual or more, read from prices alone, those in a rising week had an unusual 5-day move of +1.12 % (t 2.99, 1,230 cases). Those in a falling week had −0.24 % (t −0.62, 738 cases).
- **F5:** The large-surge effect is not one period's. It is +2.03 % (t 1.52, 129 cases) in 2018 to 2021 and +1.76 % (t 2.30, 212 cases) in 2022 to 2025. It is also +1.72 % with the 30-day return down (185 cases) and +2.03 % with it up (156 cases).
- **F6:** Most coins carry the large-surge effect, but not all. Over 5 days it is BTC +2.79 % (t 3.01, 53 cases), ETH +3.93 % (t 2.34, 51), LTC +3.43 % (t 1.92, 52), XRP +1.73 % (t 0.86, 73) and ZEC +0.18 % (65). XMR is −0.67 % (47).
- **F7:** Over the tested idea's own cases the market's year-to-year moves are larger than the effect itself. The 5-day unusual move of all cases is −1.65 % in 2018 (t −1.78), +1.71 % in 2020 (t 2.73) and −2.24 % in 2022 (t −4.05).

## Ideas
- `018-04_hourly-surge-multiday-continuation.b1_hourly-surge-within-weekly-rise.b1_largest-hourly-surges-continue.b1_largest-hourly-surges-keep-rising` (from F1, F2, F3, F4, F5): When a coin's 24-hour return, read at an hourly close, reaches twice its 30-day average absolute daily return or more on the upside, the price keeps rising over the next 5 days by more than the coin's usual 5-day return, only while its 7-day return is positive. The further that 24-hour return goes beyond twice its usual daily move, the larger the rise.
- `018-04_hourly-surge-multiday-continuation.b1_hourly-surge-within-weekly-rise.b1_largest-hourly-surges-continue.b2_largest-surges-on-more-coins` (from F1, F4, F6): When a coin's 24-hour return, read at an hourly close, reaches twice its 30-day average absolute daily return or more on the upside, the price keeps rising over the next 5 days by more than the coin's usual 5-day return, only while its 7-day return is positive. The further that 24-hour return goes beyond twice its usual daily move, the larger the rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
