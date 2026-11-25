---
line: 7.g patterns
backtest: 032-02_flat-range-downside-break-recovers_1d
idea tested: 032-02_flat-range-downside-break-recovers
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.5285 USD
---
## Findings
- **F1:** On folds B and C, a daily close above the prior 20-day high was followed over the next 10 days by an excess return over the coin's mean of +11.95 % (day-clustered t 2.96, 33 cases on 18 days), against -0.40 % (t -0.33, 669 cases) on all other grid bars; that is about 0.8 of the coins' usual 10-day move of 13-24 %, far above the 0.19 % cost of a trade.
- **F2:** The upside-break continuation in F1 is fragile. It is positive on 9 of the 10 possible 10-day grid offsets (from -0.79 % to +11.95 %) and on 4 of the 5 possible 5-day offsets. Only offset 0 at both horizons (+5.10 %, t 2.31; +11.95 %, t 2.96) and 10-day offset 7 (+7.18 %, t 2.01) reach t 2, so the offset-0 figure is the best of the grid and not a typical one.
- **F3:** The same continuation holds at other look-backs. A close above the prior 10-day high was followed by +10.09 % over 10 days (t 3.21, 64 cases on 28 days) and +4.56 % over 5 days (t 2.71, 117 cases). A close above the prior 40-day high was followed by +9.87 % over 10 days (t 2.11, 23 cases).
- **F4:** The continuation is graded by where the close sits in its 20-day range. The 10-day excess return by quintile of range position runs -1.12 %, -2.68 %, -0.54 %, +0.48 %, +4.59 % (rank slope 2.12 % per standard deviation, day-clustered t 1.80, 702 cases on 126 days). The 3-day return points the same way (slope t 1.86, 2358 cases on 425 days), and so does the coin's 20-day return (10-day slope t 1.55, 3-day t 1.72).
- **F5:** Within the upside breaks, the size of the overshoot in volatility units does not grade the following move: the slope of the 10-day excess on it has t 0.51 (33 cases) and the 5-day slope has t 0.53 (66 cases). The grading in F4 comes from range position across all bars, not from the depth of the break.
- **F6:** The tested reversal of downside breaks does not appear in these folds. Closes below the prior 60-day low were followed by -8.11 % excess over 10 days (10 cases on only 3 days), and closes below the prior 20-day low by +7.39 % (t 1.10, 32 cases on 9 days). Neither can be told from chance, matching step 5's -1.56 % (t -0.56).
- **F7:** Of the many other angles looked at, none stands out once this many tests are taken into account; the largest weekday mean has t 1.75. Those angles are 1-day and 3-day returns, volatility level and change, 20-day efficiency, volume ratio, close location in the bar, bar range and weekday, at 3 and 10 days.

## Ideas
- `032-02.g1_top-of-range-close-continues` (from F1, F2, F3, F4, F5): In a coin, the higher its daily close sits within its range of the past 20 days, the more the coin rises over the next 10 days beyond its normal drift, with the largest rises following closes above the 20-day high.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
