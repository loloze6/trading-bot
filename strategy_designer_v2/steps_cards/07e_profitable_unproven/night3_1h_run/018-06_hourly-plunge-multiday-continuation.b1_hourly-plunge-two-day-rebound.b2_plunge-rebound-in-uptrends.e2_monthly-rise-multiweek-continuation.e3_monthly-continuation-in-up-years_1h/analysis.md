---
line: 7.e profitable but not proven
backtest: 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends.e2_monthly-rise-multiweek-continuation.e3_monthly-continuation-in-up-years_1h
idea tested: 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends.e2_monthly-rise-multiweek-continuation.e3_monthly-continuation-in-up-years
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 0
cost: 0.3117 USD
---
## Findings
- **F1:** Half of the book's mean daily gain is the market's own rise. The book earns 0.0830 % a day; 0.0412 % of it is the position held times the coin's mean daily return, and 0.0418 % is timing. Holding the coins earns 0.0984 % a day at a Sharpe of 0.57, against the book's 1.17.
- **F2:** The timing comes from being out of the market in falling periods, not from catching rises.
- **F3:** The regime's share of time follows the window's outcome closely. Active share and the window's own return have a correlation of 0.61 over 141 coin-windows. By quartile of active share (4 %, 26 %, 59 %, 87 %), holding returns -21 %, +5 %, +42 % and +94 %, and the book -2 %, +5 %, +20 % and +53 %.
- **F4:** The year condition's forecast of the coming weeks is weak, so how much of F3 a trader could act on is unproven.
- **F5:** The 30-day return adds nothing to the 7-day move on its own.
- **F6:** The one sign of a 7-day effect beyond the year condition is a faded rebound in falling years. In a down year, a positive 30-day return is followed by a 7-day move 0.91 % below the coin's drift (t -1.80, 862 cases). In an up year it is followed by a move 0.62 % above it (t 1.18, 1038 cases).
- **F7:** The book's gain rests on a few long trades.

## Ideas
- `018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends.e2_monthly-rise-multiweek-continuation.e3_monthly-continuation-in-up-years.e1_one-year-trend-sets-the-month` (from F2, F3, F4): A coin's own 1-year return predicts its move over the next 30 days: the higher its 1-year return, the more it rises over the next 30 days beyond its usual 30-day drift.
- `018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends.e2_monthly-rise-multiweek-continuation.e3_monthly-continuation-in-up-years.e2_rebounds-fade-in-falling-years` (from F6, F5): In a year when a coin's own 1-year return is negative, a coin whose 30-day return is positive falls over the next 7 days below its usual 7-day drift, more as its 30-day rise is larger.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
