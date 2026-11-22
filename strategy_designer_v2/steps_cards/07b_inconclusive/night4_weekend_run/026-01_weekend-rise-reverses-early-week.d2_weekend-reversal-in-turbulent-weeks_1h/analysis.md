---
line: 7.b inconclusive
backtest: 026-01_weekend-rise-reverses-early-week.d2_weekend-reversal-in-turbulent-weeks_1h
idea tested: 026-01_weekend-rise-reverses-early-week.d2_weekend-reversal-in-turbulent-weeks
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3754 USD
---
## Findings
- **F1:** The main measure is on the predicted side, with a weighted mean unusual 48-hour fall of +1.15 % and t 2.80 over 557 cases. It is inconclusive only because the grading fails: the larger half of abs(forecast) minus the smaller half is -0.08 %. My recomputation agrees, with a mean unusual fall of +0.89 %, t 2.77, n 547.
- **F2:** Inside the cases the size of the weekend gain does not grade the fall. The Spearman correlation of the weekend gain with the fall is 0.053 (p 0.22), and 0.030 (p 0.50) once the gain is scaled by volatility. Across raw-gain quintiles the fall runs +0.67 %, +0.52 %, +0.66 %, +1.72 %, +0.85 %. Across forecast quintiles it runs +1.24 %, +0.49 %, +0.63 %, -0.04 %, +2.09 %, with no order.
- **F3:** The effect sits in two years. The fall is +4.91 % (t 3.21, n 51) in 2018 and +2.95 % (t 3.90, n 81) in 2025. Over the six other years it is -0.01 % (t -0.04, n 415), and the per-window means range from -2.45 % to +8.14 %, with a median of +0.63 % over 23 windows.
- **F4:** The effect is spread unevenly over the coins. LTC (+1.33 %, t 2.01), XMR (+1.06 %, t 1.76), ETH (+1.10 %, t 1.47) and ZEC (+1.47 %, t 1.45) lean the predicted way. BTC goes against it (-0.35 %, t -0.60).
- **F5:** Rises ending at Monday 00:00 are not reversed more than rises ending on other days. With my recomputed high-volatility rank (at least 0.5), rises ending at Monday 00:00 fall +0.23 % (t 0.62, n 406), and rises ending at Tuesday 00:00 fall +0.61 % (t 2.05, n 375). Weekend rises across all volatility levels fall +0.14 % (t 0.67, n 1289).
- **F6:** The fall shows on a horizon of two days or more. It is +0.23 % (t 0.89) over 24 hours, +0.89 % (t 2.77) over 48 hours, +0.76 % (t 2.12) over 72 hours and +1.15 % (t 2.62) over 96 hours.
- **F7:** In calm weeks a weekend fall carries on early in the week. When the recorded regime is low volatility, weekend falls keep falling, with a reversal of -1.01 % (t -3.74, n 601) over the next 48 hours. Weekend rises keep rising, with a reversal of -0.41 % (t -1.55, n 742).

## Ideas
- `026-01_weekend-rise-reverses-early-week.d2_weekend-reversal-in-turbulent-weeks.b1_turbulent-weekend-reversal-more-coins` (from F1, F2, F3, F4): When a coin's price rises from Saturday 00:00 UTC to Monday 00:00 UTC, it falls over the following two days (Monday and Tuesday), only while the coin's 30-day hourly volatility is high against its own last 6 months. The larger the weekend gain, the larger the fall.
- `026-01_weekend-rise-reverses-early-week.d2_weekend-reversal-in-turbulent-weeks.b2_calm-weekend-falls-continue` (from F7): When a coin's price falls from Saturday 00:00 UTC to Monday 00:00 UTC while the coin's 30-day hourly volatility is low against its own last 6 months, it keeps falling over the next two days (Monday and Tuesday). The larger the weekend fall, the larger the further fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
