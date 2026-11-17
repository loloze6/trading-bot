---
line: 7.g patterns
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week_1d
idea tested: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.5536 USD
---
## Findings
- **F1:** Closeness to the 20-day closing high predicts the next 7 days better than closeness to the 52-week high, and it works best with heavy volume. On 1,958 non-overlapping 7-day grid cases, the combined rank of 20-day-high closeness and the day's volume (over its 30-day mean) gives a slope t of 3.95 on the 7-day return minus the coin's mean. Taken alone, 20-day-high closeness has t 3.49; in a multivariate fit with 52-week closeness it keeps t 2.31 while 52-week closeness turns negative (t -2.24, n 558).
- **F2:** Volume grades the gain near the 20-day high. In the top fifth of 20-day-high closeness, the 7-day excess return rises with volume: 0.0033 (n 131), then 0.0159 (n 130), then 0.0318 (n 131). In the joint table, top closeness with top-tercile volume gives +0.0369 (n 201), against -0.0162 for top closeness with bottom-tercile volume (n 78).
- **F3:** The 20-day-high-plus-volume slope is positive in 6 of 8 years, with t above 2 in 2020 (2.32), 2024 (3.02) and 2025 (2.12). It is negative in 2018 (-0.85) and 2023 (-0.58), so it is not steady every year.
- **F4:** While the 30-day return is negative (the strategy flat), a close nearer the 52-week high is followed by a lower 7-day return: rank slope t -3.74 on 258 cases. In the trending state the same slope is only -0.37 (n 300).
- **F5:** A large one-day move scaled by the coin's 30-day volatility is followed by gains only in the trending state. The top quintile of this move has a 7-day excess return of +0.0176 (t 2.21, n 392). The rank slope is t 2.68 when the 30-day return is positive (n 1,013) and t 0.44 otherwise (n 945).
- **F6:** Saturdays carry an outsized share of the coins' daily gains. The mean coin return on Saturday is 0.00469 against 0.00065 on other days, using the cross-coin daily mean (Welch t 2.36, n 414 Saturdays). Saturday is higher in 7 of 8 years and in all 6 coins, and the book earns 0.00098 on Saturdays against 0.00026 on other days (t 2.44). Because this weekday pattern cannot be graded, it stays a finding only.
- **F7:** The book's whole gain comes from the trending state: the summed bar gains are 7.25 there against -0.005 in the flat state. Within the trending state, the 30-day return adds little to the 7-day forecast (rank t 0.72), while the 7-day return carries it (t 3.18).

## Ideas
- `013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g1_short-high-break-on-volume` (from F1, F2, F3): The closer a coin's daily close sits to its highest close of the past 20 days, and the heavier that day's volume against its 30-day average, the higher the coin's return over the next 7 days.
- `013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g2_falling-month-high-fades` (from F4): While a coin's 30-day return is negative, the closer its daily close sits to its highest close of the past 52 weeks, the lower its return over the next 7 days.
- `013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g3_strong-day-follow-through-in-uptrends` (from F5, F7): While a coin's 30-day return is positive, the larger its latest one-day return relative to its 30-day daily volatility, the higher its return over the next 7 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
