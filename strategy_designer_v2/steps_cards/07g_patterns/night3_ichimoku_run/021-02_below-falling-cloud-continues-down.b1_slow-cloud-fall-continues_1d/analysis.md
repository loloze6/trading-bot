---
line: 7.g patterns
backtest: 021-02_below-falling-cloud-continues-down.b1_slow-cloud-fall-continues_1d
idea tested: 021-02_below-falling-cloud-continues-down.b1_slow-cloud-fall-continues
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4022 USD
---
## Findings
- **F1:** The day after a coin's daily fall, its return beats its normal drift, and the deeper the fall the larger the rebound: over all six coins the next day's excess return is +0.20 % after falls of 0.5 to 1 usual daily moves (n 2067, t 1.8), +0.40 % after 1 to 1.5 (n 899, t 2.3), +0.61 % after 1.5 to 2 (n 484, t 2.2), +0.66 % after 2 to 3 (n 275, t 1.6) and +4.0 % after falls beyond 3 (n 109, t 3.8), against -0.10 % after small falls (n 4656).
- **F2:** The graded rebound after falls holds coin by coin: the rank correlation between the size of a down day and the next day's excess return is negative in all six coins (-0.055 BTC, -0.086 ETH, -0.057 LTC, -0.131 XMR, -0.103 XRP, -0.093 ZEC; p from 0.038 down to 0.000002, about 1,350 to 1,450 down days each).
- **F3:** The rebound is not one period's: the next-day excess after falls beyond 2 usual moves is positive in 6 of 8 years (+1.1 % 2018, +2.0 % 2019 t 2.8, +3.9 % 2020 t 2.2, +2.5 % 2021 t 2.4, +3.3 % 2024), it is near zero in 2022, 2023 and 2025, and the fall-to-next-day rank correlation is negative in 7 of 8 years.
- **F4:** The rebound is large against the cost of a trade: +0.61 % per case after falls of 1.5 to 2 usual moves is about 3 times the backtest's 0.19 % round trip, and +4.0 % after falls beyond 3 is about 21 times it. It lasts about a day: a 3-day fall is not followed by a 3-day rebound (-0.51 % excess after 3-day falls beyond 2 usual moves, n 125, t -0.47).
- **F5:** Large daily rises are followed by a next day below the coin's drift: -0.47 % after rises of 2 to 3 usual moves (n 341, t -1.4) and -0.89 % beyond 3 (n 169, t -1.6). By coin, after rises beyond 2 usual moves it is -0.84 % for BTC (t -2.2), -1.2 % for ETH (t -2.3), -2.0 % for XMR (t -3.2) and -0.87 % for LTC (t -1.4), but +1.2 % for ZEC. This is weaker and less consistent than the rebound after falls.
- **F6:** The book's own extremes are reversal days: its best 1 % of days come when the coin falls 8.9 % and the coin then rises 0.78 % the next day, against a 0.12 % usual next day. Its worst 1 % come when the coin rises 9.1 % and the coin then falls 0.51 % the next day. The short-below-a-falling-cloud book gains on the fall and gives part of it back on the rebound.
- **F7:** Saturdays carry an excess return that stands out among the seven weekdays: +0.45 % mean (n 2484, t 5.5), positive for all six coins and in 7 of 8 years (t above 2.2 in 2019, 2020, 2024 and 2025). Thursdays are the weakest day (-0.18 %, t -1.6). A weekday is a condition, not a graded situation, so no idea is written from it.
- **F8:** The tested situation shows no downward continuation at 26 days: the below-a-falling-cloud cases ended 1.5 % above the drift in the short direction (156 cases, t -0.69). Neither the 26-day past return, the 26-day volatility nor the position in the 26-day range separates the next 26 days (rank correlations 0.06 to 0.09, p ≥ 0.06).

## Ideas
- `021-02_below-falling-cloud-continues-down.b1_slow-cloud-fall-continues.g1_next-day-rebound-after-falls` (from F1, F2, F3, F4, F6): When a coin falls over a day, its return over the next day is above its normal drift, and the larger the day's fall relative to the coin's usual daily move, the larger that rebound.
- `021-02_below-falling-cloud-continues-down.b1_slow-cloud-fall-continues.g2_next-day-giveback-after-rises` (from F5, F6): When a coin rises over a day, its return over the next day is below its normal drift, and the larger the day's rise relative to the coin's usual daily move, the larger that shortfall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
