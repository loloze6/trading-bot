---
line: 7.g patterns
backtest: 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends_1h
idea tested: 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.3799 USD
---
## Findings
- **F1:** When a coin's 24-hour return is up by at least 1 times its 30-day mean absolute 24-hour return while its 30-day return is negative, the next 24 hours fall short of the coin's drift by 60.85 bps (t -4.19, 974 non-overlapping cases); the shortfall grows with the rise: -45 bps (t -2.64) for 1 to 2 times, -84 bps (t -2.66) for 2 to 3 times, -117 bps (t -2.20) beyond 3 times. Over all positive 24-hour returns in a falling month, Spearman rho is -0.069 (p 0.0002, n 2912). Per coin the mean is negative in 6 of 6 (t -0.77 to -2.93), and it is negative in 6 of 8 years. The move is about 3.2 times the 19 bps cost of a round trip.
- **F2:** The same rise in a rising month shows nothing over 24 hours: -10, +11 and +2 bps for 1 to 2, 2 to 3 and above 3 times (t within ±0.7; Spearman rho -0.032, p 0.051). The fade belongs to falling months only.
- **F3:** A 24-hour fall of at least 3 times the 30-day mean absolute 24-hour return is followed by a rebound over the next 24 hours, in a rising month and in a falling one: +254 bps (t 5.22, n 86) when the 30-day return is positive, +162 bps (t 2.89, n 211) when it is negative. By depth of fall, the 24-hour rebound is +197 bps (t 4.20, n 192) for 3 to 4 times and +172 bps (t 2.07, n 105) beyond 4 times, against +15 bps (t 0.59) for 2 to 3 times. Over all negative 24-hour returns, the deeper the fall the larger the next 24 hours (Spearman rho 0.094, p 6e-14, n 6327).
- **F4:** The plunge rebound peaks over 1 to 2 days and is gone at 4 days in falling months. For falls of 3 to 4 times, the move above drift is +39 bps over 6 hours (t 2.63), +70 bps over 12 hours (t 2.42), +197 bps over 24 hours (t 4.20) and +306 bps over 48 hours (t 3.25, n 102). Over 96 hours, a fall beyond 3 times in a falling month is followed by -101 bps (t -0.53, n 61). The tested idea's 4-day horizon and its rising-month condition therefore hold only part of the effect.
- **F5:** The 24-hour rebound after falls of at least 2.5 times is positive on every coin (+64 to +302 bps; t above 2 on XMR, XRP and ZEC). It is uneven by year: +240 to +346 bps in 2018, 2020, 2021 and 2025 (t 2.19 to 3.47), but +3 to +10 bps in 2022 to 2024 (t at most 0.10).
- **F6:** Within the book, the trades in the top quartile of entry forecast earn 13.1 % net on average, against 1.9 to 4.5 % for the other three quartiles (about 622 trades each, held 316 to 410 hours). The forecast is clipped at 20 from the second quartile up, which is why the plan's median split of the forecast could not separate the cases.
- **F7:** Patterns that do not stand out from chance, given how many angles were read:

## Ideas
- `018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends.g1_downtrend-rally-fades-next-day` (from F1, F2): When a coin's 24-hour return, read at an hourly close, rises by a large multiple of its 30-day average absolute daily return while its 30-day return is negative, its price falls over the next 24 hours below the coin's usual 24-hour drift, and the larger that multiple, the larger the fall.
- `018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends.g2_plunge-rebound-over-two-days` (from F3, F4, F5): When a coin's 24-hour return, read at an hourly close, falls by a large multiple of its 30-day average absolute daily return, its price rises over the next 2 days above the coin's usual 2-day drift, and the deeper that fall in units of the usual daily move, the larger the rebound.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
