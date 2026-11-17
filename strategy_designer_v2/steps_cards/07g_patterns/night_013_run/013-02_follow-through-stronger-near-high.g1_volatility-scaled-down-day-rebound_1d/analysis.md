---
line: 7.g patterns
backtest: 013-02_follow-through-stronger-near-high.g1_volatility-scaled-down-day-rebound_1d
idea tested: 013-02_follow-through-stronger-near-high.g1_volatility-scaled-down-day-rebound
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3642 USD
---
## Findings
- **F1:** The next-day rebound after a down day depends on volume as well as on the size of the fall. On down days (z<0), regressing the next-day excess return on the scaled fall, log volume ratio (day's volume over its prior 20-day mean) and their product gives an interaction slope of 0.00297 with t = 4.29. The fall alone then has t = −0.44.
- **F2:** The rebound is concentrated where both volatility and volume are high. Down days in a coin's top 20-day-volatility tercile and top volume-ratio tercile are followed by a mean next-day excess return of +0.0138 (t = 4.80, n = 649). In the bottom tercile of both the mean is −0.0021 (t = −1.21, n = 622).
- **F3:** The unscaled percentage fall predicts the next-day rise better than the volatility-scaled fall the idea uses. On down days the slope t is 9.37 for the raw fall against 4.58 for the scaled fall. Across raw-fall quintiles the mean next-day excess return rises from −0.0004 to +0.0069, and the top quintile has t = 4.17 (n = 1411).
- **F4:** The down-day rebound sits in high-volatility conditions in every coin and almost every year.
- **F5:** Volatility rising relative to its own longer level strengthens the rebound. Down days where 20-day volatility is high relative to 60-day volatility (top tercile) give +0.0054 (t = 3.77, n = 1417). The bottom tercile gives −0.0025 (t = −1.84).
- **F6:** High-volatility up days are followed by a small fall, and this is the mirror of the down-day rebound. The next-day excess after up days in the high-vol tercile is −0.0031 (t = −2.77), negative in five of six coins (XMR t = −2.88). The size of the rise itself carries no information (slope t = 0.21, n = 7286).
- **F7:** Next-day returns differ by weekday: Friday +0.0030 (t = 3.76) and Thursday +0.0025 (t = 2.63) against Wednesday −0.0030 (t = −2.70) and Monday −0.0024 (t = −2.53). The book's daily mean shows no matching pattern, and with many angles examined I treat this as unconfirmed.

## Ideas
- `013-02_follow-through-stronger-near-high.g1_volatility-scaled-down-day-rebound.g1_volume-confirmed-down-day-rebound` (from F1, F2): A coin's fall on a day on heavy volume, relative to its average daily volume over the previous 20 days, is followed by a rise over the next 1 day. The larger the fall multiplied by the volume surge, the larger the next day's rise.
- `013-02_follow-through-stronger-near-high.g1_volatility-scaled-down-day-rebound.g2_raw-size-down-day-rebound` (from F3, F4): A coin's percentage fall on a day, not scaled by its volatility, is followed by a rise over the next 1 day. The larger the fall in percent, the larger the next day's rise.
- `013-02_follow-through-stronger-near-high.g1_volatility-scaled-down-day-rebound.g3_rebound-grows-with-volatility-expansion` (from F4, F5): A coin's fall on a day is followed by a rise over the next 1 day that grows with how high its 20-day volatility stands against its 60-day volatility. The more volatility has expanded, the larger the next day's rise.
- `013-02_follow-through-stronger-near-high.g1_volatility-scaled-down-day-rebound.g4_high-volatility-up-day-giveback` (from F6, F4): A coin's rise on a day is followed by a fall over the next 1 day that grows with the level of its 20-day volatility. The higher the volatility, the larger the next day's fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
