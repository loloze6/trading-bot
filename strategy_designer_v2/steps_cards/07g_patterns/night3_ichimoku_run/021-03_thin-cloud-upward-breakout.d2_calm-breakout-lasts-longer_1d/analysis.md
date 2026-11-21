---
line: 7.g patterns
backtest: 021-03_thin-cloud-upward-breakout.d2_calm-breakout-lasts-longer_1d
idea tested: 021-03_thin-cloud-upward-breakout.d2_calm-breakout-lasts-longer
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4239 USD
---
## Findings
- **F1:** On daily bars, a coin's next-day return runs against the size of its day's move. Over all days with |z| > 1 (z is the day's return standardised by the coin's own mean and standard deviation), the Spearman correlation of z with the next day's return is -0.129 (p < 0.0001, n = 3510). This is the strongest pattern of the angles examined, and the one that would most clearly survive the many angles looked at.
- **F2:** The rebound after falls is graded. The next day's mean return is:
- **F3:** The rebound after large falls (z ≤ -2) is spread across the sample, not carried by one place:
- **F4:** Large rises are followed by a small giveback, which is weaker and fading. After days with z > 3 the next day's mean is -0.94 % (t -1.69, n 151). After days with z ≥ 2 the excess next-day return is negative on 5 of 6 coins (XMR -2.57 %, t -4.16; BTC t -2.09; ETH t -2.15). It is negative in every year from 2018 to 2023 but near zero or positive in 2024 and 2025.
- **F5:** Saturdays carry an excess daily return of +0.31 % over the coin's mean (t 3.84, n 2399), with t above 2 in 5 of 8 years. Tuesdays (-0.23 %, t -2.40) and Thursdays (-0.32 %, t -2.90) are below the mean. Weekday is a calendar condition, not a graded situation, so no idea is written from it.
- **F6:** Inside the tested cross cases, the 20-day volatility at the cross does not separate the outcomes clearly. The 40-day mean return falls from the calm tercile to the violent tercile (14.8 %, 12.3 %, 6.1 %; n 46, 45, 50), but its Spearman correlation with the 40-day return is only -0.146 (p 0.084, n 141). The bar's high-low range at the cross is similarly weak (rho -0.137, p 0.093).
- **F7:** The book's trades do not rise with the entry forecast. The middle forecast tercile earned +32.4 % per trade, against +7.2 % and +4.5 % for the low and high terciles (98 trades each). Its losing years, 2018 (-11.0 % mean per trade) and 2022 (-5.0 %), are years in which the cross cases themselves fell or stayed flat over 40 days (-32.8 % and +0.2 %).
- **F8:** Across all bars, the coin's own past return predicts little at the cross's horizon. On non-overlapping grids, top minus bottom tercile gives:

## Ideas
- `021-03_thin-cloud-upward-breakout.d2_calm-breakout-lasts-longer.g1_daily-fall-rebound-graded` (from F1, F2, F3): The larger a coin's one-day fall relative to its usual daily move, the more the coin rises over the next 1 to 3 days.
- `021-03_thin-cloud-upward-breakout.d2_calm-breakout-lasts-longer.g2_daily-spike-giveback-graded` (from F1, F4): The larger a coin's one-day rise relative to its usual daily move, the more the coin falls over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
