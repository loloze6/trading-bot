---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-01_weekend-rise-reverses-early-week
line: 7.g patterns
backtest: 026-01_weekend-rise-reverses-early-week_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin is in a volatile stretch, a fall over its last 24 hours is followed by a rise over the next 24 hours. The deeper the fall relative to the past 7 days' mean absolute hourly return, the larger the rebound.
Consequence: After a sharp one-day sell-off in a volatile week, a trader buys the coin for the next day, more after a deeper fall, because this rebound is larger than the reversal of rallies.
Why:
- F2: The reversal in F1 is graded and much larger than a trade's cost of 0.19 %. In that most volatile fifth, the unusual 24-hour move by quintile of the past move is +2.22 % after the largest falls (t 6.62, n 661), then +0.09 %, -0.34 %, -0.11 %, and -1.14 % after the largest rises (t -3.93, n 661).
- F1: In each coin's most volatile fifth of 24-hour cases, a large 24-hour move is followed by a move the opposite way over the next 24 hours. The slope of the standardised next-day return on the move, which is scaled by the coin's last 168 hours of mean absolute hourly return, is -0.175 with t = -9.41 (Spearman -0.178, p ≈ 5e-25, n = 3305 non-overlapping cases). Dropping the cases with |z| ≥ 4 leaves it at -0.176 with t = -8.62 (n = 3260), so it does not rest on outliers.
- F3: The F1 reversal holds in every coin and nearly every year. The slope is between -0.108 and -0.233 for all six coins, with t from -2.51 (XRP) to -5.00 (LTC). It is negative in all seven years with at least 30 cases, with t ≤ -2.5 in 2018, 2020, 2021, 2022 and 2025, and t from -0.80 to -1.81 in 2019 and 2024.
