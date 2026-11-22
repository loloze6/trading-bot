---
line: 7.g patterns
backtest: 023-03_flatter-range-stronger-reversion.c1_near-range-top-continuation.d1_top-of-range-continuation-only_1d
idea tested: 023-03_flatter-range-stronger-reversion.c1_near-range-top-continuation.d1_top-of-range-continuation-only
step 5: confirmed
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.4070 USD
---
## Findings
- **F1:** Across all coins, the next day's excess return falls as today's move grows: today's 1-day return divided by its 30-day volatility predicts the next day with slope -0.00184 per unit (t -4.46, 13,060 one-day cases), and the slope is negative in every coin (XMR -0.00466, t -4.93; ETH t -2.09; BTC t -1.74; LTC t -1.77).
- **F2:** This one-day reversal sits in the coin's most volatile stretches: slope -0.00531 (t -5.70, 4,355 cases) in each coin's highest tercile of 30-day volatility, -0.00125 (t -1.91) in the middle tercile and +0.00051 (t 0.96) in the lowest. After a 2-sigma day in the top tercile that is about 1 % back, against a 0.19 % trade cost.
- **F3:** The reversal is not steady over time: slope t of -3.68, -2.95 and -3.65 in 2018 to 2020 and -2.79 in 2023, but -0.79 and -0.57 in 2021 and 2022, and positive in 2024 and 2025 (+0.51, +0.37). When coins are averaged by date, the bins weaken (after a move below -2 sigma: +0.55 %, t 1.21), so part of the pooled t comes from coins moving together.
- **F4:** In coins whose 30-day trend is down (lowest tercile of 30-day log return over volatility), up days are followed by falls that grow with the size of the rise:
- **F5:** The book earns from long holds, not from the 10-day grading:
- **F6:** Over 10 days, the effect is not graded across the range: excess +3.18 % in the top decile of the 30-day range (t 2.35, 237 cases) but -2.90 % in the 0.7 to 0.8 decile (t -2.30). The weekday pattern also fades once coins are averaged by date (Friday decisions +0.28 %, t 1.68). Neither stands out from chance given the many angles looked at.
- **F7:** The book trails holding in rising years and loses less in falling ones: mean daily return 0.00175 against 0.00409 for the coins in 2021, and -0.00091 against -0.00347 in 2018.

## Ideas
- `023-03_flatter-range-stronger-reversion.c1_near-range-top-continuation.d1_top-of-range-continuation-only.g1_volatile-one-day-move-reversal` (from F1, F2, F3): The larger a coin's 1-day move measured against its 30-day volatility, the more the coin moves back the other way over the next day, and this reversal is larger the higher the coin's 30-day volatility.
- `023-03_flatter-range-stronger-reversion.c1_near-range-top-continuation.d1_top-of-range-continuation-only.g2_downtrend-rallies-fade-next-day` (from F4, F1): In a coin whose 30-day return is negative, the larger its 1-day rise against its 30-day volatility, the more it falls over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
