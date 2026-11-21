---
line: 7.b inconclusive
backtest: 018-06_hourly-plunge-multiday-continuation.d1_hourly-plunge-next-day-rebound.c1_deep-plunge-next-day-rebound_1h
idea tested: 018-06_hourly-plunge-multiday-continuation.d1_hourly-plunge-next-day-rebound.c1_deep-plunge-next-day-rebound
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3661 USD
---
## Findings
- **F1:** The main measure is on the side the idea predicts, but it is small: the mean excess 24-hour return after a bet is +0.108 % (t 1.92, 8426 cases), a strength of 0.020 of the coin's usual daily move (4.87 %), and the unusual move is only 0.6 times the 0.19 % cost of a trade.
- **F2:** The effect is graded as the idea says and lives in the deepest drops. At 24 hours, forecast 20 cases (drops of 2 multiples or more) gain +0.58 % (t 2.46, 693 cases), forecast 10 to 20 gain +0.19 % (t 1.21, 1167), forecast 4 to 10 gain +0.17 % (t 1.66, 2733), and forecast up to 4 lose -0.04 % (t -0.55, 3833). The shallow cases make up 45 % of the sample and dilute the mean.
- **F3:** The effect is mixed across coins and years. XMR gains +0.27 % (t 2.04), XRP +0.24 % (t 1.62) and ZEC +0.15 %, while BTC loses -0.03 % and ETH -0.06 %. By year, 2018 loses -0.61 % (t -3.11, 1121 cases), and every year from 2019 to 2025 is positive (+0.05 % to +0.43 %, 2021 at t 2.02). A single bear year holds the pooled t just under 2.
- **F4:** Most of the rebound comes from coins that were rising over the prior 30 days.
- **F5:** Inside the rising coins, the 5-day gain grows with the 30-day rise, not with the depth of the drop. By 30-day return tercile, the gain is -0.37 %, +1.56 % (t 3.09) and +1.58 % (t 2.45). The correlation of the 5-day gain with the 30-day return is 0.12, and with the forecast -0.02. The gain also swings by year: 2018 -5.35 %, 2021 +5.99 %, 2022 -1.47 %.
- **F6:** The 24-hour rebound depends on the hour of the signal's close, and the pattern is stable across both halves of the data.
- **F7:** The book does not beat holding the coins: its Sharpe is 0.53, 0.02 below holding's, and its Calmar is 0.25. This fits a 24-hour unusual move smaller than a trade's cost (the earlier findings F11 and F2).

## Ideas
- `018-06_hourly-plunge-multiday-continuation.d1_hourly-plunge-next-day-rebound.c1_deep-plunge-next-day-rebound.b1_hourly-plunge-rebound-more-coins` (from F1, F2, F3): When a coin's 24-hour return, read at an hourly close, is a drop of several times its 30-day average absolute daily return, the price rises over the next 1 day by more than the coin's normal 1-day drift. The larger the drop in those multiples, the larger the rise.
- `018-06_hourly-plunge-multiday-continuation.d1_hourly-plunge-next-day-rebound.c1_deep-plunge-next-day-rebound.b2_overnight-plunge-next-day-rebound` (from F2, F6): When a coin's 24-hour return, read at an hourly close, is a drop of several times its 30-day average absolute daily return, the price rises over the next 1 day by more than the coin's normal 1-day drift, only while that hourly close falls in the late evening or early hours UTC (18:00 to 06:00). The larger the drop in those multiples, the larger the rise.
- `018-06_hourly-plunge-multiday-continuation.d1_hourly-plunge-next-day-rebound.c1_deep-plunge-next-day-rebound.b3_dip-in-uptrend-five-day-rebound` (from F4, F5, F7): When a coin whose 30-day return is positive has a 24-hour return, read at an hourly close, that is a drop of several times its 30-day average absolute daily return, the price rises over the next 5 days by more than the coin's normal 5-day drift. The larger the coin's 30-day rise before the drop, the larger the rebound.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
