---
line: 7.g patterns
backtest: 027-02_panic-fall-depth-rebound.d2_confirmed-panic-bounce-continues_4h
idea tested: 027-02_panic-fall-depth-rebound.d2_confirmed-panic-bounce-continues
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4189 USD
---
## Findings
- **F1:** The 4-hour bar opening at 16:00 UTC rises more than any other block of the day: +0.099 % on average over 17506 bars pooled (t 6.64). It is positive in all six coins (t 1.94 to 3.59; mean +0.069 % in BTC up to +0.154 % in ZEC, against about +0.01 % in the other blocks) and in all eight years (t 0.62 to 4.00).
- **F2:** Saturday is the strongest UTC day: the coins' mean daily return is +0.454 % over 2484 coin-days (t 5.53). It is positive in all six coins (t 2.15 to 2.92) and has t ≥ 1.93 in six of eight years, with 2022 (t 0.42) and 2023 (t −0.01) the exceptions.
- **F3:** The block opening at 20:00 UTC falls on average, −0.049 % per bar (t −3.18). Its sign flips across years (2018 t −5.04, 2022 t −3.66, 2024 t +2.56), so it is not a stable pattern.
- **F4:** The panic itself carries no premium on the 84-bar grid.
- **F5:** The book's gain comes from its long side.
- **F6:** The coin's 7-day return predicts its next 14 days pooled: slope t 3.07 on 1008 cases, bottom quintile −3.48 % (t −2.57), top +3.64 %. Once scaled by volatility the slope has t 1.84, by coin t runs from −0.41 to 1.90, and by year the sign flips (2020 t +2.93, 2022 t −1.96). Given how many angles were tried, this does not stand out from chance.
- **F7:** The next 24 hours after a single 4-hour shock barely differ by shock size: +0.21 % after the largest falls (t 1.24) against +0.11 % after the largest rises (t 0.64). This is no usable reversal.

## Ideas
- `027-02_panic-fall-depth-rebound.d2_confirmed-panic-bounce-continues.g1_us-afternoon-block-rises` (from F1): Each coin tends to rise during the 4 hours from 16:00 to 20:00 UTC, by an amount that grows with the size of its usual 4-hour move (the more volatile the coin over its past 30 days, the larger that afternoon rise).
- `027-02_panic-fall-depth-rebound.d2_confirmed-panic-bounce-continues.g2_saturday-drift-up` (from F2): Each coin tends to rise over the UTC Saturday, by an amount that grows with the size of its usual daily move over its past 30 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
