---
line: 7.g patterns
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g1_two-week-momentum-continuation.g1_momentum-continuation-in-uptrends_1d
idea tested: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g1_two-week-momentum-continuation.g1_momentum-continuation-in-uptrends
step 5: confirmed
step 6: profitable enough
mode: one call
explorations: 3
cost: 0.5196 USD
---
## Findings
- **F1:** The tested slope holds wherever the 7-day grid starts: in the trending regime the t of the 14-day return, controlled for the 1-day return, stays positive at all seven grid offsets (2.75, 2.07, 3.37, 3.58, 3.06, 4.61, 2.01; about 1,000 to 1,085 cases each), and the demeaned 7-day return rises across the trending 14-day-return quintiles from -0.0223 (t -2.60) to +0.0222 (t 1.68), 217 cases each.
- **F2:** Outside the trend the same signal does nothing: in the non-trending regime the 14-day return's correlation with the demeaned 7-day return is 0.030 (p 0.33, n 1,070), against 0.102 (p 0.0008, n 1,085) in the trending regime.
- **F3:** The 1-day return looked like a second trend-regime predictor but is not robust: its t beyond the 14-day return is 2.45 on the base grid and turns to -4.22 and -4.30 at grid offsets 1 and 5, so it depends on which weekday the grid falls on.
- **F4:** The non-trending regime's negative link to the 60-day return (t -2.76, 566 cases) also depends on the grid: it is between -0.21 and -1.94 at the other six offsets, and +0.30 at one of them.
- **F5:** Saturday is the strongest day for the coins: the mean daily coin return is 0.00454 (t 3.04 on 414 days, one value per day), the demeaned Saturday return is positive in all six coins (0.0004 to 0.0051) and in 6 of 8 years, and the book's Saturday mean return is 0.00224 against 0.00003 to 0.0013 on the other days. Saturday is a condition with no grade, though, and one of seven weekdays searched.
- **F6:** The book's edge is spread across coins: its mean daily return is above zero in 5 of 6 coins (0.00042 to 0.00139), with LTC the exception (-0.00007), and it loses less than holding the coins in the down years 2018 (-0.00035 against -0.00347) and 2022 (-0.00047 against -0.00180).

## Ideas
- `013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g1_two-week-momentum-continuation.g1_momentum-continuation-in-uptrends.g1_uptrend-momentum-on-4h-bars` (from F1, F2, F6): Among coins whose 60-day return is positive, the larger a coin's 14-day rise, the higher its return over the next 7 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
