---
line: 7.b inconclusive
backtest: 027-02_panic-fall-depth-rebound.d2_confirmed-panic-bounce-continues.b1_panic-bounce-more-coins_4h
idea tested: 027-02_panic-fall-depth-rebound.d2_confirmed-panic-bounce-continues.b1_panic-bounce-more-coins
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4196 USD
---
## Findings
- **F1:** The tested slope's positive t comes from a few extreme cases. On the same 463 cases the rank correlation of bounce with 84-bar excess return is 0.001 (p 0.98), the slope after winsorising the excess return at 2 %/98 % has t 0.32, and removing the 10 highest-leverage cases (4 of them ZEC) turns it negative (slope -0.000666, t -1.81, 453 cases).
- **F2:** One coin carries the positive slope. ZEC alone gives slope 0.011048 with t 4.74 on 40 cases, while the other 18 coins together give slope -0.000128 with t -0.33 and rho 0.005 on 423 cases. No other coin has |t| above 1.82.
- **F3:** The effect is not stable over time. Without ZEC, the slope is negative in every year from 2018 to 2023 (t from -0.10 to -1.72) and in 2025 (t -1.44), and positive only in 2024 (t 2.48, 79 cases).
- **F4:** The splits that look strong do not hold up. For the smallest panic falls (mean -3.2 %) the slope has t 4.48, but without ZEC it is only t 1.24. Among stretch-range terciles, only the middle one has t 2.37 (rho 0.19); the widest-range tercile has rho -0.15. No subset shows the effect cleanly.
- **F5:** Bounce size predicts the next 24 hours, in the opposite direction to the idea. The slope of the raw 24-hour return after the case bar on the bounce is -0.000634 with t -4.17 on 507 cases, about -3.1 % across the spread from the bottom bounce quintile (-17.8) to the top one (+31.1). The relation is gone by 3 days (t -0.06) and 7 days (t -0.10).
- **F6:** Over the plan's 14-day horizon, panic cases as a whole earn less than the coin's normal drift. The unusual move is -1.28 % per case (strength -0.041), which is -5.7 times the 0.22 % cost of a trade. Cases with a positive bounce average +0.75 % excess (t 0.62, 278 cases) and those with a negative bounce -0.46 % (t -0.34, 185 cases).

## Ideas
- `027-02_panic-fall-depth-rebound.d2_confirmed-panic-bounce-continues.b1_panic-bounce-more-coins.b1_post-panic-bounce-fades-next-day` (from F5, F1): Among 24-hour stretches where a coin's range is several times its 30-day average and the coin fell, the larger the coin's rise over the 24 hours after the stretch, the lower its return over the following 24 hours.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
