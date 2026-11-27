---
line: 7.g patterns
backtest: 067-02.b1.b1.b2.b1_choppy-downside-stretch-more-coins_1d
idea tested: 067-02.b1.b1.b2.b1_choppy-downside-stretch-more-coins
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.5345 USD
---
## Findings
- **F1:** In the choppy bars of folds B and C (regime 'unknown'), 5-day grid cases with the close below its 20-day SMA are followed by a move beyond the coin's drift of -0.25 usual moves (183 cases, t -3.93, unweighted, cases not pooled by day). The deepest stretch (raw stretch < -1.5 swings) carries the most: -0.41 usual moves (74 cases, t -3.21). That is about six times the strength step 5 measured with the standardised, forecast-weighted stretch (0.068).
- **F2:** The raw stretch grades better at a longer horizon in choppy bars. Its Spearman correlation with the following excess move is 0.03 over 3 days, 0.11 over 5 days (346 cases) and 0.23 over 10 days. At 10 days the downside bins fall in order: -0.37 usual moves (z < -1.5, 45 cases, t -3.27), -0.32 (z from -1.5 to -0.5, 35 cases, t -1.98), -0.04 (z from -0.5 to 0.5, 34 cases, t -0.28).
- **F3:** The upside of the brief does not show in choppy bars. Closes stretched above the average are followed by small, uncertain gains: +0.13 usual moves for z > 1.5 (79 cases, t 0.89) and +0.04 for z from 0.75 to 1.5 (40 cases, t 0.39). So the carry is one-sided here, and the brief's two-sided theory does not hold.
- **F4:** The downside carry inside the choppy band does not depend on where the 60-day trend sits. For z < -0.75, the excess move is -0.47 usual moves when the 60-day return is from -10 % to -3 % (34 cases, t -2.98), -0.67 when it is flat (16 cases, t -2.01) and -0.27 when it is from +3 % to +10 % (18 cases, t -1.50).
- **F5:** By coin, for z < -1.5 in choppy bars, 9 of the 12 coins with cases show a negative excess move: BTC -0.77 usual moves (15 cases, t -2.07), XRP -0.62 (8 cases, t -2.49). By year, the downside is negative in all four years: 2018 -0.56 (t -3.54), 2019 -0.18 (t -2.15), 2020 -0.28 (t -1.67), 2021 -0.10 (t -0.99). It weakens over time.
- **F6:** The book loses because the drift works against a short, not because the stretch fails.
- **F7:** Other patterns are not new:

## Ideas
- `067-02.b1.b1.b2.b1.g1_choppy-downside-stretch-ten-days` (from F1, F2, F4, F5): In a choppy market, the further a coin's close stands below its 20-day average, counted in units of its 20-day standard deviation of daily returns, the more the coin keeps falling over the next 10 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
