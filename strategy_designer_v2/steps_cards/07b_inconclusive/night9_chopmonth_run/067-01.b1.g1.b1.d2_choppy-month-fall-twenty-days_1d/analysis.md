---
line: 7.b inconclusive
backtest: 067-01.b1.g1.b1.d2_choppy-month-fall-twenty-days_1d
idea tested: 067-01.b1.g1.b1.d2_choppy-month-fall-twenty-days
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3924 USD
---
## Findings
- **F1:** Step 5's result is on the side the idea predicts but far short of the bar: +0.75 % unusual move per short case over 20 days, t 0.45 on 376 days (571 cases). The test already used every fold and all 19 coins on daily bars, so there is no more daily data to add.
- **F2:** The effect lives in agitated choppy bars. On folds B and C, short cases where the coin's 30-day swing was above its recent median earned +5.8 % unusual move over 5 days (t 3.58, 54 days, 61 cases), +7.3 % over 10 days (t 2.97, 42 days) and +11.4 % over 20 days (t 2.46, 30 days, 33 cases). Calm cases earned +0.8 % (t 0.43), +4.4 % (t 1.96) and +4.3 % (t 0.57). The total move in agitated cases was also positive (+4.6 %, +4.8 %, +5.7 %), so it covers the 0.22 % trade cost. These swings were judged against a 90-day median, not the profile's one-year median.
- **F3:** The plan's 20-day horizon is noisier than 10 days. On folds B and C, all short cases earned +2.74 % over 10 days (t 2.37, 170 days, 215 cases) against +4.75 % over 20 days (t 1.86, 127 days, 161 cases). The 20-day mean rests on few cells: only 30 non-overlapping fall cells, and 5 of 11 windows are negative.
- **F4:** The forecast's size does not grade the cases. The correlation of forecast size with the unusual move is -0.02 over 20 days and -0.05 over 10 days. The strongest forecasts (≤ -10) earned +0.6 % over 20 days (t 0.11), and the deepest 30-day falls (below -20 %) earned -4.2 % (t -0.65).
- **F5:** Read on plain non-overlapping choppy cells instead, the fall does grade the continuation over 10 days. The largest-fall quartile was followed by +14.0 % unusual fall (t 4.86, 21 cells), the second by +10.9 % (t 4.95), the third by +0.5 % and the smallest by -4.4 %. The correlation of the 30-day return with the unusual move was 0.51.
- **F6:** The effect is uneven across periods. Over 10 days, 5 of 12 windows give a negative mean unusual move (for example w8 -5.4 %, w17 -2.9 %, w11 -14.0 %), against strong windows such as w9 +8.1 % (t 4.62) and w16 +19.5 % (t 2.86). Much of the effect is drowned by the market's own moves in some periods.

## Ideas
- `067-01.b1.g1.b1.d2.b1_agitated-choppy-month-fall-continues` (from F2, F1, F5): In a choppy, agitated market, the larger a coin's fall over the past 30 days, the more it keeps falling over the next 20 days.
- `067-01.b1.g1.b1.d2.b2_choppy-month-fall-ten-days` (from F3, F5, F6): In a choppy market, the larger a coin's fall over the past 30 days, the more it keeps falling over the next 10 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
