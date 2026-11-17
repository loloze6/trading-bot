---
line: 7.b inconclusive
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g2_falling-month-high-fades_1d
idea tested: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g2_falling-month-high-fades
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.2919 USD
---
## Findings
- **F1:** The tested forecast is the distance below the 52-week high standardised over its own past year, not the distance itself, and on the 1177 falling-month 7-day cases it correlates only -0.42 with the raw percent distance, so the test graded the cases differently from the idea's "how close to the high".
- **F2:** Graded by the raw percent distance below the 52-week high, the 7-day excess return falls as the close nears the high (pooled slope -0.000229 per point, t -1.43, n 1177), and the nearest third earned -0.0113 against -0.0011 for the farthest third, a difference of -0.0102.
- **F3:** The raw-distance slope is negative in all 8 years (2018 to 2025) and reaches t -3.04 in 2019, -2.26 in 2022 and -2.07 in 2025, with n between 109 and 197 per year; it is also negative in 5 of the 6 coins, the strongest being XRP at t -1.76 (n 199). The effect is consistent in direction but small next to its noise.
- **F4:** On the plan's own forecast the slope is on the predicted side but far from the bar at every horizon (t 1.05 at 3 days with n 2766, 0.42 at 7 days with n 1177, 0.01 at 14 days, -0.08 at 30 days), and its quintiles are not ordered (excess -0.0101, +0.0013, -0.0144, -0.0110, -0.0011 from smallest to largest forecast).
- **F5:** The falling month itself drags all active cases (mean 7-day excess -0.0071, t -1.96, n 1177), and the 7-day excess has a standard deviation of 0.10 to 0.15 per third, so a gap of about 0.01 between thirds is buried in the coins' own moves. The supporting check still passed (nearest minus farthest third -0.0081).

## Ideas
- `013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g2_falling-month-high-fades.b1_falling-month-high-fades-wider` (from F2, F3, F4, F5): While a coin's 30-day return is negative, the closer its daily close sits to its highest close of the past 52 weeks, the lower its return over the next 7 days.
- `013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g2_falling-month-high-fades.b2_raw-distance-high-fades` (from F1, F2, F3): While a coin's 30-day return is negative, the smaller the percent by which its daily close sits below its highest close of the past 52 weeks, the lower its return over the next 7 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
