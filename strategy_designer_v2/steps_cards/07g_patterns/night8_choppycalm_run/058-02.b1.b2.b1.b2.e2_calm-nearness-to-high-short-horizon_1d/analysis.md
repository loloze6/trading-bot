---
line: 7.g patterns
backtest: 058-02.b1.b2.b1.b2.e2_calm-nearness-to-high-short-horizon_1d
idea tested: 058-02.b1.b2.b1.b2.e2_calm-nearness-to-high-short-horizon
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4293 USD
---
## Findings
- **F1:** In a falling, calm market, where the close sits in its 20-day range predicts the next 3 days in the direction of the position, not back toward the middle. The excess 3-day return rises from −2.61 % and −2.50 % in the two lowest quarters of range position to +1.05 % and +1.54 % in the two highest. The slope's t is 2.67, with the cases of one day taken together (458 cases, 141 days). At 5 days the t is 2.07 (265 cases). The slope is positive in each year with enough cases: t 1.87 in 2018, 0.21 in 2019, 1.62 in 2021.
- **F2:** Over the next 5 days the calm-market nearness effect is stronger than over 3. On all calm bars the range-position slope has t 3.99 at 5 days (904 cases, 200 days) against t 2.91 at 3 days (1519 cases, 331 days). In choppy calm markets alone it is t 2.76 at 5 days (126 cases, 58 days) against t 0.87 at 3 days.
- **F3:** The book's trades earn far more when held longer. After fees, trades held 2 days or less average −1.19 % (median −2.36 %, 521 trades). Trades held 2 to 5 days average +0.35 %, 5 to 13 days +4.94 %, and over 13 days +12.77 % (479 trades). The edge needs time that a 3-day bet does not give it, which matters because the 3-day unusual move (+0.08 %) is below the 0.22 % cost of a trade.
- **F4:** The brief's reversion is not in choppy calm markets. On the 3-day grid, closes in the top fifth of the 20-day range average +0.37 % excess (44 cases), the middle −0.21 % (142 cases) and the bottom −0.99 % (28 cases). Closes near the top do no worse than the middle, and closes near the bottom do not rise.
- **F5:** In agitated markets, range position predicts nothing: the quintiles' excess 3-day returns range from −0.48 % to +0.40 %, with every t under 1. The day's own move reverses mildly only in falling, agitated markets (slope on the day's move in units of its 20-day swing, t −2.21, 274 cases, 75 days). That is the falling-agitated rebound the map already holds 12 times, so it is not a discovery.
- **F6:** Across weekdays, the next-day excess return after a Wednesday close is −0.45 % (t −2.60) and after a Friday close +0.37 % (t 2.85). Those t's count each coin separately on the same day. With seven weekdays looked at, and the map already holding a late-week gain (045-01), this does not stand out enough to count.

## Ideas
- `058-02.b1.b2.b1.b2.e2.g1_choppy-calm-high-continuation` (from F2, F3, F4): In a choppy, calm market, the nearer a coin's close is to its 20-day high, the larger its rise over the next 5 days.
- `058-02.b1.b2.b1.b2.e2.g2_falling-calm-low-continuation` (from F1, F4): In a falling, calm market, the nearer a coin's close is to its 20-day low, the larger its fall over the next 3 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
