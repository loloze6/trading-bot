---
line: 7.b inconclusive
backtest: 029-05_failed-breakout-multiday-drift.d1_failure-still-below-high_1d
idea tested: 029-05_failed-breakout-multiday-drift.d1_failure-still-below-high
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3173 USD
---
## Findings
- **F1:** Step 5's main measure is on the side the idea predicts but below the bar: the mean unusual 8-day move in the short direction is +0.84 % per case (t 1.44, 436 cases, strength 0.048), and my own case reading gives +1.05 % (t 1.89, 486 cases), also short of t 2.
- **F2:** The effect only appears beyond a few days and grows with time: the mean unusual short move is -0.01 % at 2 days (t -0.05, 513 cases), +0.12 % at 4 days (t 0.29, 502), +1.05 % at 8 days (t 1.89, 486) and +2.12 % at 16 days (t 2.40, 445).
- **F3:** The effect sits in coins already falling over 60 days: with a negative 60-day return, cases move +1.70 % over 8 days (t 2.61, 320 cases) and +2.80 % over 16 days (t 2.99, 311). With a positive 60-day return they move -0.21 % (t -0.21, 166) and +0.52 % (t 0.26, 134).
- **F4:** The effect is mixed across years: 2018 gives +8.28 % (t 4.33, 39 cases), 2023 +1.84 % (t 2.33, 68) and 2020 -3.03 % (t -2.57, 80); every other year has |t| below 1.2.
- **F5:** The effect is mixed across coins at 8 days: XRP +2.71 % (t 2.04, 61 cases), ZEC +3.23 % (t 1.76, 75) and BTC +1.54 % (t 1.69, 92), while LTC is -0.94 % (t -0.57, 83) and XMR -0.19 % (t -0.19, 94). Six coins leave each with under 100 cases.
- **F6:** The grading by depth holds only past the shallowest failures: the lowest depth tercile gives -0.49 % (t -0.50, 163 cases), the middle +1.96 % (t 2.24, 162) and the deepest +1.68 % (t 1.66, 161). The slope of the move on |forecast| is +0.0027 (t 1.69, 486 cases).
- **F7:** The market's own rise cancels the effect on the book: the coins' normal drift is -1.05 % per case in the short direction. That leaves a total move of -0.21 %, against a 0.19 % cost per trade. The total short move is about zero at every horizon (8 days: -0.004 %, t -0.01), and the book's Sharpe is -0.14.

## Ideas
- `029-05_failed-breakout-multiday-drift.d1_failure-still-below-high.b1_failed-breakout-more-coins` (from F1, F5): After a close back below the old 20-day high within 3 days of a breakout above it, the coin's decline continues across the following 8 days only while its close 2 days after the failure is still below that old high. The further that day-2 close sits below the old high, the larger the fall from day 2 to day 10.
- `029-05_failed-breakout-multiday-drift.d1_failure-still-below-high.b2_failed-breakout-in-downtrends` (from F2, F3, F6, F7): After a close back below the old 20-day high within 3 days of a breakout above it, the coin's decline continues while its close 2 days after the failure is still below that old high, only while the coin's 60-day return is negative. The further that day-2 close sits below the old high, the larger the fall over the next 16 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
