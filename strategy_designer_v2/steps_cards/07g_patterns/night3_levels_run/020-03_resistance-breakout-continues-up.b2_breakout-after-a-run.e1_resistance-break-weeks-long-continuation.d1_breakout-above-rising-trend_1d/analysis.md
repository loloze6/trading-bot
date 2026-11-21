---
line: 7.g patterns
backtest: 020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.e1_resistance-break-weeks-long-continuation.d1_breakout-above-rising-trend_1d
idea tested: 020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.e1_resistance-break-weeks-long-continuation.d1_breakout-above-rising-trend
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3731 USD
---
## Findings
- **F1:** Across all 6 coins, closes 20 to 35 % below the coin's 90-day highest close were followed by a 20-day return 9.7 % below the coin's normal drift (t -4.8, 78 independent cases). The same dip shows with a 60-day high (-5.1 %, t -2.5, 108 cases) and with a 30-day high (-4.6 %, t -2.2, 108 cases), and all 6 coins are negative in that 60-day quintile (-1.4 % to -9.7 %).
- **F2:** That dip is not a graded effect. The deepest quintile, about 45 to 50 % below the high, is flat to positive (+2.9 %, t 1.1 on the 90-day high; -0.1 % on the 60-day high), and the rank correlation of distance from the high with the next 20 days is weak (rho 0.084, p 0.09, 395 cases on the 90-day high; rho 0.071, p 0.10 on the 60-day high).
- **F3:** The dip also does not hold across years. In the 60-day version, the 20-35 % below-high quintile was -19.9 % in 2018, -24.0 % in 2020 and -9.5 % in 2019, but +13.9 % in 2021 and +26.2 % in 2024. Across about 60 quintile cells looked at, it is a market-phase effect, not a stable one.
- **F4:** The book's edge over holding comes from being flat in falling windows, which the idea's 50-day-average gate explains. In w2 the book's mean daily return was -2.9 bps against the coins' -35.9; in w7 -14.0 against -47.3; in w14 -31.7 against -43.1. It lagged in the strongest rising windows: w11 49.1 against 125.6, w16 12.0 against 45.4.
- **F5:** Within the book's active bars, the forecast did not grade the move in a consistent way. On the grid cases with a positive forecast, the lower, middle and upper terciles gave +0.1 %, -4.5 % and +10.0 % unusual moves (31, 30 and 31 cases). Of the 962 trades, the middle entry-forecast tercile earned the most (26.8 % net mean, against 3.4 % and 10.8 %), and median trade results were near zero for most coins (LTC -2.8 %, XRP -1.5 %, BTC +0.4 %).
- **F6:** After the 1,390 bars where the forecast turned positive, the following 20 to 40 days still rose 3.7 % on average (t 4.2, n 1,096). These cases overlap and the figure is not net of the normal 20-day drift of about 2.4 %, so the continuation beyond the horizon is about 1.3 %. That is consistent with earlier finding F9 but not separable from chance here.
- **F7:** No other angle stood out against the number of cuts made. These were the last 1, 5 and 20 days' returns, volatility, distance from the 50-day average, distance from the 60-day low, and the year. The largest other cells were the 1-day-return lowest quintile (+4.1 %, t 2.0, 138 cases) and the second 50-day-distance quintile (-6.1 %, t -2.4, 78 cases), both non-monotone.

## Ideas
- No ideas: The only pattern that stands out (F1) is the 20-day underperformance after a moderate fall from the 60- to 90-day high, but it is not graded and it reverses across years (F2, F3), so no idea follows from it, and nothing else separates from chance across the many cuts made (F5, F6, F7).

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
