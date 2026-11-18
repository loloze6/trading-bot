---
line: 7.g patterns
backtest: 006-04_upside-squeeze-break-continuation_1d
idea tested: 006-04_upside-squeeze-break-continuation
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3227 USD
---
## Findings
- **F1:** Across all six coins, the 5-day average volume over the 30-day average volume predicts the next 3-day return above the coin's average: on the non-overlapping 3-day grid (4283 cases) the OLS slope of excess return on log volume ratio is +0.0124 with t = 4.30, the top per-coin quintile averages +0.77% excess against -0.83% for the bottom quintile (Welch t = 3.75), and the share of rising 3-day outcomes goes from 47.1% to 52.5%.
- **F2:** The volume effect does not depend on the grid or the horizon: t is between 3.9 and 4.6 for 1-, 3- and 5-day horizons on every grid offset (1-day: t = 4.65, n = 13204; 5-day: t = 3.83 to 4.38, n ≈ 2500), and stays at 1.9 to 3.8 for 10 days.
- **F3:** The volume effect is not just recent trend or volatility: with the 5-day return and 20-day volatility also in the regression its t is 4.09, while the 5-day return (t = 1.10) and volatility (t = 1.79) explain little; it also does not depend on the direction of the recent move (log volume × sign of the 5-day return, t = -1.98 to +1.14).
- **F4:** The volume slope is positive for all six coins (t from 0.36 for LTC to 3.75 for XRP and 2.36 for ZEC) and in 7 of 8 years (2024 t = 5.01, 2021 t = 2.63; only 2018 is negative at t = -0.98), so the pooled effect is broad but strongest in XRP and ZEC.
- **F5:** The volume effect is stronger after a 5-day fall (slope +0.0169, t = 4.05, n = 2072) than after a 5-day rise (slope +0.0072, t = 1.81, n = 2211), so heavy volume after a decline is followed by a rebound more than heavy volume after a rise is followed by continuation.
- **F6:** The brief's compression itself does not predict a larger or a directional move: the most compressed 10-of-40-day quintile is followed by -0.25% excess against +0.63% for the least compressed (t = -2.02, weak given about ten features tested), and the absolute 3-day move barely differs (6.13% vs 5.78%, Spearman p = 0.30). By contrast, 20-day volatility and the day's range do grade the next absolute move (Spearman 0.26 and 0.25, p < 0.001).
- **F7:** The book adds almost nothing on top of holding: its mean daily return is 0.00004 against coin means of 0.0007 to 0.0016, and break-bar grid cases on LTC average -0.70% excess, so the upside-break position sits flat through most of the market's rise.

## Ideas
- `006-04_upside-squeeze-break-continuation.g1_volume-surge-precedes-rise` (from F1, F2, F3, F4): The higher a coin's average daily volume over the last 5 days against its 30-day average, the more its price rises over the next 3 days relative to its usual 3-day return.
- `006-04_upside-squeeze-break-continuation.g2_capitulation-volume-rebound` (from F5, F1, F3): After a coin has fallen over the last 5 days, the higher its 5-day average volume against its 30-day average, the larger its rebound over the next 3 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
