---
line: 7.g patterns
backtest: 026-01_weekend-rise-reverses-early-week_1h
idea tested: 026-01_weekend-rise-reverses-early-week
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3854 USD
---
## Findings
- **F1:** In each coin's most volatile fifth of 24-hour cases, a large 24-hour move is followed by a move the opposite way over the next 24 hours. The slope of the standardised next-day return on the move, which is scaled by the coin's last 168 hours of mean absolute hourly return, is -0.175 with t = -9.41 (Spearman -0.178, p ≈ 5e-25, n = 3305 non-overlapping cases). Dropping the cases with |z| ≥ 4 leaves it at -0.176 with t = -8.62 (n = 3260), so it does not rest on outliers.
- **F2:** The reversal in F1 is graded and much larger than a trade's cost of 0.19 %. In that most volatile fifth, the unusual 24-hour move by quintile of the past move is +2.22 % after the largest falls (t 6.62, n 661), then +0.09 %, -0.34 %, -0.11 %, and -1.14 % after the largest rises (t -3.93, n 661).
- **F3:** The F1 reversal holds in every coin and nearly every year. The slope is between -0.108 and -0.233 for all six coins, with t from -2.51 (XRP) to -5.00 (LTC). It is negative in all seven years with at least 30 cases, with t ≤ -2.5 in 2018, 2020, 2021, 2022 and 2025, and t from -0.80 to -1.81 in 2019 and 2024.
- **F4:** The reversal fades as volatility falls. At 24 hours the slope is -0.018 (t -1.52) in the fourth volatility quintile and +0.003 to +0.018 in the lower three. At 12 hours it is -0.002 (t -0.13) even in the top quintile. At 48 hours it is -0.053 (t -2.00) there, so the effect sits at about a one-day horizon in volatile weeks.
- **F5:** The weekend reversal itself is absent, and it is no stronger than in the middle of the week. Weekend to Monday–Tuesday gives a slope of -0.0045 (t -0.32, n 2179); Monday–Tuesday to Wednesday–Thursday gives -0.0143 (t -0.98, n 2175). The tested short's unusual move is -0.02 % per case (t -0.10, 1123 cases), and the book's Sharpe is -0.68.
- **F6:** Hourly returns have clock-hour patterns, but they are far too small to pay a trade. Bars starting 21:00 UTC have a mean z-return of +0.047 (t 6.12), and 21:00 is positive in all six coins (t 1.98 to 2.92). Bars starting 13:00 average -0.041 (t -4.60). In raw terms, the 21:00 and 22:00 bars average +5.5 and +4.4 basis points, against a 19 basis-point cost.
- **F7:** In the calmest volatility quintile, the 12-hour slope is +0.027 (t 5.52) but the rank correlation is only 0.009 (p 0.47). This apparent continuation is carried by a few large values and is not a reliable pattern.

## Ideas
- `026-01_weekend-rise-reverses-early-week.g1_volatile-day-moves-reverse-next-day` (from F1, F2, F3, F4): When a coin is in a volatile stretch, with a high mean absolute hourly return over the past 7 days, its 24-hour return is partly reversed over the next 24 hours. The larger that 24-hour move relative to the past 7 days' hourly volatility, the larger the move back.
- `026-01_weekend-rise-reverses-early-week.g2_volatile-sell-off-next-day-rebound` (from F2, F1, F3): When a coin is in a volatile stretch, a fall over its last 24 hours is followed by a rise over the next 24 hours. The deeper the fall relative to the past 7 days' mean absolute hourly return, the larger the rebound.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
