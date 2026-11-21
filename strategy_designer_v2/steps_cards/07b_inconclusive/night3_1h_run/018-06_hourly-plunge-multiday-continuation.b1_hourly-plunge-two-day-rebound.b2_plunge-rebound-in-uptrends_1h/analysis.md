---
line: 7.b inconclusive
backtest: 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends_1h
idea tested: 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.3456 USD
---
## Findings
- **F1:** The test came out inconclusive because its supporting check could not be computed, not because the effect was absent: 60.5 % of the 2345 cases entered at the forecast cap of 20, so the median entry forecast is 20.0 and no case lies strictly above it, while the main measure itself is +0.70 % per case with t 3.39.
- **F2:** Below the cap the effect is graded the way the idea predicts: by quintile of the raw fall-times-rise value, the top fifth (mean raw 36.4) earns an unusual 96-hour move of +1.85 % (t 3.01, 469 cases), against -0.19 % to +0.45 % for the middle three fifths; on all 701 non-overlapping 96-hour cells with a positive fall and a positive 30-day return, the cells above the product's median beat those below by 1.34 % (Welch t 1.96, 350 against 350), with Spearman rho 0.079 (p 0.035).
- **F3:** The effect is not spread evenly. It sits in 2020 (+2.04 %, t 4.42, 376 cases) and 2021 (+2.33 %, t 3.23, 320 cases), and is negative in 2018 (-1.14 %) and 2022 (-0.93 %). By coin it sits in ETH (+1.10 %, t 2.39), XRP (+1.44 %, t 2.01) and ZEC (+1.27 %, t 1.92), and is near zero in BTC (+0.06 %) and XMR (+0.09 %).
- **F4:** Much of the gain comes from the positive 30-day trend alone, not from the plunge. Grid cells with a positive 30-day return and no 24-hour fall earn +0.77 % unusual over 96 hours (t 2.30, 899 cells). Cells with a modest fall (0 to 2 usual moves) earn between -1.75 % and +0.15 %, and only the deepest plunges, beyond 3 usual moves, earn +8.1 % (t 3.08, 17 cells).
- **F5:** The move outlasts the 4-day horizon. The cases' total return is +0.36 % at 24 hours (t 3.45), +0.74 % at 48 hours (t 4.83), +0.70 % at 96 hours (t 3.39) and +1.84 % at 192 hours (t 5.73, 2254 cases), as F9 of the earlier runs found for other paying books.
- **F6:** The idea is large enough to pay its costs. Its total move per case is 6.2 times the 0.19 % round trip and its unusual move 3.6 times; the book earns a Sharpe of 1.02, 0.47 above holding the coins.

## Ideas
- `018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends.b1_plunge-rebound-all-coins` (from F1, F2, F3, F6): When a coin's 24-hour return, read at an hourly close, falls by a large multiple of its 30-day average absolute daily return, the price rises over the next 4 days by more than the coin's usual 4-day drift, only while the coin's 30-day return is positive, and the larger that 30-day rise, the larger the rebound.
- `018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends.b2_uptrend-plunge-eight-day-rebound` (from F2, F4, F5, F6): When a coin's 24-hour return, read at an hourly close, falls by a large multiple of its 30-day average absolute daily return while its 30-day return is positive, the price rises over the next 8 days by more than the coin's usual 8-day drift, and the larger the fall times the 30-day rise, the larger the rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
