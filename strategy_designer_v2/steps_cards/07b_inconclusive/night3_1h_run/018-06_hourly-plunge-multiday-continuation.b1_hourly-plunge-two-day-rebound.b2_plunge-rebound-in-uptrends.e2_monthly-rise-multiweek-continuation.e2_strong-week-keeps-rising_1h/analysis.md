---
line: 7.b inconclusive
backtest: 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends.e2_monthly-rise-multiweek-continuation.e2_strong-week-keeps-rising_1h
idea tested: 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends.e2_monthly-rise-multiweek-continuation.e2_strong-week-keeps-rising
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3392 USD
---
## Findings
- **F1:** The tested idea's own move is zero, not a small positive one: over 168 hours the unusual move is -0.09 % per case (t -0.28, 1883 cases, strength -0.005 of a usual 12.47 % move); the total move of +0.91 % per case (4.7 times the 0.19 % cost of a trade) is entirely the coins' normal drift of +0.99 %.
- **F2:** The move does not grow with the strength of the week. By forecast band the unusual move is -0.57 % (t -1.29, n 875), +0.88 % (t 1.37, n 371), -0.33 % (t -0.52, n 427) and +0.76 % (t 0.73, n 210 at the cap). By 7-day-return quartile it is +0.68 % for the weakest weeks (mean week +2.3 %, t 1.27) and -0.24 % for the strongest (mean week +18.9 %, t -0.34). Its correlation with the 7-day return is 0.03.
- **F3:** Moving the horizon does not reveal the effect either: the unusual move is +0.09 % over 24 hours (t 0.85), +0.02 % over 72 hours (t 0.11) and +0.27 % over 336 hours (t 0.57, 1756 cases); the signal's own hour already moves +0.85 % on average.
- **F4:** The effect shows only where the close stands at its 30-day high. In the quartile of cases nearest the 30-day high the unusual move is +1.85 % per case (t 2.75, 340 cases), about 9.7 times the cost of a trade. The other quartiles give -0.24 % (t -0.30), -1.66 % (t -2.23) and -0.39 % (t -0.64). Inside that top quartile the slope on the 7-day return is flat (0.019, correlation 0.01).
- **F5:** The pooled zero is made of market years that cancel each other. It is +1.80 % in 2020 (t 2.07) and +2.01 % in 2021 (t 1.70), against -2.51 % in 2018 (t -2.07) and -2.33 % in 2022 (t -3.06). The longer trend does not separate them in the idea's favour: -1.94 % after a rising 90 days (t -2.14, n 213) against +1.02 % after a falling one (t 1.06, n 183), and +0.32 % after a rising 30 days (t 0.68) against -0.71 % after a falling one (t -1.32).
- **F6:** No coin carries the effect: per-coin means range from -0.66 % (XMR, t -1.17) and -0.52 % (ZEC) to +0.13 to +0.37 % (BTC, ETH, LTC), and no coin's |t| exceeds 1.17.

## Ideas
- `018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends.e2_monthly-rise-multiweek-continuation.e2_strong-week-keeps-rising.b1_strong-week-at-monthly-high` (from F4, F1, F2): A coin whose 7-day return is among its largest rises over the next 7 days by more than its usual 7-day drift, and the larger its 7-day return, the larger that rise, only while its close stands at the highest of its last 30 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
