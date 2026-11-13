---
line: 7.g patterns
backtest: 002-02_sma-death-cross-downward-drift_1d
idea tested: 002-02_sma-death-cross-downward-drift
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3122 USD
---
## Findings
- **F1:** Bars where the 50-day SMA had only just fallen below the 200-day SMA (raw spread between -40 and +1, the fourth octile) were followed by a 10-bar return 2.18% above the coin's mean, with t = 2.76 and 58.4% up. This was the only spread octile that cleared |t| > 2, and its sign is the opposite of what the death-cross short expects.
- **F2:** Inside that near-cross zone, the rebound came mostly when the spread was still widening downward over the past 10 bars: +3.46% 10-bar excess, t = 3.17, 62.9% up, n = 1066. When the spread was already narrowing the excess was +0.84%, t = 0.75. The pattern held in both early and late windows (t = 1.86 and 2.12) and pointed the same way in all six coins (+1.3% to +5.6%).
- **F3:** After a down day (z-move below -0.5 of 20-day volatility), the next day's return beat the coin's mean by 0.41%, t = 3.89, 58.0% up, while the 50-day SMA was below the 200-day SMA. When it was not, the excess was 0.25%, t = 1.90. The bounce was positive in all six coins (t from 0.74 to 3.88), and up days were followed by slightly below-mean returns in four of six coins.
- **F4:** The day after a Friday-stamped bar beat the coin's mean by 0.34%, t = 4.32, 54.5% up. This held in early windows (t = 4.31) and late windows (t = 2.00) and was positive in all six coins (t from 0.66 to 2.71). The day after a Wednesday-stamped bar was below the mean by 0.34%, t = -3.02, and negative in all six coins.
- **F5:** The short book's 10-bar excess depended on the year, not on the cross. While the forecast was short it was +6.2% (t = 4.23) in 2020, +4.8% (t = 2.45) in 2021, +2.2% (t = 2.35) in 2023 and +3.3% (t = 2.89) in 2024, in the coin's favour against the short. It helped the short only in 2018 and 2022. This lines up with the trades: 143 to 272 trades per coin, win rates of 19% to 28%, and mean net losses of -8.5% to -14.9% per trade.

## Ideas
- `002-02_sma-death-cross-downward-drift.g1_fresh-death-cross-rebound` (from F1, F2, F5): When a coin's 50-day SMA has just crossed below its 200-day SMA and the gap is still widening, the coin's price rises over the following ten daily bars more than its usual drift, because the fresh death cross marks the exhaustion of the selloff.
- `002-02_sma-death-cross-downward-drift.g2_down-day-bounce-under-death-cross` (from F3): While a coin's 50-day SMA is below its 200-day SMA, a daily close that fell by more than half its recent daily volatility is followed by a next-day return above the coin's average.
- `002-02_sma-death-cross-downward-drift.g3_weekday-drift-in-daily-bars` (from F4): In each coin, the daily bar that follows the Friday-stamped bar returns more than the coin's average daily bar, and the bar that follows the Wednesday-stamped bar returns less.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
