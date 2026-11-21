---
line: 7.g patterns
backtest: 017-04_postsettle-decline-after-downtrend.c1_post-settlement-decline-four-hours_1h
idea tested: 017-04_postsettle-decline-after-downtrend.c1_post-settlement-decline-four-hours
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3657 USD
---
## Findings
- **F1:** Coins bounce after their largest 24-hour falls. On a non-overlapping 24-bar grid, the bottom decile of past 24h return was followed by a mean 24h return of +1.07% (t 6.44, n 1723), against roughly -0.2% to +0.24% for the other deciles. Among all 24h falls, the forward 24h return falls with the past return: slope -0.223 per unit of past return, se 0.016, p<0.001, so the steeper the fall, the larger the rebound.
- **F2:** The rebound after the two lowest deciles of 24h return holds in every coin and every year. By coin it ran from +0.37% (BTC, t 2.05) to +0.79% (ZEC, t 2.63). By year it was positive in all of 2018 to 2025, from +0.22% (2022, t 0.88) to +0.95% (2021, t 3.05). Spearman rho between past and next 24h return is negative in all six coins, from -0.050 to -0.114, p ≤ 0.009.
- **F3:** Bars starting at 20:00 and 21:00 UTC carry the strongest positive hourly drift of the day. The mean next-bar return was +0.055% (t 6.75) and +0.044% (t 5.66), with n ≈ 17,400 each. The 2-hour return from the 20:00 start is positive in all six coins, +0.084% to +0.108%, t 3.1 to 4.7. It is positive in 7 of 8 years, the exception being 2022 at -0.043%, t -1.43.
- **F4:** The 20:00–22:00 UTC rise grows with the coin's 24-hour volatility. By volatility tercile it was +0.034% (t 3.15), +0.065% (t 4.34) and +0.192% (t 7.28), each with n ≈ 5,750.
- **F5:** Inside the bottom 72h-return quintile, the 4 hours after the 00:00 close fall by -0.124% (t -2.83, n 3359), which is part of what the tested idea captures. The 4 hours after the 12:00 close in the same downtrends rise by +0.227% (t 4.20, n 3399), and those after the 20:00 close rise by +0.10% (t 2.10).
- **F6:** The book, all short trades held about 238 minutes, lost money. Its mean daily return was -0.154% (t -15.4, n 17381), and its 46,029 trades averaged -0.295% before fees and -0.395% after. This happened despite the confirmed post-settlement edge and a tiny positive per-bar gross position gain of 0.0033% (t 2.43). The bounce after deep falls (F1) works directly against shorting falling coins.

## Ideas
- `017-04_postsettle-decline-after-downtrend.c1_post-settlement-decline-four-hours.g1_one-day-fall-rebound` (from F1, F2, F6): After a coin falls over 24 hours, its return over the next 24 hours is positive, and the steeper the 24-hour fall, the larger that rebound.
- `017-04_postsettle-decline-after-downtrend.c1_post-settlement-decline-four-hours.g2_evening-utc-volatile-drift` (from F3, F4): A coin's return over the 2 hours from 20:00 UTC is positive, and the higher its 24-hour volatility at that time, the larger the rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
