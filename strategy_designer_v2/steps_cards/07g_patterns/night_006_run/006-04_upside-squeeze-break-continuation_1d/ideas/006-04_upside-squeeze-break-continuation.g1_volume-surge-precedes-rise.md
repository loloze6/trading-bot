---
brief: 006_range-compression-precedes-expansion
source-idea: 006-04_upside-squeeze-break-continuation
line: 7.g patterns
backtest: 006-04_upside-squeeze-break-continuation_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The higher a coin's average daily volume over the last 5 days against its 30-day average, the more its price rises over the next 3 days relative to its usual 3-day return.
Consequence: A surge in a coin's recent volume is a reason to lean long for the next few days, and quiet, fading volume is a reason to stay out.
Why:
- F1: Across all six coins, the 5-day average volume over the 30-day average volume predicts the next 3-day return above the coin's average: on the non-overlapping 3-day grid (4283 cases) the OLS slope of excess return on log volume ratio is +0.0124 with t = 4.30, the top per-coin quintile averages +0.77% excess against -0.83% for the bottom quintile (Welch t = 3.75), and the share of rising 3-day outcomes goes from 47.1% to 52.5%.
- F2: The volume effect does not depend on the grid or the horizon: t is between 3.9 and 4.6 for 1-, 3- and 5-day horizons on every grid offset (1-day: t = 4.65, n = 13204; 5-day: t = 3.83 to 4.38, n ≈ 2500), and stays at 1.9 to 3.8 for 10 days.
- F3: The volume effect is not just recent trend or volatility: with the 5-day return and 20-day volatility also in the regression its t is 4.09, while the 5-day return (t = 1.10) and volatility (t = 1.79) explain little; it also does not depend on the direction of the recent move (log volume × sign of the 5-day return, t = -1.98 to +1.14).
- F4: The volume slope is positive for all six coins (t from 0.36 for LTC to 3.75 for XRP and 2.36 for ZEC) and in 7 of 8 years (2024 t = 5.01, 2021 t = 2.63; only 2018 is negative at t = -0.98), so the pooled effect is broad but strongest in XRP and ZEC.
