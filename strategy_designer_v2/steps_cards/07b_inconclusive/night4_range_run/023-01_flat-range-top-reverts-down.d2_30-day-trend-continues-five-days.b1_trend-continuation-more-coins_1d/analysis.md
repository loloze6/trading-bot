---
line: 7.b inconclusive
backtest: 023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins_1d
idea tested: 023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.3938 USD
---
## Findings
- **F1:** Inside the tested regime, the test's 5-day horizon is the weakest of the clean readings: the slope of the drift-adjusted return on forecast/10 has t 4.27 over the next day (3221 cases, mean directional unusual move +0.39 %, t 3.91) and t 2.83 over 3 days (3138 cases, +0.54 %). Over 5 days it falls to t 1.86 (3120 cases, +0.71 %, t 2.76).
- **F2:** Over longer horizons the slope's t is 2.76 at 10 days (+1.34 %) and 4.52 at 20 days (+2.64 %), but these returns overlap on the 5-day grid, so their t is overstated by about √2 and √4. That leaves roughly 1.9 and 2.3.
- **F3:** The slope at 5 days comes almost entirely from the sign of the forecast, not its size. Within each side the slope is negative: t −2.82 on the short side (1539 cases) and −1.07 on the long side (1581 cases). The forecast quartiles show no gradient either: directional means of +1.37 %, +0.89 %, −0.59 % and +1.19 % from the smallest to the largest |forecast|.
- **F4:** The long side carries the 5-day effect: +1.16 % directional, t 2.73, 1581 cases. The short side gives +0.25 %, t 0.88, 1539 cases.
- **F5:** Across all grid bars, the 30-day return's continuation over 5 days is strongest where the 30-day net move covers a quarter to half of the 30-day high-low range: slope t 5.84, directional mean +1.40 %, 1688 cases (t 6.19 over 10 days). It weakens inside the tested regime's band of 0.5–0.75 (t 1.22, 1719 cases) and turns negative at 0.75 and above (t −1.22, 551 cases). The plan's condition therefore selects mostly the part of the data where the effect fades.
- **F6:** The effect is widespread but small per coin, and one year goes the other way. At 5 days, 15 of 19 coins have a positive slope, none with t above 1.64. By year, 2022 is strongly negative (t −3.01, 421 cases) and 2018 also negative (t −1.86, 189 cases).

## Ideas
- `023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins.b1_trend-continues-next-day` (from F1, F3): In a coin whose 30-day net move has been large relative to its 30-day high-low range, the larger its 30-day return, the further the coin moves in that same direction over the next day.
- `023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins.b2_building-trend-continues-five-days` (from F5, F2, F4): In a coin whose 30-day net move has been a moderate share of its 30-day high-low range, the larger its 30-day return, the further the coin moves in that same direction over the next 5 days. The move grows as the net move's share rises toward the middle of its scale and fades as the share nears its top.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
