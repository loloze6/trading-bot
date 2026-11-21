---
line: 7.g patterns
backtest: 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends.e2_monthly-rise-multiweek-continuation.e1_monthly-rise-weekly-continuation_1h
idea tested: 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends.e2_monthly-rise-multiweek-continuation.e1_monthly-rise-weekly-continuation
step 5: confirmed
step 6: profitable enough
mode: one call
explorations: 3
cost: 0.6474 USD
---
## Findings
- **F1:** Saturday (UTC) is the one weekday whose daily return stands clearly above the coin's normal daily drift: +33.5 bps a day, t 4.08 over 2484 coin-days. The next best is Friday at +21.1 bps, t 2.25, against Thursday at −29.9 bps, t −2.70, and Tuesday at −24.2 bps, t −2.53. It holds in 6 of 8 years (2019 +45.9 bps t 2.67, 2024 +45.2 t 2.21, 2025 +54.0 t 2.63; 2022 −4.5, 2023 −12.0) and in all 6 coins (BTC +3.9 bps, the others +26 to +51 bps).
- **F2:** Saturday's unusual return follows the coin's return over the five days before it, step by step. By prior 5-day quintile it is −44.6 bps (t −2.20, n 480), −8.8 (t −0.65), +43.8 (t 3.93), +74.0 (t 3.90), +102.5 bps (t 4.09, n 480). The top-to-bottom spread of about 147 bps is about 7 times this backtest's 19 bps round-trip cost.
- **F3:** The two hours 21:00–23:00 UTC rise in every coin, at +5.5 bps (t 6.87) and +4.4 bps (t 5.76) per hourly bar. The two hours together rise 4.3 to 5.6 bps per coin (t 3.0 to 4.6) and are positive in 7 of 8 years (2022 −2.2 bps). The two-hour move is 4 to 16 bps across prior-20-hour quintiles, not monotone. That is below the 19 bps cost, as in earlier finding F2.
- **F4:** The tested monthly rise carries its excess move mostly in its top part and does not last past a week. On the 168-hour grid the strength by 30-day-return quintile is −0.099 (t −2.14), −0.031, +0.027, +0.108 (t 1.74) for the top. In forecast quintiles the top is +0.167 (t 1.86) and the others are −0.05 to +0.06. At 336 hours the top quintile falls to +0.033 (t 0.42).
- **F5:** A milder 30-day decline looked like continuation on raw returns: quintile 1 strength −0.099 at 168 h, negative-side slope t −2.68, n 833. It does not survive scaling by volatility (slope t 0.21), and it changes sign by year (2019 +0.066, 2023 +0.042). It is not a finding to build on.
- **F6:** The book's trades entered at the highest forecast are shorter and earn less. The top entry-forecast quintile (mean 19.2) lasts about 18,100 minutes and nets +5.1 %. The bottom quintile (mean 4.2) lasts about 52,400 minutes and nets +13.4 %. The book's gain sits in its longest quarter of trades (+39.4 % mean net, median +20.9 %), while the shortest quarter loses (−1.27 %).
- **F7:** The book trails holding in rising years and loses less in falling ones. In 2021 it earned +18 bps a day against +41 for holding, and in 2018 it lost −12 bps a day against −35. It earned less than holding in XMR (+5.4 vs +10.7 bps) and ZEC (+9.6 vs +15.5 bps).

## Ideas
- `018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends.e2_monthly-rise-multiweek-continuation.e1_monthly-rise-weekly-continuation.g1_weekend-continues-the-week` (from F1, F2): A coin's Saturday return (UTC) follows its return over the preceding five days. The larger that 5-day return up to the close of Friday, the higher the coin's return over the next day, Saturday, against its normal daily drift.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
