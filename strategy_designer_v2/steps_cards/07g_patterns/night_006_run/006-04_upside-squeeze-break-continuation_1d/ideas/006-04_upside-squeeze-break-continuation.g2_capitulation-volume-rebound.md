---
brief: 006_range-compression-precedes-expansion
source-idea: 006-04_upside-squeeze-break-continuation
line: 7.g patterns
backtest: 006-04_upside-squeeze-break-continuation_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: After a coin has fallen over the last 5 days, the higher its 5-day average volume against its 30-day average, the larger its rebound over the next 3 days.
Consequence: Heavy volume during a decline signals capitulation that a trader can buy for a short rebound, while a decline on thin volume gives no such reason.
Why:
- F5: The volume effect is stronger after a 5-day fall (slope +0.0169, t = 4.05, n = 2072) than after a 5-day rise (slope +0.0072, t = 1.81, n = 2211), so heavy volume after a decline is followed by a rebound more than heavy volume after a rise is followed by continuation.
- F1: Across all six coins, the 5-day average volume over the 30-day average volume predicts the next 3-day return above the coin's average: on the non-overlapping 3-day grid (4283 cases) the OLS slope of excess return on log volume ratio is +0.0124 with t = 4.30, the top per-coin quintile averages +0.77% excess against -0.83% for the bottom quintile (Welch t = 3.75), and the share of rising 3-day outcomes goes from 47.1% to 52.5%.
- F3: The volume effect is not just recent trend or volatility: with the 5-day return and 20-day volatility also in the regression its t is 4.09, while the 5-day return (t = 1.10) and volatility (t = 1.79) explain little; it also does not depend on the direction of the recent move (log volume × sign of the 5-day return, t = -1.98 to +1.14).
