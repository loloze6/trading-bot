---
line: 7.g patterns
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side_1d
idea tested: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.3626 USD
---
## Findings
- **F1:** The larger a coin's one-day fall measured against its own 20-day volatility, the larger the next day's return, and the effect is graded across the deciles: the lowest decile is followed by a mean next-day return of 0.0064 (t 4.35, n 1400), the second by 0.0038 (t 3.10), the third by 0.0016 (t 1.20), and the middle deciles by about 0.0003 to 0.0009 (t below 1.2).
- **F2:** This rebound after a large fall shows in every coin and every year, so it is not carried by one coin or one period: next-day means after the lowest decile run from 0.0037 (BTC) to 0.0100 (XMR, t 3.33), all positive, and from 0.0005 (2024) to 0.0163 (2020, t 3.04), all eight years positive.
- **F3:** The rebound holds in both regimes the strategy uses. It is 0.0050 (t 3.58, n 1186) in the trending state and 0.0052 (t 3.96, n 1610) in the flat state, so it is independent of the 30-day-return filter the idea relies on.
- **F4:** The rebound is short-lived. On a non-overlapping 3-day grid, the lowest quintile of scaled daily moves gains only 0.0039 excess over 3 days (t 1.29, n 920), against the one-day effect in F1, so most of the bounce lands on the first day.
- **F5:** The bars on which the book stands flat lag the coin's own average, and this is the side the long-only design avoids: their 7-day excess return is -0.0070 (t -1.96, n 1179), against +0.0069 (t 1.71, n 1199) on forecast > 0 bars. Five of six coins show the same split; XMR is the exception.
- **F6:** The idea's gain depends heavily on the year. Forecast > 0 grid bars earn a 7-day excess of 0.027 (t 2.57) in 2020 and 0.034 (t 2.29) in 2021, but lose 0.057 (t -3.85) in 2018 and 0.018 (t -1.93) in 2022.
- **F7:** Saturday is the strongest weekday for the coins: mean daily return 0.0044 (t 5.39, n 2416), positive in all six coins and in seven of eight years. It is a calendar pattern with no graded situation, so it does not lead to an idea here.
- **F8:** A day with very low volume against its 20-day mean is followed by a weak week (lowest quintile 7-day excess -0.0157, t -3.10, n 394), but the quintiles above it are not ordered (+0.0084, -0.0056, +0.0108, +0.0062). After the many angles examined, this is too ungraded to count as a basis for an idea.

## Ideas
- `013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.g1_next-day-rebound-after-sharp-falls` (from F1, F2, F3, F4): The larger a coin's one-day fall relative to its own 20-day volatility of daily returns, the higher its return over the next 1 day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
