---
line: 7.g patterns
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.b1_nearness-to-high-more-coins_1h
idea tested: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.b1_nearness-to-high-more-coins
step 5: confirmed
step 6: profitable enough
mode: one call
explorations: 3
cost: 0.6659 USD
---
## Findings
- **F1:** Each coin rises in the two hours from 21:00 to 23:00 UTC: the mean 2-hour return is 0.000991 (t = 10.75, n = 24274 non-overlapping days). The hourly log returns are 0.000416 (t = 7.03) at 21:00 and 0.000492 (t = 8.72) at 22:00, the two highest t values of the 24 hours. The pattern holds in all 19 coins (excess over the other hours from 0.000067 in TRX to 0.001429 in ONDO) and in 7 of 8 years, 2022 being the one negative year (-0.000383).
- **F2:** The evening rise grows with the coin's 7-day hourly volatility, rising steadily across volatility quintiles from 0.000344 (t = 3.14) in the calmest to 0.002604 (t = 8.37) in the most volatile, n = 4855 each. It is the same while the 30-day return is positive (0.000982) or not (0.001001).
- **F3:** While the 30-day return is negative, the coin's 168-bar forward return is below its own average. The regression constant is -0.0120 (t = -3.98, n ≈ 1590), 16 of 19 coins are negative, and 7 of 8 years are negative. Inside that state, a higher 7-day return predicts a lower next 7 days (slope -0.0070 per standard deviation, t = -2.24). The deepest 30-day falls are the exception (+0.0135, t = 1.75).
- **F4:** While the 30-day return is positive, a higher 1-day return predicts a higher 168-bar excess return. The top 1-day-return quintile earns +0.0321 (t = 3.14, n = 320) against +0.0016 in the bottom quintile. In a joint regression with volume ratio and distance from the high, the slope is +0.0095 per standard deviation (t = 2.38, n = 1598).
- **F5:** The book's forecast is graded at the top but not at the bottom. The highest forecast quintile earns +0.0303 (t = 3.76) in 168-bar excess return, while the lowest positive quintile earns -0.0115 (t = -1.71). Grid bars with the book flat earn -0.0065 against +0.0069 with a forecast above zero.

## Ideas
- `013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.b1_nearness-to-high-more-coins.g1_late-evening-utc-rise` (from F1, F2): Each coin rises over the two hours from 21:00 to 23:00 UTC, and the rise is larger the higher the coin's hourly volatility over the past 7 days.
- `013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.b1_nearness-to-high-more-coins.g2_daily-strength-in-rising-months` (from F4, F5): While a coin's 30-day return is positive, the larger its 1-day return, the higher its return over the next 7 days.
- `013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.b1_nearness-to-high-more-coins.g3_bounces-fade-in-falling-months` (from F3): While a coin's 30-day return is negative, its return over the next 7 days is below its usual 7-day return, and more so the higher its 7-day return.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
