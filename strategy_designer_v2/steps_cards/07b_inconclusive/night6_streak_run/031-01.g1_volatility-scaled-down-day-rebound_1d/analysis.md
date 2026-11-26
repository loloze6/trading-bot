---
line: 7.b inconclusive
backtest: 031-01.g1_volatility-scaled-down-day-rebound_1d
idea tested: 031-01.g1_volatility-scaled-down-day-rebound
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3113 USD
---
## Findings
- **F1:** The effect is strongest one day after the fall and fades by the plan's 3-day horizon: the day-clustered slope t is 3.48 at 1 day (17,380 grid bars, 2,898 days), 1.62 at 2 days, 1.05 at 3 days (5,723 bars, 1,034 days, step 5's own result), 0.02 at 5 days and 1.11 at 10 days.
- **F2:** At 1 day the rebound grows with the depth of the fall. The unusual move in usual moves is +0.010 after a fall of 0 to 1 usual daily move (5,487 cases), +0.099 after a fall of 1 to 2 (1,314 cases, t 3.27), +0.194 after a fall of 2 to 3 (280 cases, t 3.32) and +0.379 after a fall beyond 3 (84 cases, t 1.77).
- **F3:** The 1-day effect is on the predicted side in all six coins, with clustered t of 1.48 for BTC, 1.84 for ETH, 2.30 for LTC, 2.29 for ZEC, 3.25 for XRP and 5.04 for XMR.
- **F4:** At 3 days the result is on the predicted side but too small to show: a slope of +0.0040 with t 1.05, and a size of +0.10 % per case, which is 0.012 of a usual move with t 0.43 over 1,471 days and 4,415 cases. Five of six coins have a positive slope (ETH −0.34), but no coin's t exceeds 1.7.
- **F5:** Much of the 3-day slope comes from the extreme falls beyond 3 usual moves. There are only 28 of them, with a mean of +0.63 usual move, positive in all six coins. Leaving them out drops the 3-day clustered t from 1.05 to 0.72, while the 1-day t barely moves (3.48 to 3.45).
- **F6:** At 3 days the result varies by year: the plain t is 3.26 in 2020, 1.56 in 2021 and 1.43 in 2025, against −1.16 in 2018 and −0.36 in 2024.
- **F7:** The 30-day trend does not separate the 3-day effect clearly. The clustered t is 1.30 when the coin's 30-day return is positive (2,187 bars) and 0.51 when it is negative (3,536 bars).

## Ideas
- `031-01.g1.b1_down-day-rebound-more-coins` (from F4, F5): The larger a coin's one-day fall, measured against its own daily volatility over the past 60 days, the more it rises above its normal drift over the next 3 days.
- `031-01.g1.b2_next-day-down-close-rebound` (from F1, F2, F3): The larger a coin's one-day fall, measured against its own daily volatility over the past 60 days, the more it rises above its normal drift over the next 1 day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
