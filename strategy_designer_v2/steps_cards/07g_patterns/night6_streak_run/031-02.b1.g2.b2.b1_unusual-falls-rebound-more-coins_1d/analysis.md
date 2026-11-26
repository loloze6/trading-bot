---
line: 7.g patterns
backtest: 031-02.b1.g2.b2.b1_unusual-falls-rebound-more-coins_1d
idea tested: 031-02.b1.g2.b2.b1_unusual-falls-rebound-more-coins
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4094 USD
---
## Findings
- **F1:** The tested idea's measured effect is too small to trade. The unusual move is +0.08 % per 2-day case (t 0.42 over 1909 days, strength 0.010 of a usual 7.48 % move). That is 0.3 times the 0.22 % cost of a trade. The book's Sharpe of 0.62 is only 0.02 above holding the coins, so the book earns mostly the coins' drift.
- **F2:** Graded by the fall measured against 20-day volatility, 2-day moves are not ordered. Falls beyond 2.5 standard deviations are followed by −0.41 % excess (t −0.51, 299 cases). Falls of 1.5 to 2.5 are followed by +0.72 % (t 0.57). Falls of 0.75 to 1.5 are followed by +0.56 % (t 1.47). The slope on down days, measured against 60-day volatility, is negative: −0.048, t −1.35, on 7381 cases. This is the opposite of the tested grading.
- **F3:** Streak length shows no graded follow-on move either way. At 2 days, strength runs +0.067, +0.025, +0.098, +0.015 and −0.021 for down streaks of 5, 4, 3, 2 and 1 days. It runs −0.042, −0.007, +0.041, −0.029 and +0.108 for up streaks of 1 to 5 days. No group reaches |t| 2: the largest is 1.81 for 5-day up streaks. At 5 days the largest is −1.86, for 4-day down streaks.
- **F4:** The coin's own return over its past 10 to 40 days, measured against its volatility, has a positive slope on the next moves, but it is weak. At 10 days the t is 2.19 for the 10-day return (3249 cases, 280 days), 1.66 for the 20-day and 1.64 for the 40-day. At 2 days the 20-day return's t is 1.29, and its top quintile gives +0.63 % excess (t 2.02).
- **F5:** That momentum slope is not stable across years. For the 20-day return at a 10-day horizon, the t is −2.10 in 2022 and −1.60 in 2018, against +2.25 in 2024; the other years lie between −0.22 and 1.13. By coin, 14 of 19 slopes are positive, but only ADA reaches t 2.07.
- **F6:** Other angles show nothing beyond chance. The volatility ratio quartiles at 2 days have t from −1.41 to 1.36. Weekday excess 1-day returns have t from −1.39 to 1.73. Falls split by volatility tercile have t from −0.94 to 1.38. Rises of more than 2.5 standard deviations give +1.42 % at 2 days, but with t 1.75 on 398 cases.

## Ideas
- No ideas: I compared about 60 slices: fall size, streak length, past 10-to-40-day return, volatility level, weekday, and year and coin splits. The strongest pattern is the momentum slope in F4, which has a t of about 2 and reverses sign by year (F5). At that count of comparisons, nothing stands out from chance, so no finding is strong enough to support a new idea.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
