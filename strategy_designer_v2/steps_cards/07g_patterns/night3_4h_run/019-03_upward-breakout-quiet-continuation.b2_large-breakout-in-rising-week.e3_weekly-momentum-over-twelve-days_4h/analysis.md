---
line: 7.g patterns
backtest: 019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.e3_weekly-momentum-over-twelve-days_4h
idea tested: 019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.e3_weekly-momentum-over-twelve-days
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4299 USD
---
## Findings
- **F1:** How fast volatility is rising predicts the next twelve days better than the tested forecast does. On the non-overlapping 72-bar grid (1,116 cases), the coin's 12-day return minus its drift grows with the ratio of its 20-bar to its 120-bar 4h volatility, pooled slope +0.070 per unit of ratio (t 4.47). Added next to the forecast in one regression it keeps its weight (t 4.72), and the forecast keeps its own (t 3.70). From the lowest to the highest quintile of the ratio, the drift-adjusted 12-day return goes from -2.57 % (t -2.38) to +4.74 % (t 2.97), against a 0.19 % round trip.
- **F2:** The rising-volatility effect does not depend on the direction of the last week, though it is uneven across years. In the highest ratio quintile both sides end higher: after a 7-day fall +3.76 % (t 2.81, 124 cases), after a 7-day rise +5.95 % (t 1.87, 99). In the lowest quintile both end lower: -3.12 % (t -2.26) and -2.03 % (t -1.22). The slope is positive on 5 of 6 coins (t 1.7 to 2.7; XMR t 0.20) and in 6 of 8 years (t 4.09 in 2024 and 3.28 in 2025, but -1.78 in 2023).
- **F3:** The tested momentum carries on after a wide past week, not a narrow one, the reverse of the brief's mechanism. Split by the range of the week before the 7-day move, the slope of the 12-day drift-adjusted return on the 7-day scaled return has t -0.65 in the narrowest tercile, 2.10 in the middle and 5.07 in the widest (276 cases each).
- **F4:** Narrow ranges are not followed by larger moves. The mean absolute 12-day move is 13.2 % after the narrowest current-week range quintile and 13.8 % after the widest. By the previous week's range tercile it is 12.3 %, 12.4 % and 11.7 %.
- **F5:** Only the largest forecasts carry the tested idea's capture. In the top quartile of the forecast's size the signed 12-day drift-adjusted return is +3.49 % (t 3.32, 279 cases); the lower three quartiles give -0.77 %, +0.52 % and +1.23 % (all |t| < 1.2). Both extreme forecast quintiles capture: shorts +3.05 % (t 3.65), longs +3.11 % (t 2.47).
- **F6:** Coins rise on Fridays and Saturdays (UTC). Mean daily return is +0.33 % on Friday (t 3.51, 2,479 coin-days) and +0.45 % on Saturday (t 5.53, 2,484), against -0.18 % to +0.28 % on the other days. The Friday-Saturday mean is positive on all 6 coins (t 1.87 to 3.76) and in 7 of 8 years (2022: -0.20 %, t -1.24). This is a calendar condition with no grade, and I looked at many angles, so I propose no idea from it.
- **F7:** The book trails holding the coin. Its mean daily return is below holding's on 5 of 6 coins (XMR -0.008 % vs +0.107 %, ZEC -0.031 % vs +0.155 %, BTC 0.049 % vs 0.118 %); only ETH beats it (0.152 % vs 0.137 %). This fits a signed book that is short for much of a rising period, while the idea's capture sits only in its largest forecasts (F5).

## Ideas
- `019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.e3_weekly-momentum-over-twelve-days.g1_rising-volatility-precedes-rises` (from F1, F2, F4): The more a coin's 4h volatility over the last three days exceeds its 4h volatility over the last twenty days, the more the coin rises over the next twelve days, whichever way its last week moved.
- `019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.e3_weekly-momentum-over-twelve-days.g2_momentum-after-wide-weeks` (from F3, F4, F5): The wider a coin's high-low range over the 7 days before its latest 7 days, relative to its usual range, the more strongly its 7-day volatility-scaled return continues in the same direction over the next twelve days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
