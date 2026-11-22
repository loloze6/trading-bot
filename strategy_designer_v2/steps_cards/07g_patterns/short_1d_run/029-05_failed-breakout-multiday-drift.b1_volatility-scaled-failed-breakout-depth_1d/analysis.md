---
line: 7.g patterns
backtest: 029-05_failed-breakout-multiday-drift.b1_volatility-scaled-failed-breakout-depth_1d
idea tested: 029-05_failed-breakout-multiday-drift.b1_volatility-scaled-failed-breakout-depth
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4196 USD
---
## Findings
- **F1:** The day after a coin's daily return falls in the lowest tenth when measured in units of its 20-day daily volatility, the coin beats its normal daily drift by +0.53 % (t 3.61, 1450 days). The effect shrinks steadily across the deciles: the second tenth gives +0.27 % (t 2.18), the middle tenths are near 0, and the seventh to ninth tenths are negative (-0.25 %, t -2.26 in the eighth).
- **F2:** The rebound after the lowest fifth of volatility-scaled days is positive for all six coins: BTC +0.18 %, ETH +0.32 %, LTC +0.32 %, XRP +0.35 %, ZEC +0.37 %, and XMR strongest at +0.85 % (t 4.06). It holds in both halves of the windows (w1–w12: +0.48 %, t 3.91; w13–w24: +0.32 %, t 2.19).
- **F3:** Over 8 days on the non-overlapping grid, the lowest fifth of volatility-scaled daily returns is followed by an excess rise of +2.92 % (t 3.25, 339 cases). The fourth fifth is followed by an excess fall of -1.80 % (t -2.79). The ordering is the same in both halves: early +4.00 % (t 3.39), late +1.96 % (t 1.47).
- **F4:** My own reconstruction of the tested situation does not reproduce the step-5 result. Read on the bar of the close back below the old 20-day high, the coin rises +2.59 % from day 2 to day 10 (t 3.08, 386 events) and +3.22 % from day 0 to day 10 (t 3.39). On the 8-day grid, failure cells show an excess rise of +4.56 % (t 2.71, 131 cases).
- **F5:** The book's short trades lose on every coin. Mean net trade results run from -0.56 % (XMR) to -3.57 % (ZEC), and only 34.9 % of 878 trades win. This fits F4 better than the confirmed excess fall of the verdict, so the two case definitions should be compared before the verdict is trusted.
- **F6:** Saturdays beat the coin's normal daily drift by +0.34 % (t 4.08, 2484 days), positive for all six coins and in both halves (t 3.60 and 2.30). This is a calendar condition with no grading, so it supports no idea here.
- **F7:** Several other angles showed nothing that stands out after this many looks, judged by the 8-day excess move by quintile:

## Ideas
- `029-05_failed-breakout-multiday-drift.b1_volatility-scaled-failed-breakout-depth.g1_volatility-scaled-down-day-rebound` (from F1, F2, F7): The further a coin's 1-day return falls below zero, measured in units of its 20-day daily volatility, the more the coin rises over the next day.
- `029-05_failed-breakout-multiday-drift.b1_volatility-scaled-failed-breakout-depth.g2_week-long-rebound-after-selloffs` (from F3, F1): The further a coin's 1-day return falls below zero, measured in units of its 20-day daily volatility, the more the coin rises over the next 8 days.
- `029-05_failed-breakout-multiday-drift.b1_volatility-scaled-failed-breakout-depth.g3_failed-breakout-rebound` (from F4, F5, F1): After a coin closes back below its old 20-day high within 3 days of closing above it, the coin rises over the next 10 days, the more so the larger that day's fall in units of the coin's 20-day daily volatility.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
