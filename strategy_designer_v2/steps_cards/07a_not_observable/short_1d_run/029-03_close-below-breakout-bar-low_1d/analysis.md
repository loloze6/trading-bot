---
line: 7.a not observable
backtest: 029-03_close-below-breakout-bar-low_1d
idea tested: 029-03_close-below-breakout-bar-low
step 5: not observable
step 6: not profitable enough
mode: one call
explorations: 1
cost: 0.2348 USD
---
## Findings
- **F1:** The idea could not be observed because the strategy's forecast reaches the situation rarely. Over 6 coins × 24 windows (17,524 daily bars), the forecast was short on only 63 bars. That left 18 cases on the 5-day grid, against the plan's minimum of 30. The six coins gave 6, 1, 2, 6, 1 and 2 cases (BTC, ETH, LTC, XMR, XRP, ZEC), and 15 of the 24 windows gave none.
- **F2:** The forecast reaches only part of the situation. Recomputed from prices, a close below the breakout day's low within 3 days of a close above the prior 20-day high happens on 207 bars, about 4.3 per coin per year. The recorded raw depth is above 0 on 149 bars, but the forecast is below 0 on only 63 bars, under half of the raw situation bars.
- **F3:** The situation is spread evenly across the years, so no single period is short of it. Price-recomputed situation bars run 11 to 33 per year from 2018 to 2025, with the fewest in 2022 (11). Forecast-short grid cases run 0 to 5 per year.
- **F4:** The direction is consistent across ways of counting the cases. On the 18 forecast cases, the mean excess 5-day return is −2.82 % (sd 7.40 %, t −1.62). On grid cells holding a short forecast it is −5.33 % (n 54, t −4.21). On grid cells holding a price-recomputed situation it is −2.32 % (n 140, t −3.01).
- **F5:** The case-to-case spread (sd 7.4 %) and the mean (−2.8 %) put the cases needed for t ≤ −2 at about 28, close to the plan's 30.
- **F6:** The forecast currently yields about 0.375 cases per coin-year (18 cases over 48 coin-years). Adding the 13 other coins in their folds gives about 53 more coin-years, about 100 in total, so about 38 cases at the same rate, above the minimum of 30.
- **F7:** Hourly bars would not add cases. The idea's times are in real time (a 20-day high, a 3-day failure, a 5-day horizon), and its cases fall on a 5-day grid, so the count depends on coin-years, not on bar size.

## Ideas
- `029-03_close-below-breakout-bar-low.a1_failed-breakout-all-coins` (from F1, F3, F4, F5, F6, F7): When a failed breakout above the prior 20-day high ends with a daily close below the low of the breakout day, the coin falls over the next 5 days, and the further that close sits below the breakout day's low, the larger the fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
