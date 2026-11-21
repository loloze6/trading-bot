---
line: 7.d not profitable
backtest: 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends.e2_monthly-rise-multiweek-continuation.e2_strong-week-keeps-rising_1h
idea tested: 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends.e2_monthly-rise-multiweek-continuation.e2_strong-week-keeps-rising
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3650 USD
---
## Findings
- **F1:** The book fails on its falls: its deepest fall across the chained windows reaches 45 % to 52 % (w3 −45 %, w14 −52 %, w15 −49 %), and every coin on its own falls 63 % to 88 % (ZEC −88 %, LTC −76 %). Against a yearly return in the tens of percent, that gives a Calmar of 0.47.
- **F2:** The worst book days are days the coins crash while the book is fully long: the 15 worst book days lose 8.7 % to 15.7 % while the coins lose 7.7 % to 38.7 %. The book has no state in which it steps aside before a shared fall.
- **F3:** The book's gain lives where the coin's 30-day return is not negative. Long hours with a positive 30-day return earned 18.00 of the summed hourly gain over 236,105 hours (mean 0.000076 per hour). Long hours with a negative 30-day return earned 0.28 over 120,998 hours (0.000002 per hour), though they held a mean allocation of 0.67. So a third of the exposure carries risk and almost no return.
- **F4:** On non-overlapping 168-hour cells with a long forecast (950 cells), the unusual 7-day move depends on the 30-day return:
- **F5:** Nearness to the 30-day high grades the move. Cells within 2.2 % of the 30-day high have an unusual move of +2.79 % (t 2.33, 171 cases). Cells 14 % or more below it have −0.78 % (t −0.85). Between them, the move rises steadily: +0.27 %, then +1.12 %.
- **F6:** The idea is real only in its strong part, but the pooled measure drowns it.
- **F7:** A gross simulation that keeps only the long hours with a positive 30-day return cuts the deepest fall on 5 of 6 coins:
- **F8:** Among active cells, a week whose volatility is high against its 30-day volatility is followed by a larger unusual move: +3.11 % (t 2.42, 171 cases) in the top quarter of the 7-day to 30-day volatility ratio (1.12 to 1.94). The other quarters range from −0.62 % to +0.65 %.

## Ideas
- `018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends.e2_monthly-rise-multiweek-continuation.e2_strong-week-keeps-rising.d1_strong-week-in-rising-month` (from F1, F2, F3, F4, F6, F7): A coin whose 7-day return is among its largest rises over the next 7 days by more than its usual 7-day drift, and the larger its 7-day return, the larger that rise, only while its 30-day return is positive.
- `018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends.e2_monthly-rise-multiweek-continuation.e2_strong-week-keeps-rising.d2_strong-week-near-monthly-high` (from F1, F2, F5, F6): A coin whose 7-day return is among its largest rises over the next 7 days by more than its usual 7-day drift, and the larger its 7-day return and the closer its close to its 30-day high, the larger that rise.
- `018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends.e2_monthly-rise-multiweek-continuation.e2_strong-week-keeps-rising.d3_breakout-week-on-expanding-volatility` (from F6, F8): A coin whose 7-day volatility is large against its 30-day volatility while its 7-day return is among its largest rises over the next 7 days by more than its usual 7-day drift, and the larger that volatility ratio, the larger the rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
