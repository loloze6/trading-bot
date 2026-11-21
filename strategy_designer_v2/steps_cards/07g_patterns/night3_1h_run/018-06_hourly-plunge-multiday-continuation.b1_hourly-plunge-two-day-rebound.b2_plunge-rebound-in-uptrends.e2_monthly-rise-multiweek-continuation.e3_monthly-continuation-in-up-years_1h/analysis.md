---
line: 7.g patterns
backtest: 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends.e2_monthly-rise-multiweek-continuation.e3_monthly-continuation-in-up-years_1h
idea tested: 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends.e2_monthly-rise-multiweek-continuation.e3_monthly-continuation-in-up-years
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.3814 USD
---
## Findings
- **F1:** While a coin's 1-year return is positive, nearness to its 30-day high is followed by a larger 7-day rise than the 30-day return is. On the non-overlapping 168-hour grid, the quintile closest to the high has an unusual 7-day move of +3.27 % (t 3.44, 297 cases), the nearest decile +4.14 % (t 2.35, 97 cases). The top 30-day-return quintile, the tested idea's situation, has only +1.73 % (t 1.65, 242 cases).
- **F2:** Nearness adds to the 30-day rise rather than repeating it. Among up-year cases in the top tercile of 30-day return, those in the two quintiles nearest the 30-day high move +2.39 % (t 2.16, 223 cases), against +0.99 % (t 0.61, 94 cases) for the rest of that tercile.
- **F3:** The nearness effect is uneven and not smooth.
- **F4:** A sharp up hour (more than 3 times the past week's hourly volatility) is not followed by an unusual 7-day rise, and a larger jump does not raise it. Across 1262 cases, the up-year cases show +0.60 % (t 1.12, 722) and the z quartiles range from +0.08 % to +1.22 %, none with t above 1.41. This is against the brief's claim that the hour the move happens starts a multi-day continuation.
- **F5:** Hour-of-day returns are strongly uneven, but far below a round trip. The hours starting 21:00 and 22:00 UTC average +5.5 bps (t 6.88) and +4.5 bps (t 5.99), the hour starting 14:00 averages -3.3 bps (t -3.53), and Saturday's hours average +2.0 bps (t 5.51). This matches F2 of the earlier runs: real but too small to pay.
- **F6:** On days in position the book earns less than the coins it holds. It averages +0.168 % a day against the coins' +0.236 % over 8732 days, while out-of-position days see the coins move only +0.015 % (8291 days). The book's gain comes from being out in weak periods, not from catching more of the rise.

## Ideas
- `018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends.e2_monthly-rise-multiweek-continuation.e3_monthly-continuation-in-up-years.g1_near-monthly-high-in-up-years` (from F1, F2, F3): In a year when a coin's own 1-year return is positive, the closer its close is to its highest close of the past 30 days, the more it rises over the next 7 days above its usual 7-day drift.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
