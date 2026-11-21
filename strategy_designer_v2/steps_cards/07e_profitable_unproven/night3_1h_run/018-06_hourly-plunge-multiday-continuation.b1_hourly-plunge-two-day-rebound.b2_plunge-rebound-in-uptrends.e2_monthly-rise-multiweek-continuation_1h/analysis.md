---
line: 7.e profitable but not proven
backtest: 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends.e2_monthly-rise-multiweek-continuation_1h
idea tested: 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends.e2_monthly-rise-multiweek-continuation
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.4063 USD
---
## Findings
- **F1:** The book's mean daily gain of 0.129 % splits into 0.075 % (58 %) from the market's own rise, with an average position of 0.52 of the book, and 0.054 % from timing, and the timing is not significant (t 1.33 over about 2,900 book-days).
- **F2:** The book beats holding mainly by being smaller or out in falling periods: in 2018 it lost 0.19 % a day against holding's 0.35 %, and in 2022 0.05 % against 0.19 %. In strong rising windows it trails holding (w11: 0.59 % against 1.26 % a day; w16: 0.27 % against 0.45 %).
- **F3:** The gain comes from a few long trades. The top 5 % of the 2,853 trades carry 35,483 of the 48,470 summed net percent (73 %), and trades held 30 to 90 days carry 33,346. Trades held under 7 days lose: 111 trades under 1 day average -1.10 %, and 160 trades of 1 to 7 days average -0.54 %.
- **F4:** The plan measured the idea at 2 weeks, where its forecast-weighted excess return has t 1.77 (568 cells), and the effect is clearer at shorter horizons:
- **F5:** Inside the positive side the forecast is barely graded: 502 of the 568 two-week cells sit at forecasts above 2.5. Ranked by the 30-day return itself, the 7-day excess is not monotone across quintiles:
- **F6:** A coin's 7-day return ranks the next move about as well as its 30-day return. The top 7-day-return quintile is followed by a 3-day excess of +0.66 % (strength 0.072) and a 7-day excess of +0.96 % (strength 0.058). The middle quintiles are negative at both horizons (-0.42 % to -1.00 % over 7 days).
- **F7:** The effect depends on the year and the coin:

## Ideas
- `018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends.e2_monthly-rise-multiweek-continuation.e1_monthly-rise-weekly-continuation` (from F4, F5, F3): A coin whose 30-day return is positive rises over the next 7 days by more than its usual 7-day drift, and the larger its 30-day return, the larger that rise.
- `018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends.e2_monthly-rise-multiweek-continuation.e2_strong-week-keeps-rising` (from F6, F4): A coin whose 7-day return is among its largest rises over the next 7 days by more than its usual 7-day drift, and the larger its 7-day return, the larger that rise.
- `018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends.e2_monthly-rise-multiweek-continuation.e3_monthly-continuation-in-up-years` (from F7, F2, F4): In a year when a coin's own 1-year return is positive, a coin whose 30-day return is positive rises over the next 7 days by more than its usual 7-day drift, more as its 30-day return is larger.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
