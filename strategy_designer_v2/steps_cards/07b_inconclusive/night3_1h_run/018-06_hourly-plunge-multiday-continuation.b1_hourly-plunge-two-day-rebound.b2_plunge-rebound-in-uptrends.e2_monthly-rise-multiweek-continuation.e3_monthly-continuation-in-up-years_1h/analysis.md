---
line: 7.b inconclusive
backtest: 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends.e2_monthly-rise-multiweek-continuation.e3_monthly-continuation-in-up-years_1h
idea tested: 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends.e2_monthly-rise-multiweek-continuation.e3_monthly-continuation-in-up-years
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 1
cost: 0.1978 USD
---
## Findings
- **F1:** The result is on the side the idea predicts but too varied for 750 cases to show it: the 7-day unusual move is +0.73 % (t 1.27; size +0.88 %, strength 0.062, total move 9.9 times the 0.19 % cost of a trade), while by year it ranges from −4.96 % in 2018 (t −2.55, 65 cases), −4.74 % in 2019 and −4.11 % in 2022, to +2.11 % in 2020, +3.06 % in 2021 (t 2.04) and +0.82 % to +1.41 % in 2024 and 2025.
- **F2:** The grading is clear and monotonic, so the weak mean comes from the weakest cases diluting the strong ones: by quarter of the forecast the 7-day unusual move is −1.79 % (t −1.82, forecast near 2.8), +0.29 %, +1.86 % (t 1.85) and +2.58 % (t 1.81, forecast near 19.5); the upper half beats the lower by +2.97 %.
- **F3:** The effect splits by coin: positive on BTC (+0.94 %, t 1.24), ETH (+1.06 %), XRP (+1.65 %) and ZEC (+2.68 %), negative on LTC (−0.84 %) and XMR (−0.59 %), each over only 99 to 163 cases.
- **F4:** The plan's 7-day horizon sits where the effect is already fading. Over 1 day its strength is 0.026 (t 1.72, 5,343 cases), over 3 days 0.054 (t 1.95, 1,770), over 7 days 0.050 (t 1.27). Over 14 days it falls to 0.016 (t 0.55), and over 30 days it is −0.038.
- **F5:** The month's sign does carry information inside up years: on bars with a positive 1-year return but no positive 30-day rise, the move is negative at every horizon (−0.78 % over 7 days, t −1.57; −0.43 % over 3 days, t −1.97). Outside up years it is about zero (−0.08 % over 7 days, t −0.21).

## Ideas
- `018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends.e2_monthly-rise-multiweek-continuation.e3_monthly-continuation-in-up-years.b1_monthly-continuation-more-coins` (from F1, F2, F3): In a year when a coin's own 1-year return is positive, a coin whose 30-day return is positive rises over the next 7 days by more than its usual 7-day drift, more as its 30-day return is larger.
- `018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends.e2_monthly-rise-multiweek-continuation.e3_monthly-continuation-in-up-years.b2_monthly-rise-three-day-continuation` (from F4, F5, F2): In a year when a coin's own 1-year return is positive, a coin whose 30-day return is positive rises over the next 3 days by more than its usual 3-day drift, more as its 30-day return is larger.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
