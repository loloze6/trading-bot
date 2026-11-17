---
line: 7.d not profitable
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week_1d
idea tested: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3337 USD
---
## Findings
- **F1:** The book earns a mean daily return of 0.000366 while the coins themselves average 0.001315, because the book is barely exposed: its mean position is 0.072, it is flat on 46% of bars and short on 21%, and long bars carry 99.8% of its gain (coin next-bar return 0.00295 when long, against 0.00053 when short and 0.00052 when flat).
- **F2:** In the trending regime the gain sits almost entirely in the top forecast fifth (next-bar coin return 0.0056, gain 0.0035 per bar, mean position 0.60), while the bottom fifth holds a mean short of -0.25 as the coin still rises 0.0007 per bar and earns only 0.0001, and the middle fifths earn between -0.00003 and 0.0006.
- **F3:** On the non-overlapping 7-day grid in the trending regime (888 cases), the coin's 7-day return predicts its excess 7-day return with t 4.09 and the 30-day return with t 2.10, but closeness to the 52-week high gives only t 0.59, and its fifths do not rank the gain (excess 0.0064, -0.0175, 0.0355, 0.0163, 0.0095 from farthest to nearest).
- **F4:** Among trending bars with a forecast above 6, the calmest third of realised volatility (0.47) sees a next-bar coin return of 0.0070, against 0.0035 and 0.0032 in the middle (0.73) and most volatile (1.19) thirds, so the signal's move is about twice as large where volatility is low.
- **F5:** Outside the trending regime the book holds almost nothing (mean position about -0.002), yet on its 7-day grid (790 cases) a lower closeness to the high predicts a higher excess 7-day return (slope -0.0105 per standard deviation, t -2.51), and so does a lower 30-day return (t -2.05).
- **F6:** Fees do not explain the shortfall: they cost 0.000063 per bar against a gross gain of 0.000428 per bar.

## Ideas
- `013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.d1_near-high-gain-in-calm-trends` (from F1, F2, F4): The closer a coin's daily close sits to its highest close of the past 52 weeks, the higher its return over the next 7 days, only while its 30-day return is positive; inside that state, the higher the 30-day return and the higher its 7-day return, the larger the gain, and the gain is larger still the lower the coin's daily-return volatility over the past 60 days.
- `013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.d2_weekly-momentum-in-rising-months` (from F2, F3): While a coin's 30-day return is positive, the higher its 7-day return, the higher its return over the next 7 days.
- `013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.d3_deep-drawdown-rebound-in-downtrends` (from F1, F5): While a coin's 30-day return is negative, the farther its daily close sits below its highest close of the past 52 weeks, the higher its return over the next 7 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
