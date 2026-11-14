---
line: 7.e profitable but not proven
backtest: N2-04_slow-and-fast-momentum_1d
idea tested: N2-04_slow-and-fast-momentum
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.3512 USD
---
## Findings
- **F1:** The book's timing part is twice its market part: of a mean daily book return of 0.000754 (Sharpe 1.055), 0.000503 is timing and 0.000252 comes from the coins' own rise. On the days it holds a coin, that coin returns 0.002937 a day, against 0.000311 on the days it is out (5816 against 11564 coin-days).
- **F2:** The idea's excess return on active bars is real at short horizons and fades by the plan's 20 bars. Mean excess over the coin's mean, non-overlapping, by horizon:
- **F3:** The gain sits in young up-trends. In the first 0–10 bars of the trending regime, the 5-bar excess is 0.0113 (t 2.20, n 593) and the 10-bar excess is 0.0263 (t 2.46, n 298). Trends 31–60 bars old give -0.0038 at 5 bars and -0.0170 at 10 bars.
- **F4:** The book's profit is concentrated, but it is not a few-trades artefact of one coin:
- **F5:** The book earns in rising years and loses in falling ones:
- **F6:** The strength of the signal grades the 1-bar move. The 1-bar excess rises from 0.00056 (t 0.53) in the lowest forecast tercile to 0.00209 in the middle tercile and 0.00299 (t 2.15) in the highest, n about 1900 each. This grading is absent at 5 bars, where the Spearman correlation of the forecast with the excess is -0.003.

## Ideas
- `N2-04_slow-and-fast-momentum.e1_fresh-uptrend-short-continuation` (from F1, F2, F3, F4): After a coin's medium and slow returns have both just turned positive, its price keeps rising faster than its usual pace over the following days to two weeks, and the younger that joint up-trend is, the larger the extra rise.
- `N2-04_slow-and-fast-momentum.e2_trend-strength-next-day-drift` (from F2, F6): While a coin's medium and slow returns are both positive, the further those returns stand above their own usual size, the larger the coin's rise over the next day.
- `N2-04_slow-and-fast-momentum.e3_uptrend-signals-favour-rising-years` (from F5, F1): The excess rise that follows a joint up-turn in a coin's medium and slow returns is larger in years when that coin is itself trending up over the year.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
